$(document).ready(function(){
    $('.invalid').click(function(){
        $('.invalid').fadeOut(100); 
    });
});

function validate()
{
    // call error if login fails
    // error();
    var username = document.forms["login"]["username"].value;
    var password = document.forms["login"]["password"].value;
    
    setTimeout(function() {window.location.href="courses.html?id=101";});
}

function error() {
    $('.invalid').fadeIn(400);
}
