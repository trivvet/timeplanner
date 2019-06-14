'use strict';

angular.module('reportList').
    component('allList', {
        templateUrl: "/api/templates/report-list.html",
        controller: function(Report, $location,
            $routeParams, $rootScope, $scope, $filter){
            
            $scope.navButtonClass2 = "active";
            $scope.reportItems = 15;
            $scope.propertyName = 'number';

            Report.query(function(data){
                $scope.items = data;
                $scope.activeReports = $scope.items.filter(function(item) {
                    if (item.active != false) {
                        return item;
                    }
                });
                $scope.deactivatedReports = $scope.items.filter(function(item) {
                    if (item.active == false && item.executed == false) {
                        return item;
                    }
                });
                $scope.executedReports = $scope.items.filter(function(item) {
                    if (item.executed) {
                        return item
                    }
                });
            });
            

            $scope.filterStatus = function(item) {
                if ($scope.status == "active" || !$scope.status) {
                    if (item.active && !item.executed) {
                        return item;
                    } else if (item.active != false && !item.executed) {
                        return item;
                    }
                } else if ($scope.status == "deactivate") {
                    if (item.active == false && !item.executed) {
                        return item;
                    }
                } else if ($scope.status == "executed") {
                    if (item.executed) {
                        return item;
                    }
                } else if ($scope.status == "all") {
                    return item;
                }
            }

            $scope.setStatus = function(event) {
                var elementAttributes = event.currentTarget.attributes;
                $scope.status = elementAttributes.data.value;
                $scope.reportItems = 15;
                $scope.navButtonClass1 = "";
                $scope.navButtonClass3 = "";
                $scope.navButtonClass4 = "";
                $scope.navButtonClass2 = "";
                if ($scope.status == "active") {
                    $scope.navButtonClass2 = "active";
                } else if ($scope.status == "deactivate") {
                    $scope.navButtonClass3 = "active";
                } else if ($scope.status == "executed") {
                    $scope.navButtonClass4 = "active";
                } else {
                    $scope.navButtonClass1 = "active";
                }
                $scope.listReports__currentPage = 1;
                $scope.reverse = null;
                $scope.items = $filter('orderBy')($scope.items, $scope.propertyName, $scope.reverse);
            }

            $scope.itemNumberColor = function(item) {
                if (item.active && !item.executed) {
                    return "text-success";
                } else if (!item.active && !item.executed) {
                    return "text-secondary";
                } else {
                    return "text-info";
                }
            }

            $scope.itemRowColor = function(item) {
                if (item.active != false && !item.executed && !item.active) {
                    return "table-danger";
                }
                if (item.address == '-' || item.plaintiff == '-') {
                    return "table-warning";
                } else if (item.defendant == '-' || item.object_name == '-') {
                    return "table-warning";
                } else if (item.research_kind == '-') {
                    return "table-warning";
                }
            }

            $scope.showAll = function() {
                if ($scope.reportItems != $scope.items.length) {
                    $scope.reportItems = $scope.items.length;
                } else {
                    $scope.reportItems = 15;
                }
                
            }
            
            $scope.sortBy = function(propertyName) {
                $scope.reverse = (propertyName !== null && $scope.propertyName == propertyName) ? !$scope.reverse : false;
                $scope.propertyName = propertyName;
                $scope.items = $filter('orderBy')($scope.items, $scope.propertyName, $scope.reverse);
            }

            $scope.showDetail = function(reportId) {
                 $location.path('/' + reportId);
            };
        }
    });