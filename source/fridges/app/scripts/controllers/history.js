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

    }])
    .controller('HistoryChartCtrl', ['$scope', 'historyFactory', function($scope, historyFactory) {

        $scope.showData = false;
        $scope.message = 'Loading ...';
        historyFactory.getReadings().query(
            function(response) {
                $scope.readings = response;
                $scope.showData = true;
                $scope.rows = [];

                for (var reading of $scope.readings) {
                    $scope.rows.push({ c: [{ v: new Date(reading.date) }, { v: reading.sensors[0].temp }, { v: reading.sensors[0].hum }] });
                }

                console.log($scope.rows);

                $scope.chartObject = {};

                $scope.chartObject.type = 'LineChart';

                $scope.chartObject.data = {
                    'cols': [
                        { id: 't', label: 'Topping', type: 'string' },
                        { id: 's', label: 'Temperature', type: 'number' },
                        { id: 's', label: 'Humidity', type: 'number' }
                    ],
                    'rows': $scope.rows 
                };

                $scope.chartObject.options = {
                    'title': 'Ambient'
                };

            },
            function(response) {
                $scope.message = 'Error: ' + response.status + ' ' + response.statusText;
            });

    }]);
