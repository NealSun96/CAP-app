angular.module('app.controllers', [])

.controller('signupCtrl', ['$scope', '$stateParams', '$http', '$state', '$rootScope',
    
    function ($scope, $stateParams, $http, $state, $rootScope) {
        var offline_debug = true;
        $scope.signup = function() {
            if (offline_debug) {$state.go('login');}

            data = {
                "username": $scope.reg_username,
                "first_name": $scope.reg_firstname,
                "last_name": $scope.reg_lastname,
                "password": $scope.reg_password
            };
            $http.post("https://5994a09c.ngrok.io/api/v1/register/", data).then(function successCallback(response) {
                $rootScope.register_success = true;
                $state.go('login');
            }, function errorCallback(response) {
                $rootScope.register_success = false;
                var ERRelement = document.getElementById("signup_error_box");
                ERRelement.style.visibility = "visible";
                setTimeout(function() { ERRelement.style.visibility = "hidden"; }, 2500);
            });
        }
    }])

.controller('loginCtrl', ['$scope', '$stateParams', '$http', '$state', '$rootScope',
    function ($scope, $stateParams, $http, $state, $rootScope) {
        var offline_debug = true;

        $scope.login = function() {
            if (offline_debug) {$state.go('dashboard');}

            var auth = btoa($scope.username + ":" + $scope.password);
            var config = {headers:  {
                'Authorization': 'Basic ' + auth,
                'Content-Type': 'application/json'
            }
        };

        $http.get("https://5994a09c.ngrok.io/api/v1/login/", config).then(function successCallback(response) {
            $rootScope.api_auth = $scope.username + ":" + response.data.objects[0].api_key;
            $scope.saveData();
            $state.go('dashboard');
        }, function errorCallback(response) {
            $rootScope.logout();//delete any existing data
            var ERRelement = document.getElementById("login_error_message");
            ERRelement.style.visibility = "visible";
            setTimeout(function() { ERRelement.style.visibility = "hidden"; }, 2500);
        });
    }
    // used for testing
    // $scope.printData = function(){
    //     alert("user: " + window.localStorage.getItem("username") + " pass: " + window.localStorage.getItem("password"));
    // }

    $scope.logout = function(){
        //delete all data saved
        window.localStorage.removeItem("apiKey");
    }

    $scope.saveData = function(){
        window.localStorage.setItem("apiKey", $rootScope.api_auth);
    }

    //if user data is found, it fills the fields with it and calls login
    $scope.isLoggedIn = function (){
        if (window.localStorage.getItem("apiKey") !== null) {
            $rootScope.api_auth = window.localStorage.getItem("apiKey");
            $state.go("dashboard");
        }else{
            console.log("No saved user data");
        }
    }

    //runs at page load
    $scope.isLoggedIn();

}])

.controller('courseOneCtrl', ['$scope', '$stateParams', '$http', '$rootScope', '$state',
    function ($scope, $stateParams, $http, $rootScope, $state) {
        $scope.f_disabled = false;
        $scope.ap_disabled = false;
        $scope.kt_disabled = false;
        $scope.d_disabled = false;

        var init = function() {
            var config = {headers:  {
                'Authorization': 'Apikey ' + $rootScope.api_auth
            }
        };
        $http.get("https://5994a09c.ngrok.io/api/v1/enrollment/enrollments/", config)
        .then(function successCallback(response) {
            var enrollments = response.data.objects;
            $rootScope.enrollments = enrollments

            var len = enrollments.length;
            for (var i = 0; i < len; i++) {
                if (enrollments[i].id == $rootScope.enrollment_in_handle) {
                    $scope.enrollment = enrollments[i];
                }
            }

            $scope.f_disabled = $scope.enrollment.feedback_status != 'Available';
            $scope.ap_disabled = $scope.enrollment.action_plan_status != 'Available';
            $scope.kt_disabled = $scope.enrollment.knowledge_test_status != 'Available';
            $scope.d_disabled = $scope.enrollment.diagnosis_status != 'Available';
        }, function errorCallback(response) {
            $rootScope.enrollments = [];
        });
    };
    init();

    $scope.feedback = function() {
        if (!$scope.f_disabled) {
            $state.go("feedback");
        }
    };

    $scope.action_plan = function() {
        if (!$scope.ap_disabled) {
            $state.go("behavior");
        }
    };

    $scope.k_test = function() {
        if (!$scope.kt_disabled) {
            $state.go("knowledge_test");
        }
    };

    $scope.diagnosis = function() {
        if (!$scope.d_disabled) {
            $state.go("diagnosis");
        }
    }
}])

