from tokenizer import sent_tokenizer, word_tokenizer
import biviewer
import re
import progressbar
import collections
import string
from unidecode import unidecode
import codecs

import yaml
from pprint import pprint

import numpy as np
import math

import difflib

import sklearn
from sklearn.feature_extraction.text import CountVectorizer

from sklearn.feature_extraction import DictVectorizer

from sklearn import cross_validation
from sklearn import metrics
from sklearn import svm
from sklearn.linear_model import SGDClassifier

from collections import defaultdict

from sklearn.metrics import precision_recall_fscore_support
import random

from sklearn.cross_validation import KFold

from journalreaders import PdfReader

import cPickle as pickle

# QUALITY_QUOTE_REGEX = re.compile("Quote\:\s*[\'\"](.*?)[\'\"]")


REGEX_QUOTE_PRESENT = re.compile("Quote\:")
REGEX_QUOTE = re.compile("\"(.*?)\"") # retrive blocks of text in quotes
REGEX_ELLIPSIS = re.compile("\s*[\[\(]?\s?\.\.+\s?[\]\)]?\s*") # to catch various permetations of "..." and "[...]"

SIMPLE_WORD_TOKENIZER = re.compile("[a-zA-Z]{2,}") # regex of the rule used by sklearn CountVectorizer

CORE_DOMAINS = ["Random sequence generation", "Allocation concealment", "Blinding of participants and personnel",
                "Blinding of outcome assessment", "Incomplete outcome data", "Selective reporting"]
                # "OTHER" is generated in code, not in the mapping file
                # see data/domain_names.txt for various other criteria
                # all of these are available via QualityQuoteReader

ALL_DOMAINS = CORE_DOMAINS[:] # will be added to later




def show_most_informative_features(vectorizer, clf, n=10):
    ###
    # note that in the multi-class case, clf.coef_ will
    # have k weight vectors, which I believe are one per
    # each class (i.e., each is a classifier discriminating
    # one class versus the rest). 
    c_f = sorted(zip(clf.coef_, vectorizer.get_feature_names()))

    if n == 0:
        n = len(c_f)/2

    top = zip(c_f[:n], c_f[:-(n+1):-1])
    print
    print "%d most informative features:" % (n, )
    out_str = []
    for (c1, f1), (c2, f2) in top:
        out_str.append("\t%.4f\t%-15s\t\t%.4f\t%-15s" % (c1, f1, c2, f2))
    feature_str = "\n".join(out_str)
    return feature_str


def show_most_informative_features_ynu(vectorizer, clf, n=10):
    ###
    # note that in the multi-class case, clf.coef_ will
    # have k weight vectors, which I believe are one per
    # each class (i.e., each is a classifier discriminating
    # one class versus the rest). 

    combinations =  ["NO vs (YES + UNKNOWN)", "UNKNOWN vs (YES + NO)", "YES vs (NO + UNKNOWN)"]

    out_str = []

    for i, combination in enumerate(combinations):

        out_str.append(combination)
        out_str.append("*" * 20)

        c_f = sorted(zip(clf.coef_[i], vectorizer.get_feature_names()))

        if n == 0:
            n = len(c_f)/2

        top = zip(c_f[:n], c_f[:-(n+1):-1])
    
        for (c1, f1), (c2, f2) in top:
            out_str.append("\t%.4f\t%-15s\t\t%.4f\t%-15s" % (c1, f1, c2, f2))
    feature_str = "\n".join(out_str)
    return feature_str

def load_domain_map(filename="data/domain_names.txt"):

    with codecs.open(filename, 'rb', 'utf-8') as f:
        raw_data = yaml.load(f)

    mapping = {}

    for key, value in raw_data.iteritems():
        for synonym in value:
            mapping[synonym] = key

    return mapping

