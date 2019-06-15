'use strict';

angular.module('report').
    factory('Report', function($resource){

        var url = '/api/freports/';

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

            }
        })
    })