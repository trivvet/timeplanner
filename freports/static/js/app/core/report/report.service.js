'use strict';

angular.module('report').
    factory('Report', function(LoginRequiredInterceptor, $resource, $cookies, $location){

        var url = '/api/freports/';

        return function(token) {
            if (token) {
                return $resource(url, {}, {
                    query: {
                        url: url,
                        method: 'GET',
                        params: {},
                        interceptor: {responseError: LoginRequiredInterceptor},
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
            } else {
                return {
                    query: function(){
                        $location.path("/login");
                    }
                }
            }
        }
    });