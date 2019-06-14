'use strict';

angular.module('reportDetail').
    component('reportDetail', {
        templateUrl: "/api/templates/report-detail.html",
        controller: function(Report, $location,
            $routeParams, $scope){
            
            Report.query(function(data){
                $scope.notFound = true;
                data.forEach(function(report) {
                    if (report.id == $routeParams.id) {
                        $scope.report = report;
                        $scope.notFound = false;
                    }
                });
            });

            if ($scope.notFound) {
                $location.path("/404");
            }
        }
    });