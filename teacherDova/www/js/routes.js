angular.module('app.routes', [])

.config(function($stateProvider, $urlRouterProvider) {

  // Ionic uses AngularUI Router which uses the concept of states
  // Learn more here: https://github.com/angular-ui/ui-router
  // Set up the various states which the app can be in.
  // Each state's controller can be found in controllers.js
  $stateProvider

  .state('signup', {
    url: '/signup',
    templateUrl: 'templates/signup.html',
    controller: 'signupCtrl'
  })

  .state('login', {
    url: '/login',
    templateUrl: 'templates/login.html',
    controller: 'loginCtrl'
  })

  .state('edit_course', {
    url: '/edit_course',
    templateUrl: 'templates/edit_course.html',
    controller: 'edit_courseCtrl'
  })

  .state('dashboard', {
    url: '/dash',
    templateUrl: 'templates/dashboard.html',
    controller: 'dashboardCtrl'
  })

  .state('edit_behaviour', {
    url: '/edit_behaviour',
    templateUrl: 'templates/edit_behaviour.html',
    controller: 'edit_behaviourCtrl'
  });

$urlRouterProvider.otherwise('/login')

  

});