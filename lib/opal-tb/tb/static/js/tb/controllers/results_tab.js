angular.module('opal.controllers').controller('resultsTabCtrl',
  function($scope, $modal) {
    "use strict";

    $scope.orderedTests = function(){
      return $modal.open({
          controller : 'ModalPathwayController',
          templateUrl: '/templates/pathway/pathway_detail.html',
          size       : 'lg',
          resolve    :  {
            episode: function(){ return $scope.episode; },
            pathwaySlug: function(){ return 'tests_ordered_pathway'; },
          }
        }).result.then(function(episode){
            $scope.episode.test_result = episode.test_result;
        });
    };

    $scope.resultsReceived = function(){
      return $modal.open({
          controller : 'ModalPathwayController',
          templateUrl: '/templates/pathway/pathway_detail.html',
          size       : 'lg',
          resolve    :  {
            episode: function(){ return $scope.episode; },
            pathwaySlug: function(){ return 'results_received_pathway'; },
          }
        }).result.then(function(episode){
            $scope.episode.test_result = episode.test_result;
        });
    };
});
