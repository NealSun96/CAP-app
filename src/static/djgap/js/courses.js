$(document).ready(function() {
    
    // center div
    $(function() {
        $('#content').css({
            'position' : 'absolute',
            'left' : '50%',
            'top' : '50%',
            'margin-left' : function() {return -$(this).outerWidth()/2},
            'margin-top' : function() {return -$(this).outerHeight()/2}
        });
    });
    
    var auth = getAuth();
    var courses = [];
    var baseUrl = getUrl();
    var endPoint = baseUrl + "/api/v1/course/"
    $.ajax({
        type: "GET",
        url: endPoint,
        data: {},
        success: function(data){
            for (var i = 0; i < data.objects.length; i++) {
                var btn = "<li><a href=\"" + baseUrl + "/dashboard/" + data.objects[i].id + "\">" + "<button class=\"cbtn\"><span>" + data.objects[i].course_name + "</span></button></a></li>"
                $("#list").append(btn);
            }

            // add the create new course button
            var btn = "<li><a href=\"" + baseUrl + "/dashboard\"><button class=\"cbtn crCourse\"><span>新建课程</span></button></a></li>"
            $("#list").append(btn);
        },
        error: function(data){
            error();
        },
        beforeSend: function(xhr){
            xhr.setRequestHeader("Authorization", "Apikey " + auth);
            xhr.setRequestHeader("Content-Type", "application/json");
        },
        complete: function(){
        }
    })
    
    $(".logout").click(function() {
        setTimeout(function(){window.location.href = baseUrl + "/index.html"});
    });
});

function getAuth() {
    var params = document.URL.split("/");
    return atob(params[params.length - 1]);
}

function getUrl() {
    return location.protocol + "//" + location.hostname + (location.port && ":" + location.port);
}
