'use strict';

/**
 * @ngdoc function
 * @name fridgesApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the fridgesApp
 */
angular.module('fridgesApp')
    .controller('MainCtrl', ['$scope', 'currentFactory', function($scope, currentFactory) {
        this.awesomeThings = [
            'HTML5 Boilerplate',
            'AngularJS',
            'Karma'
        ];

        this.message = 'asasas';
        $scope.showCurrent = false;
        $scope.message = 'Loading ...';
        currentFactory.getCurrent().query(
            function(response) {
                $scope.reading = response[0];
                $scope.showCurrent = true;
            },
            function(response) {
                $scope.message = 'Error: ' + response.status + ' ' + response.statusText;
            });

    }]);
