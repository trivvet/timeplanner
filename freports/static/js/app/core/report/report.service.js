'use strict';

angular.module('report').
    factory('Report', function($resource, $cookies, $location, $scope){

        var url = '/api/freports/', token = $cookies.get("token");

        $scope.$watch(function(){
            var token = $cookies.get("token");
        });

        return $resource(url, {}, {
            query: {
                url: url,
                method: 'GET',
                params: {},
                interceptor: {responseError: function(response) {
                    console.log(token);
                    if (response.status == 401) {
                        var currentPath = $location.path();
                        if (currentPath == "/login") {
                            $location.path("/login");
                        } else {
                            $location.path("/login").search("next", currentPath);
                        }
                        
                    }
                }},
                headers: {authorization: "JWT " + token},
                isArray: true,
                cache: true,
                transformResponse: function (data) { 
                    return angular.fromJson(data);
                },
            },
            get: {
                url: url + ":id/",
                method: 'GET',
                params: {'id': '@id'},
                headers: {authorization: "JWT " + token},
                isArray: false,
                cache: true,
                transformResponse: function (data) {
                    return angular.fromJson(data);
                }

            },
            save: {
                url: url + "create/",
                method: "POST",
                params: {},
                headers: {authorization: "JWT " + token},
            }
        });
    });