var baseUrl = getUrl();
var params = getAuthAndID();
var auth = atob(params[0]);
var teacher = auth.split(":")[0];
var id = params[1];
var new_course = id == "new_course";
var date = new Date();

var reader  = new FileReader();


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

    var titles = ["全部学员", "Cardio", "ENDO", "PION", "CRM", "EP", "Urology",
              "Structural Hear", "HK&TW", "Emerging Marketing", "Others"];
    for (var i=0; i < 11; i++) {
        $("#dataRowTitle").append('<td class="cell header">'+titles[i]+'</td>');
  	    $('#dataTable tr').not($('#dataRowTitle')).append('<td class="cell" id="' + i + '"></td>');
    }

    if (!new_course) {
        refresh();
    }
    
    $("#refresh").click(function(){setTimeout(function(){window.location.href = document.URL;});});
    
    $("#logout").click(function(){
       $("#logout").animate(function() {
           $("#logout").css("background-color:#4ECDC4;");
       });
       setTimeout(function(){window.location.href = baseUrl + "/courses/"+btoa(auth)});
    }); 

    
    if (new_course) {
        $("#1 span").text("新建课程");
        $("#2").addClass("blocked");
        $("#3").addClass("blocked");
        $("#4").addClass("blocked");
        $("#5").addClass("blocked");
        $("#6").addClass("blocked");
        $("#7").addClass("blocked");
        $("#teacherEmail").val(teacher);
        $("#classStartTimeField").show();
        $("#classDoneField").hide();
    } else {
        $(".menuItem").click(function(){
            if (!$(".menuItem").hasClass('.error')){
                $(".menuItem").removeClass("menuItemActive");
                $(".data").removeClass("active");
                var id = $(this).attr('id');
                $("#data"+id).addClass("active");
                $(this).addClass("menuItemActive");
                refresh();
            }
        });

    }

    $('.startTime').each(function() {
        $(this).val('00:00:00');
        $(this).timepicker({
            timeFormat: 'HH:mm:ss',});
    });
    
    $('.startDate').each(function() {
        $(this).val(new String(date.getFullYear())+"-"+(("0" + date.getMonth()).slice(-2))+"-"+date.getDate());
        $(this).datepicker(
        { dateFormat: 'yy-mm-dd' });
    });
    
    $("#courseSave").click(function(){
        editCourse();
    });
    
    $("#planSave").click(function(){
        editPlan();
    });
    
    $("#testUpload").click(function(){
        editTest();
    });

    $('#q1 .checkBox').on("change", function() {$('#q1 .checkBox').not(this).prop('checked', false);});
    $('#q2 .checkBox').on("change", function() {$('#q2 .checkBox').not(this).prop('checked', false);});
    $('#q3 .checkBox').on("change", function() {$('#q3 .checkBox').not(this).prop('checked', false);});
    $('#q4 .checkBox').on("change", function() {$('#q4 .checkBox').not(this).prop('checked', false);});
    $('#q5 .checkBox').on("change", function() {$('#q5 .checkBox').not(this).prop('checked', false);});
    $('#q6 .checkBox').on("change", function() {$('#q6 .checkBox').not(this).prop('checked', false);});
    $('#q7 .checkBox').on("change", function() {$('#q7 .checkBox').not(this).prop('checked', false);});
    $('#q8 .checkBox').on("change", function() {$('#q8 .checkBox').not(this).prop('checked', false);});
    $('#q9 .checkBox').on("change", function() {$('#q9 .checkBox').not(this).prop('checked', false);});
    $('#q10 .checkBox').on("change", function() {$('#q10 .checkBox').not(this).prop('checked', false);});

    $("#enroll").click(function(){
        enroll();
    });

    $("#calculateData").click(function(){
        calculateData();
    });
    
    $('#errorItem').click(function(){
        $('#errorItem').fadeOut(100);
    });

	$('#saveNoti').click(function(){
        $('#saveNoti').fadeOut(100);
    });
    
    $('#dropDownSave').click(function(){
        editCourse();
    });
    
    $('#courseDateSave').click(function(){
        $('#courseStartDate').val($('#newCourseStartDate').val());
        $('#courseStartTime').val($('#newCourseStartTime').val());
        editCourse();
        populateEnrollTimes();
    });
});

