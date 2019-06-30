'use strict';

angular.module('sideBar').
    directive('sideBar', function($location, $rootScope, $cookies) {
        return {
            restrict: "E",
            templateUrl: '/api/templates/side-bar.html',
            link: function (scope, element, attr) {
                
            }
        }
    });