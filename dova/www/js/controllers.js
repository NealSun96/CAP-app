angular.module('app.controllers', [])
  
.controller('signupCtrl', ['$scope', '$stateParams', '$http', '$state', '$rootScope',
function ($scope, $stateParams, $http, $state, $rootScope) {
    $scope.signup = function() {
        data = {
            "username": $scope.reg_username,
            "first_name": $scope.reg_firstname,
            "last_name": $scope.reg_lastname,
            "password": $scope.reg_password
        };
        $http.post("https://ebc43596.ngrok.io/api/v1/register/", data).then(function successCallback(response) {
            $rootScope.register_success = true;
            $state.go('login');
        }, function errorCallback(response) {
            $rootScope.register_success = false;
        });
    }
}])
   
.controller('signUpCompleteCtrl', ['$scope', '$stateParams', // The following is the constructor function for this page's controller. See https://docs.angularjs.org/guide/controller
// You can include any angular dependencies as parameters for this function
// TIP: Access Route Parameters for your page via $stateParams.parameterName
function ($scope, $stateParams) {


}])
   
.controller('loginCtrl', ['$scope', '$stateParams', '$http', '$state', '$rootScope',
function ($scope, $stateParams, $http, $state, $rootScope) {

    $scope.login = function() {
        var auth = btoa($scope.username + ":" + $scope.password);
        var config = {headers:  {
        'Authorization': 'Basic ' + auth,
        'Content-Type': 'application/json'
            }
        };

        $http.get("https://ebc43596.ngrok.io/api/v1/login/", config).then(function successCallback(response) {
            $rootScope.api_auth = $scope.username + ":" + response.data.objects[0].api_key;
            $state.go('dashboard');
        }, function errorCallback(response) {
            var ERRelement = document.getElementById("login_error_message");
            ERRelement.style.visibility = "visible";
            setTimeout(function() { ERRelement.style.visibility = "hidden"; }, 2500);
        });
    }
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
        $http.get("https://ebc43596.ngrok.io/api/v1/enrollment/enrollments/", config)
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
   
.controller('quizPageCtrl', ['$scope', '$stateParams', // The following is the constructor function for this page's controller. See https://docs.angularjs.org/guide/controller
// You can include any angular dependencies as parameters for this function
// TIP: Access Route Parameters for your page via $stateParams.parameterName
function ($scope, $stateParams) {


}])
   
.controller('taskPageCtrl', ['$scope', '$stateParams', // The following is the constructor function for this page's controller. See https://docs.angularjs.org/guide/controller
// You can include any angular dependencies as parameters for this function
// TIP: Access Route Parameters for your page via $stateParams.parameterName
function ($scope, $stateParams) {


}])
   
.controller('dashboardCtrl', ['$scope', '$stateParams', '$http', '$rootScope', '$state',
function ($scope, $stateParams, $http, $rootScope, $state) {
    var init = function() {
        var config = {headers:  {
            'Authorization': 'Apikey ' + $rootScope.api_auth
        }
        };

        $http.get("https://ebc43596.ngrok.io/api/v1/enrollment/enrollments/", config)
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
}])

.controller('feedbackCtrl', ['$scope', '$stateParams', // The following is the constructor function for this page's controller. See https://docs.angularjs.org/guide/controller
// You can include any angular dependencies as parameters for this function
// TIP: Access Route Parameters for your page via $stateParams.parameterName
function ($scope, $stateParams) {


}])

.controller('behaviorCtrl', ['$scope', '$stateParams', '$http', '$rootScope', '$state',
function ($scope, $stateParams, $http, $rootScope, $state) {
    $scope.limit = 3;

    $scope.loadActions = function() {
        $scope.checked = 0;
        var config = {headers:  {
            'Authorization': 'Apikey ' + $rootScope.api_auth
        }
        };

        var url = "https://ebc43596.ngrok.io/api/v1/enrollment/assignments/" + $rootScope.enrollment_in_handle + "/action_plan/";
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
        var answers = [];
        for (var i = 0; i < $scope.action_points.length; i++) {
            if ($scope.action_points[i].selected) answers.push($scope.action_points[i].point)
        };
        var config = {headers:  {'Authorization': 'Apikey ' + $rootScope.api_auth}};
        var data = {"answers": angular.toJson(answers)}
        var url = "https://ebc43596.ngrok.io/api/v1/enrollment/upload/" + $rootScope.enrollment_in_handle + "/action_plan/";
        $http.post(url, data, config).then(function successCallback(response) {
            $state.go('courseOne');
        }, function errorCallback(response) {
        });
    }
}])

.controller('knowledge_testCtrl', ['$scope', '$stateParams', '$http', '$rootScope', '$state',
function ($scope, $stateParams, $http, $rootScope, $state) {
    var answers = []
    var init = function() {
        var config = {headers:  {
            'Authorization': 'Apikey ' + $rootScope.api_auth
        }
        };

        var url = "https://ebc43596.ngrok.io/api/v1/enrollment/assignments/" + $rootScope.enrollment_in_handle + "/knowledge_test/";
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

        $http.post("http://ebc43596.ngrok.io/api/v1/enrollment/record_start/" + $rootScope.enrollment_in_handle + "/", {}, config).then(function successCallback(response) {
        }, function errorCallback(response) {});
    };
    init();

    $scope.click = function(id, choice) {
        answers[id] = choice;
        $scope.count = 0;
        for(var i = 0; i< answers.length; i++) {
            $scope.count = answers[i] == "" ? $scope.count : $scope.count+1;
        }
    }

    $scope.submit = function() {
        $rootScope.knowledge_test_answers = answers;
        $state.go('check_knowledge_test');
    }

}])

.controller('diagnosisCtrl', ['$scope', '$stateParams', '$http', '$rootScope', '$state',
function ($scope, $stateParams, $http, $rootScope, $state) {
    $scope.options = ["明显进步", "稍有改善", "没有变化"];
//    $scope.options = ["good", "ok", "bad"];

    $scope.loadDiagnosis = function() {
        var config = {headers:  {
            'Authorization': 'Apikey ' + $rootScope.api_auth
        }
        };

        var url = "https://ebc43596.ngrok.io/api/v1/enrollment/assignments/" + $rootScope.enrollment_in_handle + "/diagnosis/";
        $http.get(url, config).then(function successCallback(response) {
            $scope.diagnosis_points = [];
            var diagnosis_points = response.data.objects[0].diagnosis_points;
            for (var i = 0; i < diagnosis_points.length; i++) {
                $scope.diagnosis_points.push({
                    point: diagnosis_points[i],
                    id: i,
                    display_id: i + 1,
                    self_id: "self" + parseInt(i),
                    other_id: "other" + parseInt(i)
                });
            };
        }, function errorCallback(response) {
            $scope.diagnosis_points = [];
        });
    };
}])

.controller('check_knowledge_testCtrl', ['$scope', '$stateParams', '$http', '$rootScope', '$state',
function ($scope, $stateParams, $http, $rootScope, $state) {
    var init = function() {
        $scope.passed = false;
        var config = {headers:  {'Authorization': 'Apikey ' + $rootScope.api_auth}};
        var data = {"answers": angular.toJson($rootScope.knowledge_test_answers)}
        var url = "http://ebc43596.ngrok.io/api/v1/enrollment/check_mark/" + $rootScope.enrollment_in_handle + "/";
        $http.post(url, data, config).then(function successCallback(response) {
            var score = response.data.objects[0];
            var total_score = response.data.objects[1];
            var passed = score * 1.0 / total_score > 0.8;
            console.log(score * 1.0 / total_score);

            data = {"first_score": score}
            url = "https://ebc43596.ngrok.io/api/v1/enrollment/first_score/" + $rootScope.enrollment_in_handle + "/";
            $http.post(url, data, config).then(function successCallback(response) {
                $scope.score = score;
                $scope.total_score = total_score;
                $scope.passed = passed;
                $scope.extra_message = passed ? "" : "You score is too low for the test to be submitted. Please retry.";
            }, function errorCallback(response) {});
        }, function errorCallback(response) {
        });
    };
    init();

    $scope.submit = function() {
        var config = {headers:  {'Authorization': 'Apikey ' + $rootScope.api_auth}};
        var data = {"answers": angular.toJson($rootScope.knowledge_test_answers), "final_score": $scope.score}
        var url = "https://ebc43596.ngrok.io/api/v1/enrollment/upload/" + $rootScope.enrollment_in_handle + "/knowledge_test/";
        $http.post(url, data, config).then(function successCallback(response) {
            $state.go('courseOne');
        }, function errorCallback(response) {
        });
    }
}])
