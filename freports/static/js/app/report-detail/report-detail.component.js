'use strict';

angular.module('reportDetail').
    component('reportDetail', {
        templateUrl: "/api/templates/report-detail.html",
        controller: function(Report, $location,
            $routeParams, $cookies, $scope){
            Report($cookies.get('token')).get({id: $routeParams.id}, function(data){
                $scope.report = data;
                $scope.plaintiffs = $scope.report.participants.filter(function(person) {
                    if (person.status == 'plaintiff') {
                        return person;
                    }
                });
                $scope.defendants = $scope.report.participants.filter(function(person) {
                    if (person.status == 'defendant') {
                        return person;
                    }
                });
            });

            $scope.backToList = function() {
                 $location.path('/');
            };
        }
    });