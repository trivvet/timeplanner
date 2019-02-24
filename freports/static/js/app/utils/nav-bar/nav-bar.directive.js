'use strict';

angular.module('navBar').
    directive('navBar', function($location, $rootScope) {
        return {
            restrict: "E",
            templateUrl: '/api/templates/nav-bar.html',
            link: function (scope, element, attr) {
                // var getElements = [];
                // scope.getElements = Post.query();
                // scope.selectItem = function($item, $model, $label) {
                //     $location.path('/blog/' + $item.id); 
                //     scope.blogFilter = "";      
                // }
                // scope.searchItem = function(){
                //     $location.path('/blog').search('q', scope.blogFilter);
                //     scope.blogFilter = ""; 
                // }
                
                // scope.loggedIn = false;
                // scope.$watch(function(){
                //     var tokenExist = $cookies.get('token');
                //     if (tokenExist) {
                //         scope.loggedIn = true;
                //         scope.username = $cookies.get('username')
                //     } else {
                //         scope.loggedIn = false;
                //     }
                // });
                // scope.loggingOut = function() {
                //     scope.loggedIn = false;
                //     scope.username = "";
                //     $cookies.remove("token");
                //     $cookies.remove("username");
                // }
                
            }
        }
    });