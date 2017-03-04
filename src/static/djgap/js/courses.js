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
    
    var userID = getUserID();
    console.log(userID);
    
    var username = userID; // get name froms server
    var courses = ["CSCA08", "CSCA48", "MATB41", "CSCB63"]; // get courses in a list from server
    
    $("h1").append(username); 
    
    for (var i = 0; i < courses.length; i++) {
        var btn = "<li><a href=\"dashboard.html?course=" + courses[i] + "&id=" + userID + "\">" + "<button class=\"cbtn\"><span>" + courses[i] + "</span></button></a></li>"
        $("#list").append(btn);
    }
    
    // add the create new course button
    var btn = "<li><a href=\"dashboard.html?course=\"><button class=\"cbtn crCourse\"><span>+ Create Course</span></button></a></li>"
    $("#list").append(btn);
    
    $(".logout").click(function() {
        setTimeout(function(){window.location.href = "index.html"});
    });
});

function getUserID() {
    
    var params = document.URL.split("?");
    var userID = "";
    if (params.length > 1) {
        var userID = params[1].split("=")[1];
    }
    
    return userID;
}