class QualityQuoteReader():
    """
    iterates through Cochrane Risk of Bias information for domains where there is a quote only
    """

    def __init__(self, quotes_only=True):
        self.BiviewerView = collections.namedtuple('BiViewer_View', ['cochrane', 'studypdf'])
        self.pdfviewer = biviewer.PDFBiViewer()
        self.domain_map = load_domain_map()
        self.quotes_only = quotes_only


    def __iter__(self):
        """
        run through PDF/Cochrane data, and return filtered data of interest
        preprocesses PDF text
        and maps domain title to one of the core Risk of Bias domains if possible
        """

        used_pmids = set()

        p = progressbar.ProgressBar(len(self.pdfviewer), timer=True)

        for study in self.pdfviewer:

            p.tap()

            quality_quotes = []
            quality_data = study.cochrane["QUALITY"]


            for domain in quality_data:
                
                
                if REGEX_QUOTE_PRESENT.match(domain['DESCRIPTION']) or not self.quotes_only:

                    domain['DESCRIPTION'] = self.preprocess_cochrane(domain['DESCRIPTION'])
                    try:
                        mapped_domain = self.domain_map[domain["DOMAIN"]] # map domain titles to our core categories

                        domain["DOMAIN"] = mapped_domain
                        
                        if mapped_domain not in ALL_DOMAINS:                            
                            ALL_DOMAINS.append(mapped_domain)
                        
                        
                            
                    except:
                        domain["DOMAIN"] = "OTHER"
                    
                    quality_quotes.append(domain)

            if quality_quotes:
                yield self.BiviewerView(cochrane={"QUALITY": quality_quotes}, studypdf=self.preprocess_pdf(study.studypdf))
                # returns only the quality data with quotes in it for ease of use; preprocesses pdf text


    def preprocess_pdf(self, pdftext):
        pdftext = unidecode(pdftext)
        pdftext = re.sub("\n", " ", pdftext) # preprocessing rule 1
        return pdftext

    def preprocess_cochrane(self, rawtext):

        # regex clean up of cochrane strings
        processedtext = unidecode(rawtext)
        processedtext = re.sub(" +", " ", processedtext)

        # extract all parts in quotes
        quotes = REGEX_QUOTE.findall(processedtext)

        # then split at any ellipses
        quote_parts = []
        for quote in quotes:
            quote_parts.extend(REGEX_ELLIPSIS.split(quote))
        return quote_parts
        

    def domains(self):
        domain_headers = set((value for key, value in self.domain_map.iteritems()))
        return list(domain_headers)



# class SentenceDataViewer():
#     """
#     Stores data at sentence level in parallel with study level indices
#     """
#     def __init__(self, indices=None, data=None)



class PDFMatcher():
    """
    matches and generates sent tokens from pdf text
    """
    def __init__(self, quotes=None, pdftext=None):
        # load a sequence matcher; turn autojunk off (since buggy for long strings)
        self.sequencematcher = difflib.SequenceMatcher(None, autojunk=False)

        if quotes:
            self.quotes = self.load_quotes(quotes)
        if pdftext:
            self.pdftext = self.load_pdftext(pdftext)




    def load_quotes(self, quotes):
        self.quotes = quotes

    def load_pdftext(self, pdftext):
        self.pdftext = pdftext
        self.lenpdf = len(pdftext)
        self.sequencematcher.set_seq2(self.pdftext)
        self.sent_indices =  sent_tokenizer.span_tokenize(self.pdftext)


    def _overlap(self, t1, t2):
        """
        finds out whether two tuples overlap
        """
        t1s, t1e = t1
        t2s, t2e = t2

        # true if either start of t1 is inside t2, or start of t2 is inside t1
        return (t2s <= t1s <= t2e) or (t1s <= t2s <= t1e) 


    def generate_X(self):
        X = []
        # go through sentence indices
        # make X (list of sentences)
        for (start_i, end_i) in self.sent_indices:
            X.append(self.pdftext[start_i: end_i])
        return X


    def generate_y(self, min_char_match=20):
        """
        returns X: list of sentence strings
                y: numpy vector of 1, -1 (for positive/negative examples)
        """
        good_match = False # this will be set to True if sufficent matching characters in
                           # at least one of the parts of the quotes

        match_indices = []


        # go through quotes, match using difflib
        # and keep any matches which are long enough so likely true matches
        for quote in self.quotes:

            self.sequencematcher.set_seq1(quote)

            best_match = self.sequencematcher.find_longest_match(0, len(quote), 0, self.lenpdf)

            # only interested in good quality matches
            if best_match.size > min_char_match:
                good_match = True
                match_indices.append((best_match.b, best_match.b + best_match.size)) # add (start_i, end_i) tuples (of PDF indices)

        
        y = []

        if not good_match:
            # if quality criteria not met, leave here
            # (i.e. return empty lists [], [])
            return y

        # otherwise continue and generate feature and answer vectors

        # get indices of sentences (rather than split)
        sent_indices = sent_tokenizer.span_tokenize(self.pdftext)

        # go through sentence indices
        # make X (list of sentences)
        # and calculate y, if there is *any* overlap with matched quoted text then
        # y = True
        for (start_i, end_i) in sent_indices:



            # if any overlaps with quotes, then y = True, else False
            if any((self._overlap((start_i, end_i), match_tuple) for match_tuple in match_indices)):
                y.append(1)
            else:
                y.append(-1)

        return y



