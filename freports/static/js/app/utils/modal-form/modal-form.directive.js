'use strict';

angular.module('modalForm').
    directive('modalForm', function($location, $rootScope) {
        return {
            restrict: "E",
            templateUrl: '/api/templates/modal-form.html',
            link: function (scope, element, attr) {
                
            }
        }
    });