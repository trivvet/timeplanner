'use strict';

angular.module('showSidebar').
    directive('showSidebar', function() {
        return {
            restrict: "A",
            link: function (scope, element, attr) {
                element.bind('click', function(event) {
                    console.log("OK");
                });
                // var msg = attr.confirmClick || "Are you sure?";
                // var clickAction = attr.confirmedClick;
                // element.bind('click', function (event) {
                //     event.stopImmediatePropagation();
                //     event.preventDefault();
                //     if ( window.confirm(msg) ) {
                //         scope.$eval(clickAction);
                //     } else {
                //         console.log("Cancelled"); 
                //     }
                // });
            }
        }
    });