class SentenceDataView():
    def __init__(self, study_ids, data):
        self.study_ids = study_ids
        self.data = data







class SentenceVectorizer():
    """
    for predicting whether sentences relate to a risk of bias domain
    """

    def __init__(self):
        pass
        

    def generate_data(self, test_mode=False, restrict_to_core=False):

        self.test_mode = test_mode
        if self.test_mode:
            print "WARNING - in test mode, using data sample only"



        if restrict_to_core:
            test_domains = CORE_DOMAINS
        else:
            test_domains = ALL_DOMAINS

        # one y vector for each core domain

        # one feature matrix X
        self.X_list = SentenceDataView([], [])

        y_list = defaultdict(lambda: SentenceDataView([], []))




        q = QualityQuoteReader()

        for study_i, study in enumerate(q):

            matcher = PDFMatcher()
            matcher.load_pdftext(study.studypdf)

            
            X_study = matcher.generate_X()
            self.X_list.data.extend(X_study)
            self.X_list.study_ids.extend([study_i] * len(X_study))

            domains_done_already = [] # for this particular study
            # (we're ignoring multiple quotes per domain at the moment and getting the first...)

            for domain in study.cochrane["QUALITY"]:

                matcher.load_quotes(domain["DESCRIPTION"])
                y_study = matcher.generate_y()

                if domain["DOMAIN"] in domains_done_already:
                    continue
                else:
                    domains_done_already.append(domain["DOMAIN"])
                    y_list[domain["DOMAIN"]].data.extend(y_study)
                    y_list[domain["DOMAIN"]].study_ids.extend([study_i] * len(y_study))

                


                

            if self.test_mode and study_i == 250:
                break

        self.vectorizer = CountVectorizer(max_features=5000)

        


        self.X = SentenceDataView(np.array(self.X_list.study_ids), self.vectorizer.fit_transform(self.X_list.data))
        self.y = {domain: SentenceDataView(np.array(y_list[domain].study_ids), np.array(y_list[domain].data)) for domain in test_domains}


    def save_data(self, filename):
        out = (self.vectorizer, self.X, self.y)
        with open(filename, 'wb') as f:
            pickle.dump(out, f)
            

    def load_data(self, filename):
        with open(filename, 'rb') as f:
            inp = pickle.load(f)
            
        self.vectorizer, self.X, self.y = inp
            
    def save_text(self, filename):
        """
        saves the original text of all PDFs, to debugging and looking at predicted text from corpus
        NB this is a large file
        """
        with open(filename, 'wb') as f:
            pickle.dump(self.X_list, f)

    def load_text(self, filename):
        """
        loads the original text of all PDFs, to debugging and looking at predicted text from corpus
        NB this is a large file
        """
        with open(filename, 'rb') as f:
            self.X_list = pickle.load(f)
            
        
    def len_domain(self, domain=0):
        """
        returns number of *studies* (not sentences)
        per domain
        """
        # if the index is passed, convert to the string
        if isinstance(domain, int):
            domain = ALL_DOMAINS[domain]

        return len(np.unique(self.y[domain].study_ids))

    def get_all_domains(self):
        return self.y.keys()


    def X_get_sentence(self, select_sent_id, domain=0):
        # if the index is passed, convert to the string
        if isinstance(domain, int):
            domain = ALL_DOMAINS[domain]

        y_study_ids = np.unique(self.y[domain].study_ids)

        X_filter = np.nonzero([X_study_id in y_study_ids for X_study_id in self.X.study_ids])[0]

        return self.X_list.data[X_filter[select_sent_id]]


    def X_domain_all(self, domain=0):
        """
        retrieve X data
        N.B. study_ids in the data are for internal use only
        externally, studies are 0 indexed and separate for each domain
        """
        # if the index is passed, convert to the string
        if isinstance(domain, int):
            domain = ALL_DOMAINS[domain]

        y_study_ids = np.unique(self.y[domain].study_ids)

        X_filter = np.nonzero([(X_study_id in y_study_ids) for X_study_id in self.X.study_ids])[0]

        return SentenceDataView(self.X.study_ids[X_filter], self.X.data[X_filter])

    def y_domain_all(self, domain=0):
        # if the index is passed, convert to the string
        if isinstance(domain, int):
            domain = ALL_DOMAINS[domain]

        return self.y[domain]


    def X_y_filtered(self, filter_ids, domain=0):

        if isinstance(domain, int):
            domain = ALL_DOMAINS[domain]

        X_all = self.X_domain_all(domain=domain)
        y_all = self.y[domain]

        # np.unique always returns ordered ids
        unique_study_ids = np.unique(y_all.study_ids)

        

        mapped_ids = [unique_study_ids[filter_id] for filter_id in filter_ids]

        X_filter_ids = np.nonzero([(X_study_id in mapped_ids) for X_study_id in X_all.study_ids])[0]
        # can probably remove the next line, ids should be the same for both at this stage
        y_filter_ids = np.nonzero([(y_study_id in mapped_ids) for y_study_id in y_all.study_ids])[0]

        
        X_filtered = SentenceDataView(X_all.study_ids[X_filter_ids], X_all.data[X_filter_ids])
        y_filtered = SentenceDataView(y_all.study_ids[y_filter_ids], y_all.data[y_filter_ids])

        return X_filtered, y_filtered
    

    def X_y_sampled(self, filter_ids, domain=0, negative_sample_ratio=10):
        """
        randomly sample negative examples
        (for when imbalance)
        N.B. negatives may be oversampled
        """

        X_filtered, y_filtered = self.X_y_filtered(filter_ids, domain)


        # find the positive and negative sentence ids
        positive_ids = np.nonzero(y_filtered.data==1)[0]
        negative_ids = np.nonzero(y_filtered.data==-1)[0]

        # sample ratio * no positive ids
        len_positive_ids = len(positive_ids)
        sample_size = negative_sample_ratio * len_positive_ids

        negative_sample_ids = np.random.choice(negative_ids, size=sample_size, replace=True) #replace=True is default, here for clarity

        full_sample_ids = np.append(positive_ids, negative_sample_ids)

        X_sampled = SentenceDataView(X_filtered.study_ids[full_sample_ids], X_filtered.data[full_sample_ids])
        y_sampled = SentenceDataView(y_filtered.study_ids[full_sample_ids], y_filtered.data[full_sample_ids])

        return X_sampled, y_sampled


