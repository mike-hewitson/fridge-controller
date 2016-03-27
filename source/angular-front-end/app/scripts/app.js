'use strict';

angular.module('charcuterieApp', [])

.controller('CharcuterieController', ['$scope', function($scope) {

    $scope.tab = 1;
    $scope.filtText = '';

    $scope.reading = {
        date: new Date().toISOString(),
        sensors: [{
                sensor: "Ambient",
                temp: 55,
                hum: 24
            },
            { sensor: "Fridge", temp: 55, hum: 24 }, 
            {
                sensor: "Curing",
                temp: 55,
                hum: 24
            }
        ]
    };


    $scope.select = function(setTab) {
        $scope.tab = setTab;

        if (setTab === 2) {
            $scope.filtText = "appetizer";
        } else if (setTab === 3) {
            $scope.filtText = "mains";
        } else if (setTab === 4) {
            $scope.filtText = "dessert";
        } else {
            $scope.filtText = "";
        }
    };

    $scope.isSelected = function(checkTab) {
        return ($scope.tab === checkTab);
    };

}])

;
