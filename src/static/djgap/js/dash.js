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
    
    var userID = getUserID();
    var course = getCourse();
    
    refresh(userID, course);
    
    $("#refresh").click(function(){setTimeout(function(){window.location.href = document.URL;});});
    
    $("#logout").click(function(){
       $("#logout").animate(function() {
           $("#logout").css("background-color:#4ECDC4;");
       });
       setTimeout(function(){window.location.href = "index.html"}); 
    }); 

    $(".menuItem").click(function(){
        if (!$(".menuItem").hasClass('.error')){
            $(".menuItem").removeClass("menuItemActive");
            $(".data").removeClass("active");
            var id = $(this).attr('id');
            $("#data"+id).addClass("active");
            $(this).addClass("menuItemActive");
        }
    });
    
    $("#courseSave").click(function(){
        updateCourseInfo();
        refresh(userID, course);
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
    return false;
}

function updatePlan() {
    return false;
}

function refresh(userID, course) {
    
    console.log(userID);
    
    var username = userID.toString(); // get name froms server using userID
    
    $("#name").text("Hello! " + username);    
    
    var courseName = "SOME COURSE NAME";
    var courseDept = "SOME DEPARTMENT";
    var courseSem = "WINTER 2017";
    var coursePreReq = "AAA123, BBB234";
    var courseIns = username;
    var courseNumStuds = 100;
    var courseAvg = "42.0";
    
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
    var actionPlan = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.";
    $(".actPlan").text(actionPlan);
    
    // dummy knowledge test
    populateTest();
    
    
    // edit course fields ===============================================
    // ==================================================================
    
    $(".courseName").val(courseName);
    $(".courseCode").val(course);
    $(".courseDept").val(courseDept);
    $(".courseSem").val(courseSem);
    $(".coursePreReq").val(coursePreReq);
    $(".courseIns").val(courseIns);
    $(".courseNumStuds").val(courseNumStuds);
    $(".courseAvg").val(courseAvg);
    
    $(".inpTitle").attr('size', $(".inpTitle").val().length);
    
    // edit action plan =================================================
    // ===================================================================
    $("#actionPlanEdit").val(actionPlan);
    $("#actionPlanEdit").css({"-webkit-box-sizing":"border-box", "-moz-box-sizing": "border-box", "box-sizing": "border-box"});
    
    
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

function populateTest() {
    
    
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