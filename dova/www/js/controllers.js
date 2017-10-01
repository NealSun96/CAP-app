angular.module('app.controllers', [])

.controller('signupCtrl', ['$scope', '$stateParams', '$http', '$state', '$rootScope',
    
    function ($scope, $stateParams, $http, $state, $rootScope) {
        var offline_debug = false;
        $scope.selectedGroup = "Cardio";//default
        
        $scope.signup = function() {
            if (offline_debug) {$state.go('login');}

            data = {
                "username": $scope.reg_username,
                "first_name": $scope.reg_firstname,
                "last_name": $scope.reg_lastname,
                "password": $scope.reg_password,
                "bu": $scope.selectedGroup
            };
            $http.post("http://bd35b038.ngrok.io/api/v1/register/", data).then(function successCallback(response) {
                $rootScope.register_success = true;
                $state.go('login');
            }, function errorCallback(response) {
                var changed = false;
                $rootScope.checkConnection();

                //get tags
                var errorText = document.getElementById("error-text");
                var firstName = document.getElementById("firstNameField");
                var lastName = document.getElementById("lastNameField");
                var username = document.getElementById("usernameField");
                var password = document.getElementById("passwordField");

                errorText.innerHTML = "";//reset error text

                if (firstName.value.length == 0){ 
                    errorText.innerHTML += "请填写First Name！<br>";
                    changed = true;
                }

                if (lastName.value.length == 0){ 
                    errorText.innerHTML += "请填写Last Name！<br>";
                    changed = true;
                }

                if (username.value.length < 3){ 
                    errorText.innerHTML += "Email必须超过三个字符！<br>";
                    changed = true;
                }

                if (password.value.length < 4){
                    errorText.innerHTML += "Password必须超过四个字符！";
                    changed = true;
                }

                if(!changed) {
                    errorText.innerHTML = response.data.error;
                    if (errorText.innerHTML == "") errorText.innerHTML = "注册发生错误！";
                }
                $rootScope.register_success = false;

                //show error box
                var ERRelement = document.getElementById("signup_error_box");
                ERRelement.style.visibility = "visible";
                setTimeout(function() { ERRelement.style.visibility = "hidden"; }, 2500);
            });
        }

        //print out the selected value from the dropdown
        $scope.showSelectValue = function(mySelect) {
            $scope.selectedGroup = mySelect;
        }
    }])

.controller('loginCtrl', ['$scope', '$stateParams', '$http', '$state', '$rootScope',
    function ($scope, $stateParams, $http, $state, $rootScope) {
        var offline_debug = false;

        $scope.login = function() {
            if (offline_debug) {$state.go('dashboard');}

            var auth = btoa($scope.username + ":" + $scope.password);
            var config = {headers:  {
                'Authorization': 'Basic ' + auth,
                'Content-Type': 'application/json'
            }
        };

        $http.get("http://bd35b038.ngrok.io/api/v1/login/", config).then(function successCallback(response) {
            $rootScope.api_auth = $scope.username + ":" + response.data.objects[0].api_key;
            $scope.saveData();
            $state.go('dashboard');
        }, function errorCallback(response) {
            alert(response);
                $rootScope.checkConnection();

                var errorText = document.getElementById("error-text");

                if (response.status >= 500) errorText.innerHTML = "服务器出现错误，请稍后重试！";
                if(response.status == 401) errorText.innerHTML = "错误的Email或密码，请重试！";

                $rootScope.register_success = false;

                //show error box
                var ERRelement = document.getElementById("login_error_message");
                ERRelement.style.display = "block";
                setTimeout(function() { ERRelement.style.display = "none"; }, 2500);
            });
    }


    $scope.saveData = function(){
        window.localStorage.setItem("apiKey", $rootScope.api_auth);
    }

    //if user data is found, it fills the fields with it and calls login
    $scope.isLoggedIn = function (){
        if (window.localStorage.getItem("apiKey") !== null) {
            $rootScope.api_auth = window.localStorage.getItem("apiKey");
            $state.go("dashboard");
        }
    }

    //runs at page load
    $scope.isLoggedIn();
}])


