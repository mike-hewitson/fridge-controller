'use strict';

function getSensorByName(name, sensors) {
    return sensors.filter(
        function(sensor) {
            return sensor.sensor === name;
        }
    );
}

function buildRows(sensor, readings) {
    var rows = [];

    for (var reading of readings) {
        var data = getSensorByName(sensor, reading.sensors)[0];
        rows.push({ c: [{ v: new Date(reading.date) }, { v: data.temp }, { v: data.hum }] });
    }
    return rows;
}

function buildChart(sensor, readings) {
    var chartObject = {};
    var cols = [
        { id: 't', label: 'Date', type: 'string' },
        { id: 's', label: 'Temperature', type: 'number' },
        { id: 's', label: 'Humidity', type: 'number' }
    ];
    var rows = buildRows(sensor, readings);
    var title = sensor + ' Conditions';
    chartObject.type = 'LineChart';
    chartObject.data = {
        'cols': cols,
        'rows': rows
    };

    chartObject.options = {
        'title': title,
        series: {
            0: { targetAxisIndex: 0, type: 'line' },
            1: { targetAxisIndex: 1, type: 'line' }
        },
        vAxes: [
            { title: 'Degrees C' },
            { title: 'Percentage' }
        ]
    };
    return chartObject;

}

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

                // Build chart objects
                $scope.chartObject1 = buildChart('Ambient', $scope.readings);
                $scope.chartObject2 = buildChart('Curing', $scope.readings);
                $scope.chartObject3 = buildChart('Fridge', $scope.readings);


            },
            function(response) {
                $scope.message = 'Error: ' + response.status + ' ' + response.statusText;
            });

    }]);