function editCourse() {
    var endPoint;
    if (new_course) endPoint = baseUrl + "/api/v1/course/add_course/";
    else endPoint = baseUrl + "/api/v1/course/edit_course/" + id + "/";
    var start_time = $('#courseStartDate').val() + "T"+$('#courseStartTime').val()+"+08:00";
    var data = {
            "course_name": $(".courseName").val(),
            "start_time": start_time,
            "teacher": $(".courseIns").val(),
            "done": $('#courseDone').prop('checked')
        }
    $.ajax({
        type: "POST",
        url: endPoint,
        data: JSON.stringify(data),
        dataType: "json",
        success: function(data){
            if (teacher != data.teacher) {
                $("#logout").click();
            }
            else if (id != data.id) {
                setTimeout(function(){window.location.href = baseUrl + "/dashboard/"+btoa(auth)+"/"+data.id;});
            }
            else {
                refresh();
                saveNoti();
            }
        },
        error: function(data){
            error(data.responseText);
        },
        beforeSend: function(xhr){
            xhr.setRequestHeader("Authorization", "Apikey " + auth);
            xhr.setRequestHeader("Content-Type", "application/json");
        },
        complete: function(){
        }
    })
}

function editPlan() {
    var endPoint = baseUrl + "/api/v1/course/edit_assignments/"
    + id + "/action_plan/";
    var points = [];
    $("#data2 li input").each(function() { if ($(this).val() != "") {points.push($(this).val())} });
    var data = {
            "action_points": points
        }
    $.ajax({
        type: "POST",
        url: endPoint,
        data: JSON.stringify(data),
        dataType: "json",
        success: function(data){
            refresh();
            saveNoti();
        },
        error: function(data){
            error(data.responseText);
        },
        beforeSend: function(xhr){
            xhr.setRequestHeader("Authorization", "Apikey " + auth);
            xhr.setRequestHeader("Content-Type", "application/json");
        },
        complete: function(){
        }
    })
}

function editTest() {
    var endPoint = baseUrl + "/api/v1/course/edit_assignments/"
    + id + "/knowledge_test/";
    var questions = [];

    for (var i = 0; i < 10; i++) {
        var qbody = $("#q" + (i+1) + " .question").val();

        if (qbody == "") continue;

        var qscore = $("#q" + (i+1) + " .score").val();
        var qkeys = [];
        var qrightanswer = "";
        for (var j = 0; j < 4; j++) {
            qkeys.push($("#q" + (i+1) + " .opt" + (j+1)).val());
            if ($("#q" + (i+1) + " .option" + (j+1)).prop('checked')) {
                qrightanswer = $("#q" + (i+1) + " .opt" + (j+1)).val();
            }
        }
        questions.push({
            "question_body": qbody,
            "score": qscore,
            "answer_keys": qkeys,
            "right_answer": qrightanswer,
        })
    }
    var data = {
            "questions": questions
        }
    $.ajax({
        type: "POST",
        url: endPoint,
        data: JSON.stringify(data),
        dataType: "json",
        success: function(data){
            refresh();
            saveNoti();
        },
        error: function(data){
            error(data.responseText);
        },
        beforeSend: function(xhr){
            xhr.setRequestHeader("Authorization", "Apikey " + auth);
            xhr.setRequestHeader("Content-Type", "application/json");
        },
        complete: function(){
        }
    })
}

function enroll() {
    var file = $('#studentFile').prop('files')[0];
    reader.onload = receivedText;
    reader.readAsDataURL(file);
    function receivedText() {
        var endPoint = baseUrl + "/api/v1/course/enroll_students/" + id + "/";
        $.ajax({
            type: "POST",
            url: endPoint,
            data: JSON.stringify({
                file: reader.result
            }),
            dataType: "json",
            success: function(data){
                refresh();
                saveNoti();
            },
            error: function(data){
                error(data.responseText);
            },
            beforeSend: function(xhr){
                xhr.setRequestHeader("Authorization", "Apikey " + auth);
                xhr.setRequestHeader("Content-Type", "application/json");
            },
            complete: function(){
            }
        })
    }
}

