import sys, os, logging, csv
import cPickle as pickle
import os.path
logging.basicConfig(level=logging.INFO)

reload(sys)
sys.setdefaultencoding('utf8')

import numpy as np
import scipy as sp
import sklearn


from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.cross_validation import train_test_split
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import confusion_matrix, precision_score, precision_recall_fscore_support
from sklearn.grid_search import ParameterGrid

from nltk.tokenize.punkt import PunktSentenceTokenizer
from nltk.corpus import stopwords

sys.path.insert(0, os.getcwd())
import cochranenlp
from cochranenlp.readers import biviewer

'''
get the text
- tokenize the text into sentences
- vectorize the sentences using HashingVectorizer
TODO: add more features

Per PICO
- Iterate over all CDSR studies
  * Get the PICO text and compute cosine distance with the LSH
  * If distance > threshold set y = 1, 0 otherwise

Predict [X,y] with 5-fold crossvalidation per PICO using SGD

'''

DATA_PATH = cochranenlp.config["Paths"]["base_path"]

PICO_DOMAINS = ["CHAR_PARTICIPANTS", "CHAR_INTERVENTIONS", "CHAR_OUTCOMES"]

viewer = biviewer.PDFBiViewer()

sentence_tokenizer = PunktSentenceTokenizer()

class memoize:
    def __init__(self, function):
        self.function = function
        self.memoized = {}

    def __call__(self, *args):
        try:
            return self.memoized[args]
        except KeyError:
            self.memoized[args] = self.function(*args)
            return self.memoized[args]


def get_sentences(held_out):
    pmids = set()
    sentences = []
    for study in viewer:
        pmid = study[1]['pmid']
        if pmid in held_out:
            continue
        if pmid not in pmids:  # Not Cached
            logging.debug("parsing sentences for %s" % pmid)
            text = study.studypdf["text"].decode("utf-8", errors="ignore")
            sentences.append(sentence_tokenizer.tokenize(text))
            pmids.add(pmid)
        else:
            logging.debug("skipping, already parsed %s" % pmid)
    return [{"pmid": k, "sentence": v} for k, t in zip(pmids, sentences) for v in t]


def vectorize(sentences):
    h = HashingVectorizer(stop_words=stopwords.words('english'),
                          norm="l2",
                          ngram_range=(1, 2),
                          analyzer="word",
                          decode_error="ignore")
    return h.transform(sentences)


def get_X(sentences):
    return vectorize([x["sentence"] for x in sentences])


def get_characteristic_fragments(pmid, domain):
    studies = viewer.get_study_from_pmid(pmid)
    char = [s[0]["CHARACTERISTICS"][domain] or "" for s in studies]
    return " ".join(char)


def __get_lsh(domain, pmid, sentences):
    s2 = sentence_tokenizer.tokenize(get_characteristic_fragments(domain, pmid))
    y1 = vectorize(s2) if s2 else vectorize([""])

    # determine the cosine similarity of the sentences, and marking as relevant if exceeding threshold
    y2 = vectorize(sentences)
    return (y1 * y2.T)


def get_y(domain, sentences, threshold=0.3):
    y = np.empty(len(sentences), 'bool')

    pmid_ptr = None
    tmp = []
    idx_ptr = 0
    for idx, s in enumerate(sentences):
        if not pmid_ptr:
            pmid_ptr = s['pmid']
        elif pmid_ptr != s['pmid']:
            # next pmid
            logging.debug("distilling essence of %s for %s at %s" % (pmid_ptr, domain, threshold))
            R = __get_lsh(domain, pmid_ptr, tmp)
            y[idx_ptr:idx] = sum(np.any(R > threshold)).A[0, :]

            tmp = []
            idx_ptr = idx
            pmid_ptr = s['pmid']

        tmp.append(s['sentence'])

    return y


def get_test_data(file):
    out = []
    with open(file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            out.append(row)

    held_out = set([t['study id'] for t in out])
    return out, held_out


def scorer_factory(test_data):
    X_test = vectorize([t['candidate sentence'] for t in test_data])
    y_true = np.array([1 if t['rating'] == '2' else 0 for t in test_data])

    def scorer(estimator, X, y):
        y_pred = estimator.predict(X_test)
        return precision_recall_fscore_support(y_true, y_pred)

    return scorer


def run_experiment(X, domain, sentences, scorer):
    logging.debug("running experiment for %s" % domain)
    y = get_y(domain, sentences)

    tune_params = ParameterGrid([
        {"alpha": [.00001, .001, 1, 10],
         "threshold": [0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.5]}])

    best_estimator = None
    best_score = 0

    for params in tune_params:
        logging.info("running %s with alpha=%s, threshold=%s" % (domain, params["alpha"], params["threshold"]))
        y = get_y(domain, sentences, threshold=params["threshold"])
        sgd = SGDClassifier(shuffle=True, loss="hinge", penalty="l2", alpha=params["alpha"])
        sgd.fit(X, y)
        precision, recall, f1 = scorer(sgd)
        logging.info("precision %s, recall %s, f1 %s" % (precision, recall, f1))
        if(precision > best_score):
            best_estimator = sgd

    logging.debug("storing %s" % domain)
    with open(DATA_PATH + domain + ".pck", "wb") as f:
        pickle.dump(best_estimator, f)
        f.close()


def run_experiments():
    logging.info("setting up")
    ratings = DATA_PATH + "../sds/annotations/master/figure8-2-15.csv"
    test, held_out = get_test_data(ratings)
    sentences = get_sentences(held_out)
    train_X = get_X(sentences)
    scorer = scorer_factory(test)

    logging.info("starting experiments")
    for domain in PICO_DOMAINS:
        run_experiment(train_X, domain, sentences, scorer)


if __name__ == '__main__':
    run_experiments()