class DocumentVectorizer(SentenceVectorizer):
    """
    for predicting the risk of bias
    as "HIGH", "LOW", or "UNKNOWN" for a document
    using a binary bag-of-words as features for each document
    """


    def generate_data(self, test_mode=False):

        # map_lbl = lambda lbl: {"YES":2, "NO":0, "UNKNOWN":1}[lbl]

        self.test_mode = test_mode
        if self.test_mode:
            print "WARNING - in test mode, using data sample only!!!"

        self.X_list = SentenceDataView([], [])
        y_list = defaultdict(lambda: SentenceDataView([], []))

        # self.vectorizer = CountVectorizer(max_features=5000)
        self.vectorizer = ModularCountVectorizer()
        q = QualityQuoteReader(quotes_only=False) # use studies with or without quotes

        for study_i, study in enumerate(q):

            domains_done_already = []

            self.X_list.study_ids.append(study_i)
            self.X_list.data.append(study.studypdf)

            
            for domain in study.cochrane["QUALITY"]:

                domain_title = domain["DOMAIN"]

                # for the moment if multiple ratings per study, just use the first
                # TODO (eventually) will have to do *per outcome*
                if domain_title in domains_done_already:
                    continue # skip to the next one

                domains_done_already.append(domain_title)

                pdf_tokens = study.studypdf
                quality_rating = domain["RATING"]

            
                y_list[domain_title].study_ids.append(study_i)
                y_list[domain_title].data.append(quality_rating)
            

        self.X = SentenceDataView(np.array(self.X_list.study_ids), self.vectorizer.fit_transform(self.X_list.data))

        # note restricted to CORE_DOMAINS here - no option given to expand since
        # 
        self.y = {domain: SentenceDataView(np.array(y_list[domain].study_ids), np.array(y_list[domain].data)) for domain in CORE_DOMAINS}

    


    def X_y_filtered_remove_unknowns(self, filter_ids, domain=0):

        X, y = self.X_y_filtered(filter_ids, domain=domain)

        yes_no_indices = np.nonzero((y.data != "UNKNOWN"))[0]

        X_filtered = SentenceDataView(X.study_ids[yes_no_indices], X.data[yes_no_indices])
        y_filtered = SentenceDataView(y.study_ids[yes_no_indices], y.data[yes_no_indices])

        return X_filtered, y_filtered




