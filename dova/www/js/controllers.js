angular.module('app.controllers', [])
  
.controller('signupCtrl', ['$scope', '$stateParams', '$http', '$state', '$rootScope',
function ($scope, $stateParams, $http, $state, $rootScope) {
    $scope.signup = function() {
        data = {
            username: $scope.reg_username,
            first_name: $scope.reg_firstname,
            last_name: $scope.reg_lastname,
            password: $scope.reg_password
        };
        $http.post("https://21574e51.ngrok.io/api/v1/register/", data).then(function successCallback(response) {
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
    $scope.signin_fail = false;

    $scope.login = function() {
        var auth = btoa($scope.username + ":" + $scope.password);
        var config = {headers:  {
        'Authorization': 'Basic ' + auth,
        'Content-Type': 'application/json'
            }
        };

        $http.get("https://21574e51.ngrok.io/api/v1/login/", config).then(function successCallback(response) {
            $rootScope.api_auth = $scope.username + ":" + response.data.objects[0].api_key;
            $state.go('dashboard');
        }, function errorCallback(response) {
            $scope.username = "ERROR";
            $scope.signin_fail = true;
            var element = document.getElementById("login_error_message");
            setTimeout(function() { element.parentNode.removeChild(element).fadeOut(); }, 2500);
        });
    }
}])

.controller('courseOneCtrl', ['$scope', '$stateParams', '$http', '$rootScope', '$state',
function ($scope, $stateParams, $http, $rootScope, $state) {
    $scope.f_disabled = false;
    $scope.ap_disabled = false;
    $scope.kt_disabled = false;
    $scope.d_disabled = false;

    $scope.loadAssignments = function() {
        var len = $rootScope.enrollments.length;
        for (var i = 0; i < len; i++) {
            if ($rootScope.enrollments[i].id == $rootScope.enrollment_in_handle) {
                $scope.enrollment = $rootScope.enrollments[i];
            }
        }

        $scope.f_disabled = $scope.enrollment.feedback_status != 'Available';
        $scope.ap_disabled = $scope.enrollment.action_plan_status != 'Available';
        $scope.kt_disabled = $scope.enrollment.knowledge_test_status != 'Available';
        $scope.d_disabled = $scope.enrollment.diagnosis_status != 'Available';
    };


    $scope.feedback = function() {

    };

    $scope.action_plan = function() {

    };

    $scope.k_test = function() {

    };

    $scope.diagnosis = function() {

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
    $scope.loadEnrollments = function() {
        // $rootScope.api_auth = "test2:7cab15440caceb2ff35099994ae4610cd39cb810";
        var config = {headers:  {
            'Authorization': 'Apikey ' + $rootScope.api_auth
        }
        };

        $http.get("https://21574e51.ngrok.io/api/v1/enrollment/enrollments/", config)
            .then(function successCallback(response) {
            $rootScope.enrollments = response.data.objects;

        }, function errorCallback(response) {
            $rootScope.enrollments = [];
        });
    };

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

.controller('behaviorCtrl', ['$scope', '$stateParams', // The following is the constructor function for this page's controller. See https://docs.angularjs.org/guide/controller
// You can include any angular dependencies as parameters for this function
// TIP: Access Route Parameters for your page via $stateParams.parameterName
function ($scope, $stateParams) {


}])

.controller('knowledge_testCtrl', ['$scope', '$stateParams', // The following is the constructor function for this page's controller. See https://docs.angularjs.org/guide/controller
// You can include any angular dependencies as parameters for this function
// TIP: Access Route Parameters for your page via $stateParams.parameterName
function ($scope, $stateParams) {


}])

.controller('diagnosisCtrl', ['$scope', '$stateParams', // The following is the constructor function for this page's controller. See https://docs.angularjs.org/guide/controller
// You can include any angular dependencies as parameters for this function
// TIP: Access Route Parameters for your page via $stateParams.parameterName
function ($scope, $stateParams) {


}])