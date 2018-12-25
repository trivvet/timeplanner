'use strict';

angular.module('reportList').
    component('allList', {
        templateUrl: "/api/templates/report-list.html",
        controller: function(Report, $location,
            $routeParams, $rootScope, $scope){

            Report.query(function(data){
                $scope.items = data;
            })
        }
    })