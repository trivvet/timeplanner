'use strict';

angular.module('report').
    factory('Report', function($resource){

        var url = '/api/freports/:id';

        return $resource(url, {}, {
            query: {
                method: 'GET',
                params: {},
                isArray: true,
                cache: true,
                transformResponse: function (data) { 
                    return angular.fromJson(data);
                }
            },
        })
    })