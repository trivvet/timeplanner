'use strict';

angular.module('loginDetail').
    component('loginDetail', {
        templateUrl: "/api/templates/login-detail.html",
        controller: function($location, $routeParams, $scope, $http, $cookies){
            var loginUrl = "/api/auth/token/";
            $scope.user = {
                username: null,
                password: null
            }
            var tokenExist = $cookies.get("token");
            var username = $cookies.get("username");
            if (tokenExist) {
                $cookies.remove("token");
                $scope.user = {
                    username: $cookies.get("username")
                }
            }
            $scope.doLogin = function(user) {
                var reqConfig = {
                    method: "POST",
                    url: loginUrl,
                    data: {
                        username: user.username,
                        password: user.password
                    },
                    headers: {}
                }
                $http(reqConfig)
                .then(function successCallback(response) {
                    $cookies.put("token", response.data.token); 
                    $cookies.put("username",user.username);
                    console.log(response.data.token)
                    $location.path("/");
                }, function errorCallback(response) {
                    console.log(response.data);
                    console.log(response.status);
                });
            }
        }
    });