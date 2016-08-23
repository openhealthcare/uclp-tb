angular.module('opal.controllers').controller('TreatmentFormCtrl', function(
  $scope, $cookieStore, $timeout, $modalInstance, $modal, $q,
  ngProgressLite, $controller, profile, item, metadata,
  referencedata, episode
) {
      "use strict";

      var parentCtrl = $controller("EditItemCtrl", {
          $scope: $scope,
          $modalInstance: $modalInstance,
          episode: episode,
          metadata: metadata,
          referencedata: referencedata,
          item: item,
          profile: profile
      });
      var vm = this;
      _.extend(vm, parentCtrl);

      $scope.stopTreatment = function(){
          $scope.editing.treatment.end_date = new Date();
      };

      $scope.showStopTreatment = !$scope.editing.treatment.end_date || moment($scope.editing.treatment.end_date).isAfter(moment(), "days");
});