.controller('dashboardCtrl', ['$scope', '$stateParams', '$http', '$rootScope', '$state',
    function ($scope, $stateParams, $http, $rootScope, $state) {
        var init = function() {
            var config = {headers:  {
                'Authorization': 'Apikey ' + $rootScope.api_auth
            }
        };

        $scope.show_detail = [];
        $http.get("http://bd35b038.ngrok.io/api/v1/enrollment/enrollments/", config)
        .then(function successCallback(response) {
            $rootScope.enrollments = response.data.objects;
            for (var i = 0; i < response.data.objects.length; i++) $scope.show_detail.push(true);
        }, function errorCallback(response) {
            $rootScope.enrollments = [];
        });
    };
    init();

    $scope.toFeedback = function(e_id) {
        $rootScope.enrollment_in_handle = e_id;
        $state.go("feedback");
    };

    $scope.toActionPlan = function(e_id) {
        $rootScope.enrollment_in_handle = e_id;
        $state.go("behavior");
    };

    $scope.toKTest = function(e_id) {
        $rootScope.enrollment_in_handle = e_id;
        $state.go("knowledge_test");
    };

    $scope.toDiagnosis = function(e_id) {
        $rootScope.enrollment_in_handle = e_id;
        $state.go("diagnosis");
    };

    $scope.logout = function(){
        //delete all data saved
        window.localStorage.removeItem("apiKey");
        $state.go("login");
    }

    $scope.toggleGroup = function (i){
         $scope.show_detail[i] = !$scope.show_detail[i];
    }

}])


.controller('feedbackCtrl', ['$scope', '$stateParams', '$http', '$rootScope', '$state',
    function ($scope, $stateParams, $http, $rootScope, $state) {
        var offline_debug = false;
        $scope.counter = 0;
        $scope.limit = 11;
        var answers = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1];
        var a_questions = ["1.本次培训内容和实际需求匹配度如何？", "2.本次培训的目标对你的明确程度如何？", "3.此次培训对提到的目标的完成度如何？", "4.培训时间长度可覆盖所提到的目标么？"];
        var b_questions = ["1.讲师讲解的易懂性:", "2.讲师能够清楚简明扼要回答问题的能力：", "3.讲师能够调整进度适应不同学员的能力：", "4.讲师专注在课程目标："];
        var c_questions = ["1.培训教室的舒适程度：", "2.培训组织与协调："];

        $scope.a_questions = [];
        $scope.b_questions = [];
        $scope.c_questions = [];
        $scope.d_question = {
            question: "",
            id: 10
        };
        $scope.keys = ["优秀", "一般", "差 "];

        for (var i = 0; i < a_questions.length; i++) {
            $scope.a_questions.push({
                question: a_questions[i],
                id: i
            })
        }
        for (var i = 0; i < b_questions.length; i++) {
            $scope.b_questions.push({
                question: b_questions[i],
                id: i + a_questions.length
            })
        }
        for (var i = 0; i < c_questions.length; i++) {
            $scope.c_questions.push({
                question: c_questions[i],
                id: i + a_questions.length + b_questions.length
            })
        }

        $scope.click = function(q, value) {
            if (answers[q.id] == -1) $scope.counter++;
            answers[q.id] = value;
        }

        $scope.submit = function() {
            if (offline_debug) {$state.go('dashboard');}
            answers.push($scope.feedback_page_text_area);
            var config = {headers:  {'Authorization': 'Apikey ' + $rootScope.api_auth}};
            var data = {"feedbacks": angular.toJson(answers)}
            var url = "http://bd35b038.ngrok.io/api/v1/enrollment/upload/" + $rootScope.enrollment_in_handle + "/feedback/";
            $http.post(url, data, config).then(function successCallback(response) {
                $state.go('dashboard');
            }, function errorCallback(response) {
            });
        }
    }])

