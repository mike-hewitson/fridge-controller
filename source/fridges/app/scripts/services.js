'use strict';

angular.module('fridgesApp')
    .constant('baseURL', 'http://localhost:3000/')
    .service('currentFactory', ['$resource', 'baseURL', function($resource, baseURL) {

        this.getCurrent = function() {
            return $resource(baseURL + 'current/:id', null, { 'update': { method: 'PUT' } });
        };

    }]);
