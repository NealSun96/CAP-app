var baseUrl = getUrl();

$(document).ready(function() {
    var key = 'auth';

    var loginAuth = localStorage.getItem(key);
    if (loginAuth != null) {
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
                if (username == "admin") setTimeout(function() {window.location.href=baseUrl+"/register_teacher/" + btoa(auth);});
                else setTimeout(function() {window.location.href=baseUrl+"/courses/" + btoa(auth);});
            },
            error: function(data){
                error("错误的用户名或密码");
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
        center();
        
    });
    
    $("#registerForm #regBtn").click(function(){
        clearError();
        registerUser();
        center();
    });
    
    $("#cancelReg").click(function(){
        clearError();
        $('#login').removeClass("hidden");
        $('#registerForm').addClass("hidden");
        center();
    });
    
    center();

});

function center() {
    $(function() {
        $('#container').css({
            'position' : 'absolute',
            'left' : '50%',
            'top' : '50%',
            'margin-left' : function() {return -$(this).outerWidth()/2},
            'margin-top' : function() {return -$(this).outerHeight()/2}
        });
    });
}

function registerUser() {
    var firstName = document.forms["registerForm"]["firstName"].value;
    var lastName = document.forms["registerForm"]["lastName"].value;
    var username = document.forms["registerForm"]["regUsername"].value;
    var password = document.forms["registerForm"]["regPassword"].value;
    var endPoint = baseUrl + "/api/v1/register/?format=json";
    var data = {
            "first_name": firstName,
            "last_name": lastName,
            "username": username,
            "password": password
        }
    $.ajax({
        type: "POST",
        url: endPoint,
        data: JSON.stringify(data),
        dataType: "html",
        success: function(data){
            $('#firstName').val("");
            $('#lastName').val("");
            $('#regUsername').val("");
            $('#regPassword').val("");
            $('#login').removeClass("hidden");
            $('#registerForm').addClass("hidden");
        },
        error: function(data){
            error(JSON.parse(data.responseText).error);
        },
        beforeSend: function(xhr){
            xhr.setRequestHeader("Content-Type", "application/json");
        },
        complete: function(){
        }
    })
}

function clearError() {
    $('.invalid').fadeOut(100);
    
}

function error(message) {
    $('.invalid').text(message);
    $('.invalid').fadeIn(400);
}

function getUrl() {
    return location.protocol + "//" + location.hostname + (location.port && ":" + location.port);
}

