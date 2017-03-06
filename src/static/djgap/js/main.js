
$(document).ready(function() {
    
    var key = 'auth';
    
    var loginAuth = localStorage.getItem(key);
    if (loginAuth != "") {
        setTimeout(function() {window.location.href=baseUrl+"/courses/" + loginAuth;});
    }
    
    $('.invalid').click(function(){clearError();});
    
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
                if ($("#signedIn").prop('checked')) {
                    localStorage.setItem(key,btoa(auth));
                }
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
    
    $("#login #register").click(function(){
        clearError();
        $('#login').addClass("hidden");
        $('#registerForm').removeClass("hidden");
    });
    
    $("#registerForm #regBtn").click(function(){
        registerUser();
        $('#login').removeClass("hidden");
        $('#registerForm').addClass("hidden");
    });
    
    $("#cancelReg").click(function(){
        $('#login').removeClass("hidden");
        $('#registerForm').addClass("hidden");
    });

});


function registerUser() {
    
    // do register stuff
}

function clearError() {
    $('.invalid').fadeOut(100);
    
}

function error() {
    $('.invalid').fadeIn(400);
}

function getUrl() {
    return location.protocol + "//" + location.hostname + (location.port && ":" + location.port);
}

