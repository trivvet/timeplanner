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
                when("/reports/:id", {
                    template: "<report-detail></report-detail>"
                }).
                when("/login", {
                    template: "<login-detail></login-detail>"
                }).
                when("/logout", {
                    redirectTo: "/login"
                }).
                otherwise({
                    template: "<h1>Not Found</h1>"
                });
        }
    );