.controller('behaviorCtrl', ['$scope', '$stateParams', '$http', '$rootScope', '$state',
    function ($scope, $stateParams, $http, $rootScope, $state) {
        var offline_debug = false;
        $scope.limit = 3;

        $scope.loadActions = function() {
            $scope.checked = 0;
            var config = {headers:  {
                'Authorization': 'Apikey ' + $rootScope.api_auth
            }
        };

        var url = "http://bd35b038.ngrok.io/api/v1/enrollment/assignments/" + $rootScope.enrollment_in_handle + "/action_plan/";
        $http.get(url, config).then(function successCallback(response) {
            $scope.action_points = [];
            var action_points = response.data.objects[0].action_points;
            for (var i = 0; i < action_points.length; i++) {
                $scope.action_points.push({
                    point: action_points[i],
                    selected: false
                });
            };
        }, function errorCallback(response) {
            $scope.action_points = [];
        });
    };

    $scope.onClick = function(point) {
        if(point.selected) $scope.checked++;
        else $scope.checked--;
    }

    $scope.submit = function() {
        if (offline_debug) {$state.go(dashboard);}
        var answers = [];
        for (var i = 0; i < $scope.action_points.length; i++) {
            if ($scope.action_points[i].selected) answers.push($scope.action_points[i].point)
        };
    var config = {headers:  {'Authorization': 'Apikey ' + $rootScope.api_auth}};
    var data = {"answers": angular.toJson(answers)}
    var url = "http://bd35b038.ngrok.io/api/v1/enrollment/upload/" + $rootScope.enrollment_in_handle + "/action_plan/";
    $http.post(url, data, config).then(function successCallback(response) {
        $state.go('dashboard');
    }, function errorCallback(response) {
    });
}
}])

.controller('knowledge_testCtrl', ['$scope', '$stateParams', '$http', '$rootScope', '$state',
    function ($scope, $stateParams, $http, $rootScope, $state) {
        var offline_debug = false;
        var answers = []
        $scope.count = 0;
        var init = function() {
            var config = {headers:  {
                'Authorization': 'Apikey ' + $rootScope.api_auth
            }
        };

        var url = "http://bd35b038.ngrok.io/api/v1/enrollment/assignments/" + $rootScope.enrollment_in_handle + "/knowledge_test/";
        $http.get(url, config).then(function successCallback(response) {
            var questions = response.data.objects[0].questions;
            for (var i = 0; i < questions.length; i++) {
                //questions[i]['id'] = i;
                //questions[i]['display_id'] = i + 1;
                answers.push("");
            };
            $scope.questions = questions;
            $scope.limit = questions.length;
        }, function errorCallback(response) {
            $scope.questions = [];
        });

        $http.post("http://bd35b038.ngrok.io/api/v1/enrollment/record_start/" + $rootScope.enrollment_in_handle + "/", {}, config).then(function successCallback(response) {
        }, function errorCallback(response) {});
    };
    init();

    $scope.click = function(id, choice) {
        if (answers[id] == "") $scope.count++;
        answers[id] = choice;
    }

    $scope.submit = function() {
        if (offline_debug) {$state.go('dashboard');}
        $rootScope.knowledge_test_answers = answers;
        $state.go('check_knowledge_test');
    }

}])

.controller('diagnosisCtrl', ['$scope', '$stateParams', '$http', '$rootScope', '$state',
    function ($scope, $stateParams, $http, $rootScope, $state) {
        var offline_debug = false;
        var self_diagnosis = [];
        var other_diagnosis = [];
        $scope.options = ["明显进步", "稍有改善", "没有变化"];
        $scope.count = 0;

        $scope.loadDiagnosis = function() {
            var config = {headers:  {
                'Authorization': 'Apikey ' + $rootScope.api_auth
            }
        };

        var url = "http://bd35b038.ngrok.io/api/v1/enrollment/assignments/" + $rootScope.enrollment_in_handle + "/diagnosis/";
        $http.get(url, config).then(function successCallback(response) {
            $scope.diagnosis_points = [];
            var diagnosis_points = response.data.objects[0].diagnosis_points;
            for (var i = 0; i < diagnosis_points.length; i++) {
                $scope.diagnosis_points.push({
                    point: diagnosis_points[i],
                    id: i,
                    display_id: i + 1,
                    self_id: "s" + i,
                    other_id: "o" + i
                });
                self_diagnosis.push("");
                other_diagnosis.push("");
            };
            $scope.limit = diagnosis_points.length * 2;
        }, function errorCallback(response) {
            $scope.diagnosis_points = [];
        });
    };

    $scope.click = function(id, self_id, option) {
        if (self_id.slice(0, 1) == "s") {
            if (self_diagnosis[id] == "") $scope.count++;
            self_diagnosis[id] = $scope.options.length - $scope.options.indexOf(option);
        }
        else {
            if (other_diagnosis[id] == "") $scope.count++;
            other_diagnosis[id] = $scope.options.length - $scope.options.indexOf(option);
        }
    }

    $scope.submit = function() {
        if (offline_debug) {$state.go('dashboard');}
        var config = {headers:  {'Authorization': 'Apikey ' + $rootScope.api_auth}};
        var data = {"self_diagnosis": angular.toJson(self_diagnosis), "other_diagnosis": angular.toJson(other_diagnosis)}
        var url = "http://bd35b038.ngrok.io/api/v1/enrollment/upload/" + $rootScope.enrollment_in_handle + "/diagnosis/";
        $http.post(url, data, config).then(function successCallback(response) {
            $state.go('dashboard');
        }, function errorCallback(response) {
        });
    }
}])

