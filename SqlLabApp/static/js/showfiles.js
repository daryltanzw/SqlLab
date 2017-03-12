var selDiv = "";

document.addEventListener("DOMContentLoaded", init, false);

function init() {
    $("#upload-file1").click(function() {
        document.querySelector('#files').addEventListener('change', handleFileSelect, false);
        selDiv = document.querySelector("#selectedQuestionFiles");
    });

    $("#upload-file2").click(function() {
        document.querySelector('#files').addEventListener('change', handleFileSelect, false);
        selDiv = document.querySelector("#selectedAnswerFiles");
    });

    $("#upload-file3").click(function() {
        document.querySelector('#multi-files').addEventListener('change', handleFileSelect, false);
        selDiv = document.querySelector("#selectedDataFiles");
    });

}

function handleFileSelect(e) {

    if (!e.target.files) return;

    selDiv.innerHTML = "";

    var files = e.target.files;
    for (var i = 0; i < files.length; i++) {
        var f = files[i];

        selDiv.innerHTML += f.name + "<br/>";

    }
}