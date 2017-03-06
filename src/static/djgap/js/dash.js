$(document).ready(function(){
    
    
    
    // disable zooming in and zoomign out
    $(document).keydown(function(event) {
    if (event.ctrlKey==true && (event.which == '61' || event.which == '107' || event.which == '173' || event.which == '109'  || event.which == '187'  || event.which == '189'  ) ) {
        event.preventDefault();
     }
        // 107 Num Key  +
        // 109 Num Key  -
        // 173 Min Key  hyphen/underscor Hey
        // 61 Plus key  +/= key
    });

    $(window).bind('mousewheel DOMMouseScroll', function (event) {
       if (event.ctrlKey == true) {
       event.preventDefault();
       }
    });
    
    var newCourse = isNewCourse();
    var userID = getUserID();
    var course = getCourse();
    
    if (!newCourse) {
        refresh(userID, course);
    }
    
    $("#refresh").click(function(){setTimeout(function(){window.location.href = document.URL;});});
    
    $("#logout").click(function(){
       $("#logout").animate(function() {
           $("#logout").css("background-color:#4ECDC4;");
       });
       setTimeout(function(){window.location.href = "courses.html?id="+userID}); 
    }); 
    
    
    if (newCourse) {
        console.log("hellolololololo");
        $("#1 span").text("NEW COURSE");
        $("#2").addClass("blocked");
        $("#3").addClass("blocked");
        $("#4").addClass("blocked");
        $("#5").addClass("blocked");
    } else {
        $(".menuItem").click(function(){
            if (!$(".menuItem").hasClass('.error')){
                $(".menuItem").removeClass("menuItemActive");
                $(".data").removeClass("active");
                var id = $(this).attr('id');
                $("#data"+id).addClass("active");
                $(this).addClass("menuItemActive");
            }
        });

    }
    
    $('.startTime').each(function() {
        
        $(this).timepicker({});
    });
    
    $("#courseSave").click(function(){
        
        if (!newCourse) {
            updateCourseInfo();
            refresh(userID, course);
        } else {
            course = $(".courseName").val();
            setTimeout(function(){window.location.href = document.URL.split("?")[0]+"?id="+userID+"&course="+course;});
        }
        // example use of error bar
        error("ERROR SAVING COURSE DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA ");
    });
    
    $("#planSave").click(function(){
        updatePlan();
        refresh(userID, course);
    });
    
    $("#testUpload").click(function(){
        uploadTest();
        refresh(userID, course);
    });
    
    $("#enroll").click(function(){
        enroll();
        refresh(userID, course);;
    });
    
    $('#errorItem').click(function(){

        $('#errorItem').fadeOut(100);
    });
    
    
});

function enroll() {
    return false;
}

function updateCourseInfo() {
    return false;
}

function uploadTest() {
    
    // questions are organized by id ex: q1, q2
    $("#q1 .question").val("THIS IS HOW TO SET A QUESTION???");
    // get the answer from database
    var answer = 2;
    // so the answer is option 2
    if ($("#q1 .option2").prop('checked')) {
        console.log("correct");
    } else {
        console.log("incorrect");
    }
    // to set the answer for q2 option2
    $("#q1 .opt2").val("NEW OPTION")
    
    return false;
}

function populateTest() {
    
    
}

function populateActionPlan() {
    
    
}

function updatePlan() {
    return false;
}

function refresh(userID, course) {
    
    console.log(userID);
    
    var username = userID.toString(); // get name froms server using userID
    
    $("#name").text("Hello! " + username);    
    
    var courseName = course;
    var startTime = "9";
    var courseIns = username;
    
    // dummy values
//    $(".course").append(course);
//    $(".cName").append(courseName);
//    $(".depart").append(courseDept);
//    $(".cSemester").append(courseSem);
//    $(".preReq").append(coursePreReq);
//    $(".instructor").append(courseIns);
//    $(".numStudents").append(courseNumStuds);
//    $(".cAvg").append(courseAvg);
        
        
    
    // dummy action plan
    populateActionPlan();
    
    // dummy knowledge test
    populateTest();
    
    
    // edit course fields ===============================================
    // ==================================================================
    
    $(".courseName").val(courseName);
    $(".startTime").val(startTime);
    $(".courseIns").val(courseIns);
    
    $(".inpTitle").attr('size', $(".inpTitle").val().length);    
    
}