.controller('check_knowledge_testCtrl', ['$scope', '$stateParams', '$http', '$rootScope', '$state', '$ionicViewSwitcher',
    function ($scope, $stateParams, $http, $rootScope, $state, $ionicViewSwitcher) {
        var init = function() {
            $scope.passed = false;
            $scope.score_message = "批改答卷中...";
            var config = {headers:  {'Authorization': 'Apikey ' + $rootScope.api_auth}};
            var data = {"answers": angular.toJson($rootScope.knowledge_test_answers)}
            var url = "http://bd35b038.ngrok.io/api/v1/enrollment/check_mark/" + $rootScope.enrollment_in_handle + "/";
            $http.post(url, data, config).then(function successCallback(response) {
                var score = response.data.objects[0];
                var total_score = response.data.objects[1];
                var passed = score * 1.0 / total_score >= response.data.objects[2];

                data = {"first_score": score}
                url = "http://bd35b038.ngrok.io/api/v1/enrollment/first_score/" + $rootScope.enrollment_in_handle + "/";
                $http.post(url, data, config).then(function successCallback(response) {
                    $scope.score = score;
                    $scope.score_message = "你的得分是：" + score + "/" + total_score;
                    $scope.passed = passed;
                    $scope.extra_message = passed ? "你可以返回重试，或者提交答卷" : "你的得分未达到提交标准，请返回重试";
                }, function errorCallback(response) {});
            }, function errorCallback(response) {
            });
        };
        init();

        $scope.submit = function() {
            var config = {headers:  {'Authorization': 'Apikey ' + $rootScope.api_auth}};
            var data = {"answers": angular.toJson($rootScope.knowledge_test_answers), "final_score": $scope.score}
            var url = "http://bd35b038.ngrok.io/api/v1/enrollment/upload/" + $rootScope.enrollment_in_handle + "/knowledge_test/";
            $http.post(url, data, config).then(function successCallback(response) {
                $ionicViewSwitcher.nextDirection('back');
                $state.go('dashboard');
            }, function errorCallback(response) {
            });
        }
    }])

.controller('change_passwordCtrl', ['$scope', '$stateParams', '$http', '$rootScope', '$state',
    function ($scope, $stateParams, $http, $rootScope, $state) {
        $scope.changePassword = function(){
            //check with server
            var auth = btoa($scope.username + ":" + $scope.oldPassword);
            var config = {headers:  {
                'Authorization': 'Basic ' + auth,
                'Content-Type': 'application/json'
            }};
            var data = {"new_password": $scope.newPassword};

            $http.post("http://bd35b038.ngrok.io/api/v1/login/change_password/", data, config)
            .then(function successCallback(response) {
                $state.go('login');
            }, function errorCallback(response) {
                $rootScope.checkConnection();

                //get tags
                var errorText = document.getElementById("error-text");
                var newPass = document.getElementById("changed_pass");

                errorText.innerHTML = "";//reset error text

                if (response.status >= 500) errorText.innerHTML = "服务器出现错误，请稍后重试！";
                if(response.status == 401) errorText.innerHTML = "错误的Email或密码，请重试！";

                //simple for new password length
                if (newPass.value.length < 4) errorText.innerHTML += "新密码必须超过四个字符！";

                if(errorText.innerHTML == "") {
                    errorText.innerHTML = response.data.error;
                    if (errorText.innerHTML == "" || errorText.innerHTML == "undefined") errorText.innerHTML = "发生错误！";
                }

                //show error box
                var ERRelement = document.getElementById("change_pass_error_message");
                ERRelement.style.visibility = "visible";
                setTimeout(function() { ERRelement.style.visibility = "hidden"; }, 2500);
            });
            //then go back to login
        }
}])

.run(function($rootScope){
    //check connection to Internet
    $rootScope.checkConnection = function(){
        if(window.Connection){
            if(navigator.connection.type == Connection.NONE) {
                alert("未能检测到网络连接，请检查设备设置！");
                return true;
            }
        }
    }
})