.controller('dashboardCtrl', ['$scope', '$stateParams', '$http', '$rootScope', '$state',
    function ($scope, $stateParams, $http, $rootScope, $state) {
        var init = function() {
            var config = {headers:  {
                'Authorization': 'Apikey ' + $rootScope.api_auth
            }
        };

        $http.get("https://5994a09c.ngrok.io/api/v1/enrollment/enrollments/", config)
        .then(function successCallback(response) {
            $rootScope.enrollments = response.data.objects;
        }, function errorCallback(response) {
            $rootScope.enrollments = [];
        });
    };
    init();

    $scope.toAssignments = function(e_id) {
        $rootScope.enrollment_in_handle = e_id;
        $state.go("courseOne");
    }

    $scope.logout = function(){
        //delete all data saved
        window.localStorage.removeItem("apiKey");
        $state.go("Login");
    }
}])


.controller('feedbackCtrl', ['$scope', '$stateParams', '$http', '$rootScope', '$state',
    function ($scope, $stateParams, $http, $rootScope, $state) {
        var offline_debug = true;
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
            if (offline_debug) {$state.go('courseOne');}
            answers.push($scope.feedback_page_text_area);
            var config = {headers:  {'Authorization': 'Apikey ' + $rootScope.api_auth}};
            var data = {"feedbacks": angular.toJson(answers)}
            var url = "https://5994a09c.ngrok.io/api/v1/enrollment/upload/" + $rootScope.enrollment_in_handle + "/feedback/";
            $http.post(url, data, config).then(function successCallback(response) {
                $state.go('courseOne');
            }, function errorCallback(response) {
            });
        }
    }])

.controller('behaviorCtrl', ['$scope', '$stateParams', '$http', '$rootScope', '$state',
    function ($scope, $stateParams, $http, $rootScope, $state) {
        var offline_debug = true;
        $scope.limit = 3;

        $scope.loadActions = function() {
            $scope.checked = 0;
            var config = {headers:  {
                'Authorization': 'Apikey ' + $rootScope.api_auth
            }
        };

        var url = "https://5994a09c.ngrok.io/api/v1/enrollment/assignments/" + $rootScope.enrollment_in_handle + "/action_plan/";
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
        if (offline_debug) {$state.go(courseOne);}
        var answers = [];
        for (var i = 0; i < $scope.action_points.length; i++) {
            if ($scope.action_points[i].selected) answers.push($scope.action_points[i].point)
        };
    var config = {headers:  {'Authorization': 'Apikey ' + $rootScope.api_auth}};
    var data = {"answers": angular.toJson(answers)}
    var url = "https://5994a09c.ngrok.io/api/v1/enrollment/upload/" + $rootScope.enrollment_in_handle + "/action_plan/";
    $http.post(url, data, config).then(function successCallback(response) {
        $state.go('courseOne');
    }, function errorCallback(response) {
    });
}
}])

.controller('knowledge_testCtrl', ['$scope', '$stateParams', '$http', '$rootScope', '$state',
    function ($scope, $stateParams, $http, $rootScope, $state) {
        var offline_debug = true;
        var answers = []
        $scope.count = 0;
        var init = function() {
            var config = {headers:  {
                'Authorization': 'Apikey ' + $rootScope.api_auth
            }
        };

        var url = "https://5994a09c.ngrok.io/api/v1/enrollment/assignments/" + $rootScope.enrollment_in_handle + "/knowledge_test/";
        $http.get(url, config).then(function successCallback(response) {
            var questions = response.data.objects[0].questions;
            for (var i = 0; i < questions.length; i++) {
                questions[i]['id'] = i;
                questions[i]['display_id'] = i + 1;
                answers.push("");
            };
            $scope.questions = questions;
            $scope.limit = questions.length;
        }, function errorCallback(response) {
            $scope.questions = [];
        });

        $http.post("http://5994a09c.ngrok.io/api/v1/enrollment/record_start/" + $rootScope.enrollment_in_handle + "/", {}, config).then(function successCallback(response) {
        }, function errorCallback(response) {});
    };
    init();

    $scope.click = function(id, choice) {
        if (answers[id] == "") $scope.count++;
        answers[id] = choice;
    }

    $scope.submit = function() {
        if (offline_debug) {$state.go('courseOne');}
        $rootScope.knowledge_test_answers = answers;
        $state.go('check_knowledge_test');
    }

}])

