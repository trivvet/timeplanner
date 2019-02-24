'use strict';

angular.module('sideBar').
    directive('sideBar', function($location, $rootScope) {
        return {
            restrict: "E",
            templateUrl: '/api/templates/side-bar.html',
            link: function (scope, element, attr) {
                
            }
        }
    });