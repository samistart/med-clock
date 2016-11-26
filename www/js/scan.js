
var CANVAS_SELECTOR = "#video";
var decoder;

function resultFn( result ) {
    window.location = "/www/html/edit.html?id=" + result.code;
}

function initScanner() {
    decoder = new WebCodeCamJS( CANVAS_SELECTOR );
    $.extend( decoder.options, {
        resultFunction : resultFn,
        decoderWorker : "/www/js/DecoderWorker.js",
        beep : false
    });
    decoder.init();
    decoder.play();
}

$(document).ready(function() {
    initScanner();
});
