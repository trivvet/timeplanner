'use strict';

angular.module('report').
    factory('Report', function($resource, $cookies){

        var url = '/api/freports/', token = $cookies.get("token");

        if (token) {
            var reportSaveToken = {authorization: "JWT " + token};
        } else {
            console.log("No token");
        }

        return $resource(url, {}, {
            query: {
                url: url,
                method: 'GET',
                params: {},
                isArray: true,
                cache: true,
                transformResponse: function (data) { 
                    return angular.fromJson(data);
                }
            },
            get: {
                url: url + ":id/",
                method: 'GET',
                params: {'id': '@id'},
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
                headers: reportSaveToken,
            }
        });
    });