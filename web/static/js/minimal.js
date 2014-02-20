function loadPdf(pdfURI) {
    var pdf = PDFJS.getDocument(pdfURI);
    PDFJS.disableWorker = true; // Must be disabled
    pdf.then(renderPdf);
}

function annotationRPC(textContents) {
    console.log(textContents);
    $.ajax({
        url: '/annotate',
        type: 'POST',
        data: JSON.stringify(textContents),
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        async: true,
        success: function(annotations) {
            // here be dragons!
            console.log(annotations);

        }
    });
}

function renderPdf(pdf) {
    var textContentPromises = [];
    for(var pageNr = 1; pageNr < pdf.numPages; ++pageNr) {
        textContentPromises[pageNr] = pdf.getPage(pageNr).then(renderPage);
    }

    Q.all(textContentPromises).then(function(textContents) { // All pages have finished rendering
        annotationRPC(textContents); // This calls python and asynchronously /should/ return the annotations.
    });
}

function renderPage(page) {
    var scale = 1.5;
    var pageIndex = page.pageInfo.pageIndex;
    var viewport = page.getViewport(scale);
    var $canvas = $("<canvas></canvas>");

    var $container = $("<div></div>");
    $container.attr("id", "pageContainer-" + pageIndex).addClass("page");

    //Set the canvas height and width to the height and width of the viewport
    var canvas = $canvas.get(0);
    var context = canvas.getContext("2d");
    canvas.height = viewport.height;
    canvas.width = viewport.width;

    //Append the canvas to the pdf container div
    var $pdfContainer = $("#pdfContainer");
    $pdfContainer.css("height", canvas.height + "px").css("width", canvas.width + "px");
    $container.append($canvas);
    $pdfContainer.append($container);

    var containerOffset = $container.offset();
    var $textLayerDiv = $("<div />")
            .addClass("textLayer")
            .css("height", viewport.height + "px")
            .css("width", viewport.width + "px")
            .offset({
                top: containerOffset.top,
                left: containerOffset.left
            });

    //The following few lines of code set up scaling on the context if we are on a HiDPI display
    var outputScale = getOutputScale(context);
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
                document.getElementById('pdfContainer').innerHTML = "";
                loadPdf(convertDataURIToBinary(reader.result));
            };

            reader.readAsDataURL(file);
        } else {
            alert("File not supported! Probably not a PDF");
        }
    });
});