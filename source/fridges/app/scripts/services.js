'use strict';

angular.module('fridgesApp')
    .constant('baseURL', 'http://192.168.1.126:3000/')
    .service('currentFactory', ['$resource', 'baseURL', function($resource, baseURL) {

        this.getCurrent = function() {
            return $resource(baseURL + 'readings/latest/');
        };

    }])
    .service('historyFactory', ['$resource', 'baseURL', function($resource, baseURL) {

        this.getReadings = function() {
            return $resource(baseURL + 'readings/:id', null, { 'update': { method: 'PUT' } });
        };

        this.getToday = function() {
            return $resource(baseURL + 'readings/today/');
        };
    }])

    ;
