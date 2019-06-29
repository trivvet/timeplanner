'use strict';

angular.module('loginDetail').
    component('loginDetail', {
        templateUrl: "/api/templates/login-detail.html",
        controller: function($location, $routeParams, $scope){
            console.log("login");
        }
    });