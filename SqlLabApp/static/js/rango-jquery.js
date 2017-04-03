$(document).ready( function() {

    $("#execute-select-query-btn").click( function(event) {
        event.preventDefault();

        var query = $("#query_area").val();
//        var testid = $(this).attr("data-tid");
        $.ajax({
            url: window.location.href + 'execute_query/',
            type: "GET",
            data: {query : query },
            success : function(json) {
                         console.log(json);
                         alert(json['result']);
                       },
            error : function() {
                    console.log("ajax fail")
                    alert("sighs")
               }
        });
        });});