.controller('diagnosisCtrl', ['$scope', '$stateParams', '$http', '$rootScope', '$state',
    function ($scope, $stateParams, $http, $rootScope, $state) {
        var offline_debug = true;
        var self_diagnosis = [];
        var other_diagnosis = [];
        $scope.options = ["明显进步", "稍有改善", "没有变化"];
        $scope.count = 0;

        $scope.loadDiagnosis = function() {
            var config = {headers:  {
                'Authorization': 'Apikey ' + $rootScope.api_auth
            }
        };

        var url = "https://5994a09c.ngrok.io/api/v1/enrollment/assignments/" + $rootScope.enrollment_in_handle + "/diagnosis/";
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
            self_diagnosis[id] = option;
        }
        else {
            if (other_diagnosis[id] == "") $scope.count++;
            other_diagnosis[id] = option;
        }
    }

    $scope.submit = function() {
        if (offline_debug) {$state.go('courseOne');}
        var config = {headers:  {'Authorization': 'Apikey ' + $rootScope.api_auth}};
        var data = {"self_diagnosis": angular.toJson(self_diagnosis), "other_diagnosis": angular.toJson(other_diagnosis)}
        var url = "https://5994a09c.ngrok.io/api/v1/enrollment/upload/" + $rootScope.enrollment_in_handle + "/diagnosis/";
        $http.post(url, data, config).then(function successCallback(response) {
            $state.go('courseOne');
        }, function errorCallback(response) {
        });
    }
}])

.controller('check_knowledge_testCtrl', ['$scope', '$stateParams', '$http', '$rootScope', '$state',
    function ($scope, $stateParams, $http, $rootScope, $state) {
        var init = function() {
            $scope.passed = false;
            $scope.score_message = "Calculating...";
            var config = {headers:  {'Authorization': 'Apikey ' + $rootScope.api_auth}};
            var data = {"answers": angular.toJson($rootScope.knowledge_test_answers)}
            var url = "http://5994a09c.ngrok.io/api/v1/enrollment/check_mark/" + $rootScope.enrollment_in_handle + "/";
            $http.post(url, data, config).then(function successCallback(response) {
                var score = response.data.objects[0];
                var total_score = response.data.objects[1];
                var passed = score * 1.0 / total_score > 0.8;

                data = {"first_score": score}
                url = "https://5994a09c.ngrok.io/api/v1/enrollment/first_score/" + $rootScope.enrollment_in_handle + "/";
                $http.post(url, data, config).then(function successCallback(response) {
                    $scope.score = score;
                    $scope.score_message = "Your current score is: " + score + "/" + total_score;
                    $scope.passed = passed;
                    $scope.extra_message = passed ? "You can choose to go back and retry, or to submit." : "You score is too low for the test to be submitted. Please retry.";
                }, function errorCallback(response) {});
            }, function errorCallback(response) {
            });
        };
        init();

        $scope.submit = function() {
            var config = {headers:  {'Authorization': 'Apikey ' + $rootScope.api_auth}};
            var data = {"answers": angular.toJson($rootScope.knowledge_test_answers), "final_score": $scope.score}
            var url = "https://5994a09c.ngrok.io/api/v1/enrollment/upload/" + $rootScope.enrollment_in_handle + "/knowledge_test/";
            $http.post(url, data, config).then(function successCallback(response) {
                $state.go('courseOne');
            }, function errorCallback(response) {
            });
        }
    }])
