'use strict';

angular.
    module('core.interceptors').
        factory("LoginRequiredInterceptor", function($cookies, $location){
            return function(response) {
                if (response.status == 401) {
                    var currentPath = $location.path();
                    $location.path("/login");
                    
                }
            }
        });

  