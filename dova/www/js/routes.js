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

  .state('courseOne', {
    url: '/CourseOne',
    templateUrl: 'templates/courseOne.html',
    controller: 'courseOneCtrl'
  })

  .state('dashboard', {
    url: '/dash',
    templateUrl: 'templates/dashboard.html',
    controller: 'dashboardCtrl'
  })

  .state('feedback', {
    url: '/feedback',
    templateUrl: 'templates/feedback.html',
    controller: 'feedbackCtrl'
  })

  .state('behavior', {
    url: '/behavior',
    templateUrl: 'templates/behavior.html',
    controller: 'behaviorCtrl'
  })

  .state('knowledge_test', {
    url: '/knowledge_test',
    templateUrl: 'templates/knowledge_test.html',
    controller: 'knowledge_testCtrl'
  })
  
  .state('diagnosis', {
    url: '/diagnosis',
    templateUrl: 'templates/diagnosis.html',
    controller: 'diagnosisCtrl'
  })

  .state('check_knowledge_test', {
    url: '/check_knowledge_test',
    templateUrl: 'templates/check_knowledge_test.html',
    controller: 'check_knowledge_testCtrl'
  });

$urlRouterProvider.otherwise('/login')

  

});