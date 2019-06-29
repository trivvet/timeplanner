'use strict';

angular.module('reports', [
    // external
    'ngResource',
    'ngRoute',
    'angularUtils.directives.dirPagination',
    'ngCookies',
    
    // internal
    'reportList',
    'reportDetail',
    'navBar',
    'sideBar',
    'loginDetail',
    ]);