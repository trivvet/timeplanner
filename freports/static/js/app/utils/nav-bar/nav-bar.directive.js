'use strict';

angular.module('navBar').
    directive('navBar', function($location, $rootScope, $cookies, $http) {
        return {
            restrict: "E",
            templateUrl: '/api/templates/nav-bar.html',
            link: function (scope, element, attr) {
                scope.hideNavBars = false;
                scope.$watch(function(){
                    scope.hideNavBars = false;
                    var token = $cookies.get("token");
                    if (!token) {
                        scope.hideNavBars = true;
                    }
                });
                
                
            }
        }
    });