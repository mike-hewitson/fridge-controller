'use strict';

angular.module('fridgesApp')
    .constant('baseURL', 'http://localhost:3000/')
    .service('currentFactory', ['$resource', 'baseURL', function($resource, baseURL) {

        this.getCurrent = function() {
            return $resource(baseURL + 'current/:id', null, { 'update': { method: 'PUT' } });
        };

    }])
    .service('historyFactory', ['$resource', 'baseURL', function($resource, baseURL) {

        this.getReadings = function() {
            return $resource(baseURL + 'readings/:id', null, { 'update': { method: 'PUT' } });
        };

    }])

    ;