function getUserID() {
    
    var params = document.URL.split("?");
    var userID = "";
    if (params.length > 1) {
        var conds = params[1].split("&");
        for (var i = 0; i < conds.length; i++) {
            var data = conds[i].split("=");
            if (data[0] === "id") {
                userID = data[1];
            }
        }
    }
    
    return userID;
}

function isNewCourse() {
    
    var params = document.URL.split("?");
    var isNewCourse = false;
    if (params.length > 1) {
        var conds = params[1].split("&");
        for (var i = 0; i < conds.length; i++) {
            var data = conds[i].split("=");
            if (data[0] === "new") {
                isNewCourse = true;
            }
        }
    }
    
    return isNewCourse;
}

function getCourse() {
    
    var params = document.URL.split("?");
    var course = "";
    if (params.length > 1) {
        var conds = params[1].split("&");
        for (var i = 0; i < conds.length; i++) {
            var data = conds[i].split("=");
            if (data[0] === "course") {
                course = data[1];
            }
        }
    }
    
    return course;
}

function error(message) {
    $('#errorItem span').text(message);
    $('#errorItem').fadeIn(500);
}

function exampleListToElement() {
    // list of sutend name I want to add to a predefined <ol> within dashboard.html
    var dummyStudents = ["Niesha Newbill","Analisa Hugo","Oralee Massingale","Setsuko Kotter","Patrica Sansone","Alice Leyba","Erica Donlan","Idell Callaway","Shoshana Killinger","TashaKaylor","Luella Pearson","Ricki Siegel","Heidy Jarrard","Irena Range","Brigette Perrin","Lawrence Caskey","Roberto Mcdaniel","Vaughn Tessier","ChinaColwell","Meda Rainville","Kellye Dollar","Wilfred Derosier","Robyn Uyehara","Niesha Newbill","Analisa Hugo","Oralee Massingale","Setsuko Kotter","Patrica Sansone","Alice Leyba","Erica Donlan","Idell Callaway","Shoshana Killinger","TashaKaylor","Luella Pearson","Ricki Siegel","Heidy Jarrard","Irena Range","Brigette Perrin","Lawrence Caskey","Roberto Mcdaniel","Vaughn Tessier","ChinaColwell","Meda Rainville","Kellye Dollar","Wilfred Derosier","Robyn Uyehara","Niesha Newbill","Analisa Hugo","Oralee Massingale","Setsuko Kotter","Patrica Sansone","Alice Leyba","Erica Donlan","Idell Callaway","Shoshana Killinger","TashaKaylor","Luella Pearson","Ricki Siegel","Heidy Jarrard","Irena Range","Brigette Perrin","Lawrence Caskey","Roberto Mcdaniel","Vaughn Tessier","ChinaColwell","Meda Rainville","Kellye Dollar","Wilfred Derosier","Robyn Uyehara","Niesha Newbill","Analisa Hugo","Oralee Massingale","Setsuko Kotter","Patrica Sansone","Alice Leyba","Erica Donlan","Idell Callaway","Shoshana Killinger","TashaKaylor","Luella Pearson","Ricki Siegel","Heidy Jarrard","Irena Range","Brigette Perrin","Lawrence Caskey","Roberto Mcdaniel","Vaughn Tessier","ChinaColwell","Meda Rainville","Kellye Dollar","Wilfred Derosier","Robyn Uyehara","Niesha Newbill","Analisa Hugo","Oralee Massingale","Setsuko Kotter","Patrica Sansone","Alice Leyba","Erica Donlan","Idell Callaway","Shoshana Killinger","TashaKaylor","Luella Pearson","Ricki Siegel","Heidy Jarrard","Irena Range","Brigette Perrin","Lawrence Caskey","Roberto Mcdaniel","Vaughn Tessier","ChinaColwell","Meda Rainville","Kellye Dollar"];
    
    
    // first loop through the list
    for (var i = 0; i < dummyStudents.length; i++){
        // construct html tag for the current student with class='student'
        var tag = "<li class='student'>" + dummyStudents[i] + "</li>"
        // apend it to the the sturent list using its iD
        $("#studentList").append(tag);
        // append will add tag to the end of the student list
        // $("#studentList").html(tag) will replace the entire list with tag
    }
    
}