class SimpleHybridModel(SentenceVectorizer):
    """
    uses interaction of YES (low risk of bias)
    direct from Cochrane to start with
    (Uses actual rather than predicted risk of biases)
    """


    def X_domain_all(self, domain=0):
        """
        retrieve X data
        this version creates a new X matrix for each domain
        and caches the last one used
        (since this function may be called a lot)
        """

        # if the index is passed, convert to the string
        if isinstance(domain, int):
            domain = ALL_DOMAINS[domain]


        y_study_ids = np.unique(self.y[domain].study_ids)        
        X_filter = np.nonzero([(X_study_id in y_study_ids) for X_study_id in self.X_list.study_ids])[0]


        if self.X_domain_cached != domain:
            # if the domain isn't cached, need to make a new X

            # first get the sentences corresponding to the y domain vector
            X_list_filtered = []
            for i, sent in enumerate(self.X_list.data):
                if i in X_filter:
                    X_list_filtered.append(sent)

            
            # then create new interaction features where we have a judgement of 'LOW' risk only
            interaction_features = []
            for sent, judgement_is_yes in zip(X_list_filtered, self.X_interaction_features[domain]):
                if judgement_is_yes:
                    interaction_features.append(sent)
                else:
                    interaction_features.append("")

            # finally build and fit vectorizer covering both these feature sets
            self.vectorizer.builder_clear() # start with a new builder list
            self.vectorizer.builder_add_docs(X_list_filtered)
            self.vectorizer.builder_add_docs(interaction_features, prefix="LOW-RISK-")

            # then fit/transform the vectorizer
            self.X = SentenceDataView(np.array(self.y[domain].study_ids), self.vectorizer.builder_fit_transform())

            # and record which domain is in the cache now
            self.X_domain_cached = domain
        

        return self.X


    def generate_data(self, test_mode=False, restrict_to_core=False):


        self.test_mode = test_mode
        if self.test_mode:
            print "WARNING - in test mode, using data sample only"



        if restrict_to_core:
            test_domains = CORE_DOMAINS
        else:
            test_domains = ALL_DOMAINS


        # one feature matrix X
        self.X_list = SentenceDataView([], [])

        self.X_interaction_features = defaultdict(list) # indexed as per y

        y_list = defaultdict(lambda: SentenceDataView([], []))


        q = QualityQuoteReader()

        for study_i, study in enumerate(q):

            matcher = PDFMatcher()
            matcher.load_pdftext(study.studypdf)

            
            X_study = matcher.generate_X()
            self.X_list.data.extend(X_study)
            self.X_list.study_ids.extend([study_i] * len(X_study))

            domains_done_already = [] # for this particular study
            # (we're ignoring multiple quotes per domain at the moment and getting the first...)

            for domain in study.cochrane["QUALITY"]:

                matcher.load_quotes(domain["DESCRIPTION"])
                y_study = matcher.generate_y()

                if domain["DOMAIN"] in domains_done_already:
                    continue
                else:
                    domains_done_already.append(domain["DOMAIN"])
                    y_list[domain["DOMAIN"]].data.extend(y_study)
                    y_list[domain["DOMAIN"]].study_ids.extend([study_i] * len(y_study))

                    self.X_interaction_features[domain["DOMAIN"]].extend([(domain["RATING"]=="YES")] * len(y_study)) # add interaction features only for low risk of bias


                


                

            if self.test_mode and study_i == 75:
                break

        self.vectorizer = ModularCountVectorizer()

        


        
        self.X = None
        self.X_domain_cached = None
        self.y = {domain: SentenceDataView(np.array(y_list[domain].study_ids), np.array(y_list[domain].data)) for domain in test_domains}




