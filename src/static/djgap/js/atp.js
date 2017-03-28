var baseUrl = getUrl();
var auth = atob(getAuth());

var reader  = new FileReader();


$(document).ready(function(){
    populateTeachers();

    $("#upload").click(function(){
        upload();
    });
});

function upload() {
    var file = $('#teacherFile').prop('files')[0];
    reader.onload = receivedText;
    reader.readAsDataURL(file);
    function receivedText() {
        var endPoint = baseUrl + "/api/v1/employee_title/add_titles/";
        $.ajax({
            type: "POST",
            url: endPoint,
            data: JSON.stringify({
                file: reader.result
            }),
            dataType: "json",
            success: function(data){
                setTimeout(function(){window.location.href = document.URL;});

            },
            error: function(data){
                $("#error").append(data.responseText+"<br>");
            },
            beforeSend: function(xhr){
                xhr.setRequestHeader("Authorization", "Apikey " + auth);
                xhr.setRequestHeader("Content-Type", "application/json");
            },
            complete: function(){
            }
        })
    }
}


function populateTeachers() {
    var endPoint = baseUrl + "/api/v1/employee_title/get_titles/";
    $.ajax({
        type: "GET",
        url: endPoint,
        data: {},
        success: function(data){
            for (var i = 0; i < data.objects.length; i++) {
                $("#titleLabel").append(data.objects[i]+"<br>");
            }
        },
        error: function(data){
            $("#error").append(data.responseText+"<br>");
        },
        beforeSend: function(xhr){
            xhr.setRequestHeader("Authorization", "Apikey " + auth);
            xhr.setRequestHeader("Content-Type", "application/json");
        },
        complete: function(){
        }
    })
}

function getUrl() {
    return location.protocol + "//" + location.hostname + (location.port && ":" + location.port);
}

function getAuth() {
    var params = document.URL.split("/");
    return params[params.length - 1];
}