'use strict';

angular.module('reports', [
    // external
    'ngResource',
    'ngRoute',
    'angularUtils.directives.dirPagination',
    
    // internal
    'reportList',
    'reportDetail',
    'navBar',
    'sideBar',
    'modalForm'
    ]);