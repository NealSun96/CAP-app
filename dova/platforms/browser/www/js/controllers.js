angular.module('app.controllers', [])
  
.controller('signupCtrl', ['$scope', '$stateParams', // The following is the constructor function for this page's controller. See https://docs.angularjs.org/guide/controller
// You can include any angular dependencies as parameters for this function
// TIP: Access Route Parameters for your page via $stateParams.parameterName
function ($scope, $stateParams) {


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

        $http.get("https://nealsun.ngrok.io/api/v1/login/", config).then(function successCallback(response) {
            $rootScope.api_auth = $scope.username + ":" + response.data.objects[0].api_key;
            $state.go('dashboard');
        }, function errorCallback(response) {
            $scope.username = "ERROR";
        });
    }
}])

.controller('courseOneCtrl', ['$scope', '$stateParams', '$http', '$rootScope', '$state',
function ($scope, $stateParams, $http, $rootScope, $state) {
    $scope.loadAssignments = function() {
        var len = $rootScope.enrollments.length;
        for (var i = 0; i < len; i++) {
            if ($rootScope.enrollments[i].id == $rootScope.enrollment_in_handle) {
                $scope.enrollment = $rootScope.enrollments[i];
            }
        }
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

        $http.get("https://nealsun.ngrok.io/api/v1/enrollment/enrollments/", config)
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