function calculateData() {
    var endPoint = baseUrl + "/api/v1/course/get_data/"+ id +"/";
    var start_time = $('#dataStartDate').val();
    var end_time = $('#dataEndDate').val();
    var data = {
            "start_time": start_time,
            "end_time": end_time
        }
    $.ajax({
        type: "POST",
        url: endPoint,
        data: JSON.stringify(data),
        dataType: "json",
        success: function(data){
            for (var i = 0; i < data.objects.length; i++) {
                for (var j = 0; j < data.objects[i].length; j++) {
                    $("#dataRow"+j+" #"+i).html(data.objects[i][j]);
                }
            }
        },
        error: function(data){
            error(data.responseText);
        },
        beforeSend: function(xhr){
            xhr.setRequestHeader("Authorization", "Apikey " + auth);
            xhr.setRequestHeader("Content-Type", "application/json");
        },
        complete: function(){
        }
    })
}


function refresh() {
    populateCourse();
    populateActionPlan();
    populateKnowledgeTest();
    populateEnrolls();
    populateEnrollTimes();
    $('#errorItem').fadeOut(100);
    $('#saveNoti').fadeOut(100);
}

function error(message) {
    $('#errorItem span').text(message);
    $('#errorItem').fadeIn(500);
}

function saveNoti() {
    $('#saveNoti span').text("保存成功");
    $('#saveNoti').fadeIn(500);
}

function populateCourse() {
    if (!new_course) {
        var endPoint = baseUrl + "/api/v1/course/"
        $.ajax({
            type: "GET",
            url: endPoint,
            data: {},
            success: function(data){
                for (var i = 0; i < data.objects.length; i++) {
                    if (data.objects[i].id == id) {
                        $(".courseName").val(data.objects[i].course_name);
                        var time = data.objects[i].start_time
                        $("#courseStartTime").val(time.split("T")[1]);
                        $("#courseStartDate").val(time.split("T")[0]);
                        $(".courseIns").val(teacher);
                        $("#courseDone").prop('checked', data.objects[i].done);

                        $(".inpTitle").val(data.objects[i].course_name+"（"+time.split("T")[0]+"）")
                        $(".inpTitle").attr('size', $(".inpTitle").val().length);

                        break;
                    }
                }
            },
            error: function(data){
                error("无法找到课程，请返回后刷新重试");
            },
            beforeSend: function(xhr){
                xhr.setRequestHeader("Authorization", "Apikey " + auth);
                xhr.setRequestHeader("Content-Type", "application/json");
            },
            complete: function(){
            }
        })
    }
}

function populateActionPlan() {
    if (!new_course) {
        var endPoint = baseUrl + "/api/v1/course/get_assignments/"
        + id + "/action_plan/";
        $.ajax({
            type: "GET",
            url: endPoint,
            data: {},
            success: function(data){
                var i = 0;
                var points = data.objects[0].action_points;
                for (; points != null && i < points.length; i++) {
                    $("#act" + (i+1)).val(points[i]);
                }
                for (; i < 10; i++) {
                    $("#act" + (i+1)).val("");
                }
            },
            error: function(data){
                error(data.responseText);
            },
            beforeSend: function(xhr){
                xhr.setRequestHeader("Authorization", "Apikey " + auth);
                xhr.setRequestHeader("Content-Type", "application/json");
            },
            complete: function(){
            }
        })
    }
}

function populateKnowledgeTest() {
    if (!new_course) {
        var endPoint = baseUrl + "/api/v1/course/get_assignments/"
        + id + "/knowledge_test/";
        $.ajax({
            type: "GET",
            url: endPoint,
            data: {},
            success: function(data){
                var i = 0;
                var questions = data.objects[0].questions
                for (; questions != null && i < questions.length; i++) {
                    var question = questions[i];
                    $("#q" + (i+1) + " .question").val(question.question);
                    for (var j = 0; j < question.answer_keys.length; j++) {
                        var answer_key = question.answer_keys[j]
                        $("#q" + (i+1) + " .opt" + (j+1)).val(answer_key);
                        if (answer_key == question.right_answer) {
                            $("#q" + (i+1) + " .option" + (j+1)).prop('checked', true);
                        }
                        else {
                            $("#q" + (i+1) + " .option" + (j+1)).prop('checked', false);
                        }
                    }
                    $("#q" + (i+1) + " .score").val(question.score);
                }
                for ( ;i < 10; i++) {
                    $("#q" + (i+1) + " .question").val("");
                    for (var j = 0; j < 4; j++) {
                        $("#q" + (i+1) + " .opt" + (j+1)).val("");
                        $("#q" + (i+1) + " .option" + (j+1)).prop('checked', false);
                    }
                    $("#q" + (i+1) + " .score").val(10);
                }
            },
            error: function(data){
                error(data.responseText);
            },
            beforeSend: function(xhr){
                xhr.setRequestHeader("Authorization", "Apikey " + auth);
                xhr.setRequestHeader("Content-Type", "application/json");
            },
            complete: function(){
            }
        })
    }
}

