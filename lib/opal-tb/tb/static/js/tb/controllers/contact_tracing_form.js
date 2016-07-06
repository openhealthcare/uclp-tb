angular.module('opal.controllers').controller('ContactTracingFormCtrl',
  function(Options, $controller, step, scope, episode) {
    "use strict";
    var vm = this;
    var stepNames = ['contact_details', 'demographics'];

    // we need a better way of doing this
    // this comes in when we fix the scope
    // in pathways
    scope.editing.demographics = {};
    scope.editing.contact_details = {};

    var parentCtrl = $controller("MultiSaveCtrl", {
        scope: scope,
        episode: episode,
        step: step
    });

    _.extend(vm, parentCtrl);

    if(episode && episode.contact_tracing && episode.contact_tracing.length){
      vm.multipleModels = angular.copy(episode[step.api_name]);
    }

    if(episode && episode[step.api_name] && episode[step.api_name].length > 1){
        vm.multipleModels = angular.copy(episode[step.api_name]);
        var editing_field = scope.editing[step.api_name];
        vm.cleanModel(editing_field);
    }

    vm.consolidate = function(editing){
      var combined = {};
      _.each(stepNames, function(stepName){
        _.extend(combined, editing[stepName]);
      });

      return combined;
    };

    vm.allClean = function(editing){
      var clean = true;
      _.each(stepNames, function(stepName){
        var editingField = scope.editing[stepName];
        clean = clean && vm.isClean(editingField);
      });

      return clean;
    }

    vm.addAnother = function(){
      var clean = true;
      _.each(stepNames, function(stepName){
        var editingField = scope.editing[stepName];
        clean = clean && vm.isClean(editingField);
      });

      if(!vm.allClean(scope.editing)){
        vm.multipleModels.push(vm.consolidate(scope.editing));
      }

      _.each(stepNames, function(stepName){
        vm.cleanModel(scope.editing[stepName]);
      });
    };

    vm.toSave = function(editing){
      var all_models = angular.copy(vm.multipleModels);
      if(!vm.allClean(editing)){
        all_models.push(vm.consolidate(editing));
      }
      editing.contact_tracing = all_models;
      editing.demographics = [];
      editing.contact_details = [];
    };
});
