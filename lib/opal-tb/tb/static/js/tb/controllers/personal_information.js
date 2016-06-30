angular.module('opal.controllers').controller('PersonalInformationCtrl',
  function(Options, $controller, Item, step, scope, episode, recordLoader) {
    "use strict";
    var vm = this;
    var stepNames = ['contact_details', 'demographics', 'referral_route'];


    recordLoader.then(function(columnSchema){
      _.each(stepNames, function(stepName){
        if(episode[stepName] && episode[stepName].length){
          delete episode[stepName][0].formController;
          delete episode[stepName][0].columnName;
          scope.editing[stepName] = episode.getItem(stepName, 0);
        }
      });
    });

    var parentCtrl = $controller("MultistageDefault", {
        scope: scope,
        episode: episode,
        step: step
    });

    _.extend(vm, parentCtrl);


    vm.toSave = function(editing){
      delete editing.referral_route;
      return editing;
    };

});
