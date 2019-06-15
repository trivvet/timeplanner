'use strict';

angular.module('reportDetail').
    component('reportDetail', {
        templateUrl: "/api/templates/report-detail.html",
        controller: function(Report, $location,
            $routeParams, $scope){
            Report.get({id: $routeParams.id}, function(data){
                $scope.report = data;
            });
        }
    });