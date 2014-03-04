function loadPdf(pdfURI) {
    var pdf = PDFJS.getDocument(pdfURI);
    PDFJS.disableWorker = true; // Must be disabled, for now
    pdf.then(renderPdf).then(annotate);
}


function drawAnnotations(annotations) {
    // For the sentence (/node) level
    $.each(annotations.annotations, function(idx, ann) {
        var $page = $("#pageContainer-" + ann.page);
        var classes = ["annotated"];
        $.each(ann.labels, function(label, value) {
            var className = label.replace(/ /g, "-").toLowerCase() + "_" + value;
            classes.push(className);
        });
        $.each(ann.nodes, function(idx, node) {
            
            $page.find(".textLayer div:eq(" + (node + 1) + ")").addClass(classes.join(" "));
            // IM: changed to :eq() rather than :nth-child since the latter
            // counts *any* element in the indexing regardless of whether a div, then returns next div
            // whereas :eq() should behave as expected
            // also added 1 to node, since jQuery indexes from 1 for selection, our server code from 0

        });
    });

    // For the document level
    var $results = $("#results");
    $results.empty();
    $results.append("<h3></h3>");
    $results.append("<table></table>");
    $results.find("h3").text(annotations.title);

    var $resultsTable = $results.find("table").addClass("pure-table");

    var risks = [{name: "high", icon: '-'}, {name: "unknown", icon: '?'}, {name: "low", icon: "+"}];
    $.each(annotations.document, function(key, value) {
        var risk = risks[value + 1];
        var klass = key.replace(/ /g, "-").toLowerCase() + "_1";
        $resultsTable.append('<tr class="'+ klass + '"><td>' + key + ' </td><td class="' + risk.name + '">' + risk.icon + '</td></tr>');
    });

}

function annotate(textContents) {
    // Look here if you are missing something, I'm shifting the array by one because it was null
    textContents.shift();
    $.ajax({
        url: '/annotate',
        type: 'POST',
        data: JSON.stringify({pages: textContents}),
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        async: true,
        success: drawAnnotations
    });
}

function renderPdf(pdf) {

    var textContentPromises = [];
        for(var pageNr = 1; pageNr < pdf.numPages; ++pageNr) {
                textContentPromises[pageNr] = pdf.getPage(pageNr).then(renderPage);
            }

    return Q.all(textContentPromises);

}

function renderPage(page) {
    var container = document.getElementById("main");

    var PADDING_AND_MARGIN = 175;
    var pageWidthScale = (container.clientWidth + PADDING_AND_MARGIN) / page.view[3];

    var pageIndex = page.pageInfo.pageIndex;
    var viewport = page.getViewport(pageWidthScale);

    var $canvas = $("<canvas></canvas>");

    var $container = $("<div></div>");
    $container.attr("id", "pageContainer-" + pageIndex).addClass("page");

    // Set the canvas height and width to the height and width of the viewport
    var canvas = $canvas.get(0);
    var context = canvas.getContext("2d");

    //Checks scaling on the context if we are on a HiDPI display
    var outputScale = getOutputScale(context);


    if (outputScale.scaled) {
        // scale up canvas (since the -transform reduces overall dimensions and not just the contents)
        canvas.height = viewport.height * outputScale.sy;
        canvas.width = viewport.width * outputScale.sx;
    } else {
        canvas.height = viewport.height;
        canvas.width = viewport.width;
    }

    // Append the canvas to the pdf container div
    var $pdfContainer = $("#pdfContainer");
    $pdfContainer.css("height", canvas.height + "px").css("width", canvas.width + "px");
    $container.append($canvas);
    $pdfContainer.append($container);

    var containerOffset = $container.offset();
    var $textLayerDiv = $("<div />")
            .addClass("textLayer")
            .css("height", canvas.height + "px")
            .css("width", canvas.width + "px")
            .offset({
                top: containerOffset.top,
                left: containerOffset.left
            });

    if (outputScale.scaled) {

        var cssScale = 'scale(' + (1 / outputScale.sx) + ', ' +
                (1 / outputScale.sy) + ')';
        CustomStyle.setProp('transform', canvas, cssScale);
        CustomStyle.setProp('transformOrigin', canvas, '0% 0%');

        if ($textLayerDiv.get(0)) {
            CustomStyle.setProp('transform', $textLayerDiv.get(0), cssScale);
            CustomStyle.setProp('transformOrigin', $textLayerDiv.get(0), '0% 0%');
        }
    }

    context._scaleX = outputScale.sx;
    context._scaleY = outputScale.sy;
    if (outputScale.scaled) {
        context.scale(outputScale.sx, outputScale.sy);
    }

    $container.append($textLayerDiv);
    var deferredTextContent = Q.defer();

    page.getTextContent().then(function (textContent) {
        var textLayer = new TextLayerBuilder({
            textLayerDiv: $textLayerDiv.get(0),
            pageIndex: pageIndex
        });

        textLayer.setTextContent(textContent);
        var renderContext = {
            canvasContext: context,
            viewport: viewport,
            textLayer: textLayer
        };

        // from http://stackoverflow.com/questions/12693207/how-to-know-if-pdf-js-has-finished-rendering
        var pageRendering = page.render(renderContext);
        var completeCallback = pageRendering.internalRenderTask.callback;
        pageRendering.internalRenderTask.callback = function (error) {
            completeCallback.call(this, error);
            deferredTextContent.resolve(textContent);
        };
    });

    return deferredTextContent.promise;
}

// from http://stackoverflow.com/questions/12092633/pdf-js-rendering-a-pdf-file-using-a-base64-file-source-instead-of-url
var BASE64_MARKER = ';base64,';
function convertDataURIToBinary(dataURI) {
  var base64Index = dataURI.indexOf(BASE64_MARKER) + BASE64_MARKER.length;
  var base64 = dataURI.substring(base64Index);
  var raw = window.atob(base64);
  var rawLength = raw.length;
  var array = new Uint8Array(new ArrayBuffer(rawLength));

  for(var i = 0; i < rawLength; i++) {
    array[i] = raw.charCodeAt(i);
  }
  return array;
}

$(document).ready(function() {

    var fileInput = document.getElementById('fileInput');
    var submit = document.getElementById('upload');

    submit.addEventListener('click', function(e) {
        var file = fileInput.files[0];
        var textType = /application\/(x-)?pdf|text\/pdf/;
        if (file.type.match(textType)) {
            var reader = new FileReader();

            reader.onload = function(e) {
                document.getElementById('pdfContainer').innerHTML = ""; // clear the container
                loadPdf(convertDataURIToBinary(reader.result));
            };

            reader.readAsDataURL(file);
        } else {
            alert("File not supported! Probably not a PDF");
        }
    });
});