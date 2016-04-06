'use strict';

/**
 * @ngdoc function
 * @name fridgesApp.controller:MainCtrl
 * @description
 * # HistoryCtrl
 * Controller of the fridgesApp
 */
angular.module('fridgesApp')
    .controller('HistoryCtrl', ['$scope', 'historyFactory', function($scope, historyFactory) {

        $scope.showData = false;
        $scope.message = 'Loading ...';
        historyFactory.getReadings().query(
            function(response) {
                $scope.readings = response;
                $scope.showData = true;
            },
            function(response) {
                $scope.message = 'Error: ' + response.status + ' ' + response.statusText;
            });

    }]);