class ModularCountVectorizer():
    """
    Similar to CountVectorizer from sklearn, but allows building up
    of feature matrix gradually, and adding prefixes to feature names
    (to identify interaction terms)
    """

    def __init__(self, *args, **kwargs):
        self.data = []
        self.vectorizer = DictVectorizer(*args, **kwargs)

    def _transform_X_to_dict(self, X, prefix=None):
        """
        makes a list of dicts from a document
        1. word tokenizes
        2. creates {word1:1, word2:1...} dicts
        (note all set to '1' since the DictVectorizer we use assumes all missing are 0)
        """
        return [self._dict_from_word_list(self._word_tokenize(document, prefix=prefix)) for document in X]

    def _word_tokenize(self, text, prefix=None):
        """
        simple word tokenizer using the same rule as sklearn
        punctuation is ignored, all 2 or more letter characters are a word
        """

        # print "text:"
        # print text
        # print "tokenized words"
        # print SIMPLE_WORD_TOKENIZER.findall(text)

        if prefix:
            return [prefix + word.lower() for word in SIMPLE_WORD_TOKENIZER.findall(text)]
        else:
            return [word.lower() for word in SIMPLE_WORD_TOKENIZER.findall(text)]


    def _dict_from_word_list(self, word_list):
        return {word: 1 for word in word_list}

    def _dictzip(self, dictlist1, dictlist2):
        """
        zips together two lists of dicts of the same length
        """
        # checks lists must be the same length
        if len(dictlist1) != len(dictlist2):
            raise IndexError("Unable to combine featuresets with different number of examples")

        output = []

        for dict1, dict2 in zip(dictlist1, dictlist2):
            output.append(dict(dict1.items() + dict2.items()))
            # note that this *overwrites* any duplicate keys with the key/value from dictlist2!!

        return output

    def fit(self, X, prefix=None):
        # X is a list of document strings
        # word tokenizes each one, then passes to a dict vectorizer
        dict_list = self._transform_X_to_dict(dict_list, prefix=prefix)
        return self.vectorizer.fit(X)

    def fit_transform(self, X, prefix=None):
        # X is a list of document strings
        # word tokenizes each one, then passes to a dict vectorizer
        dict_list = self._transform_X_to_dict(X, prefix=prefix)
        return self.vectorizer.fit_transform(dict_list)

    def get_feature_names(self):
        return self.vectorizer.get_feature_names()


    def builder_clear(self):
        self.builder = []
        self.builder_len = 0

    def builder_add_docs(self, X, prefix = None):
        if not self.builder:
            self.builder_len = len(X)
            self.builder = self._transform_X_to_dict(X)
        else:
            X_dicts = self._transform_X_to_dict(X, prefix=prefix)
            self.builder = self._dictzip(self.builder, X_dicts)

    def builder_fit_transform(self):
        return self.vectorizer.fit_transform(self.builder)

    def builder_fit(self):
        return self.vectorizer.fit(self.builder)   






class SamplingSGDClassifier():
    """
    SGDClassifier which samples negative examples according to the
    ratio negative_sample_ratio for imbalanced classes
    for binary classifier with -1 = False, and 1 = True
    """

    def __init__(self, *args, **kwargs):
        self.negative_sample_ratio = kwargs.pop("negative_sample_ratio") # remove this before calling the main function
        self.no_models = kwargs.pop("no_models") # remove this before calling the main function
        self.model_args = args
        self.model_kwargs = kwargs
        
        

    def fit(self, X, y):
        """
        fits k models (found in self.no_models), and saves all in a list
        """
        self.models = []

        
        for i in range(self.no_models):

            X_sampled, y_sampled = self.Xy_sample(X, y, self.negative_sample_ratio)



            # clf = SGDClassifier(*self.model_args, **self.model_kwargs)
            clf = SGDClassifier(**self.model_kwargs)
            clf.fit(X_sampled, y_sampled)
            self.models.append(clf)




    def predict(self, X):
        # returns list of predictions (which numpy interprets as matrix)
        # for predicted positive or negative
        y_pred_matrix = [(clf.predict(X)==1) for clf in self.models]

        # print '\n'.join([str(np.bincount((y+1)/2)) for y in y_pred_matrix])

        # mean across vectors = proportion of total votes
        proportion_of_votes = np.mean(y_pred_matrix,axis=0)

        # predict true if > 50% of the total votes
        y_preds = (proportion_of_votes >= 0.5)


        return y_preds*2-1 # change from True, False to 1, -1


    def Xy_sample(self, X, y, negative_sample_ratio):

        # find the positive and negative sentence ids
        positive_ids = np.nonzero(y==1)[0]
        negative_ids = np.nonzero(y==-1)[0]



        # sample ratio * no positive ids
        len_positive_ids = len(positive_ids)
        sample_size = negative_sample_ratio * len_positive_ids

        negative_sample_ids = np.random.choice(negative_ids, size=sample_size, replace=True) #may sample same sentence twice

        full_sample_ids = np.append(positive_ids, negative_sample_ids)


        X_sampled = X[full_sample_ids]
        y_sampled = y[full_sample_ids]

        return X_sampled, y_sampled



        





