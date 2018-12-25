'use strict';

angular.module('reports').
    config(
        function(
            $locationProvider,
            $resourceProvider,
            $routeProvider
            ){

            $locationProvider.html5Mode({
                enabled: true,
            });
            $resourceProvider.defaults.stripTrailingSlashes = false;
            $routeProvider.
                when("/", {
                    template: "<all-list></all-list>"
                }).
                otherwise({
                    template: "<h1>Not Found</h1>"
                })
        }
    );