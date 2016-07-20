angular.module('opal.controllers').controller('TestResultsCtrl', function($scope) {
    "use strict";

    var episode = $scope.episode;
    scope.testResults = episode.test_results;

    $scope.testResults = [
      {
        name: "Smear",
        status: "Pending",
        result: ""
      },
      {
        name: "Culture",
        status: "Pending",
        result: ""
      },
      {
        name: "GeneXpert",
        status: "Pending",
        result: ""
      }
    ];

    var usualTests = function(){
      episode.newItem("testResults");
      episode.newItem('testResults');
    }

    $scope.orderUsualTests = function(){
      $scope.
    };
});
