angular.module('app.controllers', [])

.controller('signupCtrl', ['$scope', '$stateParams', '$http', '$state', '$rootScope',
    
    function ($scope, $stateParams, $http, $state, $rootScope) {
        var offline_debug = false;
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
        var offline_debug = false;

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

    $rootScope.logout = function(){
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
}])