function populateEnrolls() {
    if (!new_course) {
        var endPoint = baseUrl + "/api/v1/course/get_enrolled/"+ id + "/";
        $.ajax({
            type: "GET",
            url: endPoint,
            data: {},
            success: function(data){
                $("#studentList tr").remove();
                $("#studentList").append("<tr ><td class=\"cell header\">姓名</td><td class=\"cell header\">Email</td><td class=\"cell header\">BU</td><td class=\"cell header\">Feedback</td><td class=\"cell header\">Action Plan</td><td class=\"cell header\">Knowledge Test</td><td class=\"cell header\">Diagnosis</td></tr>");
                for (var i = 0; i < data.objects.length; i++) {
                    var tag = "<tr ><td class=\"cell\">" + data.objects[i][0] +
                    "</td><td class=\"cell\">" + data.objects[i][1] +
                    "</td><td class=\"cell\">" + data.objects[i][2] +
                    "</td><td class=\"cell\">" + data.objects[i][3] +
                    "</td><td class=\"cell\">" + data.objects[i][4] +
                    "</td><td class=\"cell\">" + data.objects[i][5] +
                    "</td><td class=\"cell\">" + data.objects[i][6] + "</td></tr>";
                    $("#studentList").append(tag);
                }
            },
            error: function(data){
                error(data.responseText);
            },
            beforeSend: function(xhr){
                xhr.setRequestHeader("Authorization", "Apikey " + auth);
                xhr.setRequestHeader("Content-Type", "application/json");
            },
            complete: function(){
            }
        })
    }
}

function populateEnrollTimes() {
    if (!new_course) {
        var endPoint = baseUrl + "/api/v1/course/get_enroll_times/"+ id + "/";
        $.ajax({
            type: "GET",
            url: endPoint,
            data: {},
            success: function(data){
                $(".enrollTimesSelect option").remove();
                $("#enrollTimesTable tr").remove();
                $("#enrollTimesTable").append("<tr><td class=\"cell header\">课时</td><td class=\"cell header\">学员人数</td></tr>")
                var tag = "";
                var tableRows = "";
                var selectedIndex = 0;
                for (var i = 0; i < data.objects.length; i++) {
                    tag += "<option value=\""+ data.objects[i][0] + "\">"
                    + data.objects[i][0].split("T")[0] + " " +  data.objects[i][0].split("T")[1]
                    + " " + data.objects[i][1] +
                    "个学员</option>";
                    if (data.objects[i][2]) selectedIndex = i;
                    tableRows += "<tr><td class=\"cell\">"+ data.objects[i][0].split("T")[0]
                     + " " +  data.objects[i][0].split("T")[1]+ "</td><td class=\"cell\">"
                     + data.objects[i][1] + "</td></tr>"
                }
                $(".enrollTimesSelect").append(tag);
                $('.enrollTimesSelect').val($('.enrollTimesSelect>option:eq('+selectedIndex+')').val());
                $("#enrollTimesTable").append(tableRows);
            },
            error: function(data){
                error(data.responseText);
            },
            beforeSend: function(xhr){
                xhr.setRequestHeader("Authorization", "Apikey " + auth);
                xhr.setRequestHeader("Content-Type", "application/json");
            },
            complete: function(){
            }
        })
    }
}

function getUrl() {
    return location.protocol + "//" + location.hostname + (location.port && ":" + location.port);
}

function getAuthAndID() {
    var params = document.URL.split("/");
    return [params[params.length - 2], params[params.length - 1]];
}

function sDate(option) {
    $("#courseStartTime").val(option.value.split("T")[1]);
    $("#courseStartDate").val(option.value.split("T")[0]);
}