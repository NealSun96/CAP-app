
$(document).ready(function() {
$("#submit").click(function() {
    console.log("function entered");
    var username = document.forms["login"]["username"].value;
    var password = document.forms["login"]["password"].value;
    var encodedString = btoa(username + ":" + password)
    var endPoint = "http://71133ed0.ngrok.io/api/v1/login/"
    console.log("finished initialization");
    $.ajax({
        type: "GET",
        url: endPoint,
        data: {},
        success: function(data){
            console.log("success");
            var auth = username + ":" + data.objects[0].api_key;
            setTimeout(function() {window.location.href="courses/" + encodedString;});
        },
        error: function(data){
            console.log(data);

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