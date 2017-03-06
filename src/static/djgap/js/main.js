
$(document).ready(function() {
$("#submit").click(function() {
    var username = document.forms["login"]["username"].value;
    var password = document.forms["login"]["password"].value;
    var encodedString = btoa(username + ":" + password)
    var baseUrl = getUrl();
    var endPoint = baseUrl + "/api/v1/login/";
    $.ajax({
        type: "GET",
        url: endPoint,
        data: {},
        success: function(data){
            var auth = username + ":" + data.objects[0].api_key;
            setTimeout(function() {window.location.href=baseUrl+"/courses/" + btoa(auth);});
        },
        error: function(data){
            error();
        },
        beforeSend: function(xhr){
            xhr.setRequestHeader("Authorization", "Basic " + encodedString);
            xhr.setRequestHeader("Content-Type", "application/json");
        },
        complete: function(){
        }
    })
    $('#login').submit();
});

});


function error() {
    $('.invalid').fadeIn(400);
}

function getUrl() {
    return location.protocol + "//" + location.hostname + (location.port && ":" + location.port);
}