def demo(testfile="testdata/demo.pdf"):

    raw_text = PdfReader(testfile).get_text()
    text = unidecode(raw_text)
    text = re.sub('\n', ' ', text)
    sents = sent_tokenizer.tokenize(text)

    # print sents

    s = SentenceVectorizer()
    # s.generate_data(test_mode=False)
    # s.save_data('data/qualitydat.pck')
    s.load_data('data/qualitydat.pck')

    X_demo = s.vectorizer.transform(sents)

    for domain in s.get_all_domains():
        
        clf = SGDClassifier(loss="hinge", penalty="elasticnet", class_weight={1: 5, -1:1})

        # don't bother if fewer than 5 studies
        if s.len_domain(domain) < 5:
            print "Fewer than 5 studies in domain: %s --- skipping" % (domain,)
            continue

        all_X = s.X_domain_all(domain=domain)
        all_y = s.y_domain_all(domain=domain)

        clf.fit(all_X.data, all_y.data)

        y_preds = clf.predict(X_demo)
        pos_indices = np.nonzero(y_preds==1)[0]
        

        print
        print
        print "*********"
        print domain
        print "*********"
        print
        for i in pos_indices:
            print sents[i]

        











def document_prediction_test():

    print "Document level prediction"
    print "=" * 40
    print


    d = DocumentVectorizer()
    
    d.generate_data()
    d.save_data('data/quality_doc_data.pck')
    # d.load_data('data/quality_doc_data.pck')


    for test_domain in CORE_DOMAINS:
        print ("*"*40) + "\n\n" + test_domain + "\n\n" + ("*" * 40)
        
        no_studies = d.len_domain(test_domain)

        kf = KFold(no_studies, n_folds=5, shuffle=True)

        clf = SGDClassifier(loss="hinge", penalty="l2", alpha=.01)
        # removed from above
       
        all_X = d.X_domain_all(domain=test_domain)
        all_y = d.y_domain_all(domain=test_domain)

        

        metrics = []



        for fold_i, (train, test) in enumerate(kf):

            # X_train, y_train = d.X_y_filtered(np.array(train), domain=test_domain)
            X_train, y_train = d.X_y_filtered_remove_unknowns(np.array(train), domain=test_domain) #train removing unknowns, test using all
            X_test, y_test = d.X_y_filtered(np.array(test), domain=test_domain)

            print len(y_train.data), len(y_test.data)

            clf.fit(X_train.data, y_train.data)

            y_preds = clf.predict(X_test.data)


            fold_metric = np.array(sklearn.metrics.precision_recall_fscore_support(y_test.data, y_preds))

            metrics.append(fold_metric) # get the scores for positive instances

            # print "fold %d:\tprecision %.2f, recall %.2f, f-score %.2f" % (fold_i, fold_metric[0], fold_metric[1], fold_metric[2])

            print collections.Counter(y_test.data)
            print fold_metric
            

        # fit on all
        clf.fit(all_X.data, all_y.data)

        # if not sample and list_features:
            # not an obvious way to get best features for ensemble
        # print show_most_informative_features_ynu(d.vectorizer, clf)
        print show_most_informative_features_ynu(d.vectorizer, clf)
            

        # summary score

        # summary_metrics = np.mean(metrics, axis=0)
        # print "=" * 40
        # print "mean score:\tprecision %.2f, recall %.2f, f-score %.2f" % (summary_metrics[0], summary_metrics[1], summary_metrics[2])



