var baseUrl = getUrl();
var params = getAuthAndID();
var auth = params[0];
var id = params[1];

$(document).ready(function(){
    var new_course = id == "new_course";

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

    if (!new_course) {
        refresh();
    }
    
    $("#refresh").click(function(){setTimeout(function(){window.location.href = document.URL;});});
    
    $("#logout").click(function(){
       $("#logout").animate(function() {
           $("#logout").css("background-color:#4ECDC4;");
       });
       setTimeout(function(){window.location.href = base_url + "/courses/"+auth});
    }); 

    
    if (new_course) {
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
    
    $('.startDate').each(function() {
        
        $(this).datepicker();
    });
    
    $("#courseSave").click(function(){
        if (new_course) {
            setTimeout(function(){window.location.href = baseUrl + "/dashboard/"+auth+"/"+id;});
        }
        else refresh();

        error("ERROR SAVING COURSE DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA ");
    });
    
    $("#planSave").click(function(){
        updatePlan();
        refresh();
    });
    
    $("#testUpload").click(function(){
        uploadTest();
        refresh();
    });
    
    $("#enroll").click(function(){
        enroll();
        refresh();
    });
    
    $('#errorItem').click(function(){
        $('#errorItem').fadeOut(100);
    });
    
    // tier listners
    // action plan
    $('#data2 select').on('change', function() {
        alert( this.value );
    });
    
    // knowledge test plan
    $('#data3 select').on('change', function() {
        alert( this.value + "test" );
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

function refresh() {

    populateCourse();

    populateActionPlan();
    populateTest();
}

function error(message) {
    $('#errorItem span').text(message);
    $('#errorItem').fadeIn(500);
}

function populateCourse() {
    if (id != "new_course") {
        var endPoint = baseUrl + "/api/v1/course/"
        $.ajax({
            type: "GET",
            url: endPoint,
            data: {},
            success: function(data){
                for (var i = 0; i < data.objects.length; i++) {
                    console.log(data.objects);
                    if (data.objects[i].id == id) {
                        $(".courseName").val(data.objects[i].course_name);
                        $(".startTime").val(data.objects[i].start_time);
                        $(".courseIns").val(atob(auth).split(":")[0]);
                        $("#courseDone").val(data.objects[i].done);

                        $(".inpTitle").val(data.objects[i].course_name)
                        $(".inpTitle").attr('size', $(".inpTitle").val().length);

                        break;
                    }
                }
            },
            error: function(data){
                error("无法找到课程，请返回后刷新重试");
            },
            beforeSend: function(xhr){
                xhr.setRequestHeader("Authorization", "Apikey " + atob(auth));
                xhr.setRequestHeader("Content-Type", "application/json");
            },
            complete: function(){
            }
        })
    }
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

function getUrl() {
    return location.protocol + "//" + location.hostname + (location.port && ":" + location.port);
}

function getAuthAndID() {
    var params = document.URL.split("/");
    return [params[params.length - 2], params[params.length - 1]];
}