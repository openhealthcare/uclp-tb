angular.module('opal.controllers').controller('ContactTracingFormCtrl',
  function(Options, $controller, recordLoader, step, scope, episode) {
    "use strict";
    var vm = this;
    var stepNames = ['contact_details', 'demographics', 'contact_tracing'];
    var key = step.api_name;

    // we need a better way of doing this
    // this comes in when we fix the scope
    // in pathways

    var parentCtrl = $controller("MultiSaveCtrl", {
        scope: scope,
        episode: episode,
        step: step
    });

    _.extend(vm, parentCtrl);

    scope.instanceName = "Person";

    scope.addAnother = function(){
        var cleanObject = {};
        _.each(stepNames, function(stepName){
          cleanObject[stepName] = {};
        });
        scope.allEditing.push(cleanObject);
    };

    scope.init = function(){
      recordLoader.then(function(recordschema){
        var stepNamesToFields = _.reduce(stepNames, function(memo, stepName){
            memo[stepName] = _.map(recordschema[stepName].fields, function(field){
                return field.name;
            });

            return memo;
        }, {});

        // we just want the following fields from contact tracing
        stepNamesToFields.contact_tracing = [
          "reason_at_risk", "relationship_to_index", "contact_episode_id", "id"
        ];
        scope.allEditing = _.map(episode[key], function(row){
            var result = {};
            _.each(stepNames, function(stepName){
              result[stepName] = {};
            });
            _.each(stepNames, function(stepName){
              _.each(stepNamesToFields[stepName], function(field){
                  result[stepName][field] = row[field];
              });
            });



            return result;
        });

        scope.addAnother();
      });
    };

    scope.consolidate = function(){
      return _.map(scope.allEditing, function(row){
          var consolidatedRow = {};
          _.each(stepNames, function(stepName){
              _.extend(consolidatedRow, row[stepName]);
          });
          return consolidatedRow;
      });
    };

    scope.preSave = function(editing){
      editing[step.api_name] = scope.consolidate();
    };

    scope.init();
});