def sentence_prediction_test(sample=True, negative_sample_ratio=50, no_models=10, class_weight={1: 1, -1:1}, list_features=False, hybrid=False):


    print "Sentence level prediction"
    print "=" * 40
    print
    if hybrid:
        print "HYBRID MODEL 1 - adding in word-judgement interaction features for all LOW risk papers"
    print "sampling=%s, class_weight=%s" % (str(sample), str(class_weight))
    if sample:
        print "negative_sample_ratio=%d, no_models=%d" % (negative_sample_ratio, no_models)
    print


    if hybrid:
        s = SimpleHybridModel()
    else:
        s = SentenceVectorizer()
    
    s.generate_data(test_mode=False)
    
    # s.save_data('data/qualitydat.pck')
    # s.save_text('data/qualitydat_text.pck')

    # s.load_data('data/qualitydat.pck')
    # s.load_text('data/qualitydat_text.pck')


    for test_domain in CORE_DOMAINS:
        print ("*"*40) + "\n\n" + test_domain + "\n\n" + ("*" * 40)
        

        no_studies = s.len_domain(test_domain)

        kf = KFold(no_studies, n_folds=5, shuffle=True)


        if sample:
            clf = SamplingSGDClassifier(loss="hinge", penalty="elasticnet", class_weight=class_weight, negative_sample_ratio=negative_sample_ratio, no_models=no_models)
        else:
            clf = SGDClassifier(loss="hinge", penalty="elasticnet", class_weight=class_weight)
        
        all_X = s.X_domain_all(domain=test_domain)
        all_y = s.y_domain_all(domain=test_domain)

        metrics = []

        for fold_i, (train, test) in enumerate(kf):

            X_train, y_train = s.X_y_filtered(np.array(train), domain=test_domain)
            X_test, y_test = s.X_y_filtered(np.array(test), domain=test_domain)

            clf.fit(X_train.data, y_train.data)

            y_preds = clf.predict(X_test.data)

            fold_metric = np.array(sklearn.metrics.precision_recall_fscore_support(y_test.data, y_preds))[:,1]

            metrics.append(fold_metric) # get the scores for positive instances

            print "fold %d:\tprecision %.2f, recall %.2f, f-score %.2f" % (fold_i, fold_metric[0], fold_metric[1], fold_metric[2])
            

            if not sample and list_features:
                # not an obvious way to get best features for ensemble
                print show_most_informative_features(s.vectorizer, clf)
            

        # summary score

        summary_metrics = np.mean(metrics, axis=0)
        print "=" * 40
        print "mean score:\tprecision %.2f, recall %.2f, f-score %.2f" % (summary_metrics[0], summary_metrics[1], summary_metrics[2])




def main():
    q = QualityQuoteReader()

    for study in q:

        sm = difflib.SequenceMatcher(None, autojunk=False)

        sm.set_seq2(study.studypdf)
        pdf_end_i = len(study.studypdf)

        for domain in study.cochrane["QUALITY"]:
            


            for quote_part in domain["DESCRIPTION"]:

                

                

                quote_end_i = len(quote_part)

                if not quote_end_i:
                    continue

                sm.set_seq1(quote_part)

                longest_match = sm.find_longest_match(0, quote_end_i, 0, pdf_end_i)

                proportion_matched = (100 * float(longest_match.size)) / float(quote_end_i)


                print "matched %.2f" % (proportion_matched, )
                if longest_match.size < MIN_CHAR_MATCH:
                    print "NOT BIG ENOUGH MATCH - SKIP!"

                print
                print "Cochrane quote:"
                print quote_part
                print
                print "PDF part"
                print study.studypdf[longest_match.b-100: longest_match.b] + "..."
                print study.studypdf[longest_match.b: longest_match.b+longest_match.size]
                print "..." + study.studypdf[longest_match.b+longest_match.size: longest_match.b+100+longest_match.size] 
                print
                print

                
            # pprint(output)

    






if __name__ == '__main__':
    # sentence_prediction_test(hybrid=True)
    sentence_prediction_test(sample=False, negative_sample_ratio=5, no_models=200, list_features=False, class_weight={1:5, -1:1}, hybrid=True)
    # sentence_prediction_test(sample=False, class_weight={1:1.5, -1:1}, list_features=False)
    # demo('testdata/demo3.pdf')
    # document_prediction_test()
