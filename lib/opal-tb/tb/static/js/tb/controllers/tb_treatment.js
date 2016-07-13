angular.module('opal.controllers').controller('TBTreatmentCtrl',
function($modal, $q, ngProgressLite, $controller, scope, step, episode) {
      "use strict";

    var existing_smear_test = _.find(episode.investigation, function(e){
      return e.test === "Smear";
    });

    scope.localEditing = {};
    var smearId;
    var smearConsistencyToken;
    var cultureId;
    var cultureConsistencyToken;
    var diagnosisId;
    var diagnosisConsistencyToken;

    var tests = [
      "Sputum Culture",
      "Smear",
      "Gene Expert"
    ];
    scope.tests = [];

    _.each(tests, function(testTitle){
        var test = _.find(episode.investigation, function(e){
            return e.test === testTitle;
        });

        if(!test){
            test = {test: testTitle, result: "Not Done"};
        }
        scope.tests.push(test);
    });

    scope.localEditing.hasPulmonary = false;
    scope.localEditing.otherSites = false;

    var hasPulmonary = function(){
      return _.contains(scope.editing.tb_location.sites, "Pulmonary");
    };

    scope.pulmonaryChange = function(){
        var contains = hasPulmonary();

        if(!contains && scope.localEditing.hasPulmonary){
          scope.editing.tb_location.sites.push("Pulmonary");
        }
        else if(!scope.localEditing.hasPulmonary){
          scope.editing.tb_location.sites = _.without(scope.editing.tb_location.sites, "Pulmonary");
        }
    };

    scope.sitesChange = function(){
        var contains = hasPulmonary();

        if(contains && !scope.localEditing.hasPulmonary){
            scope.localEditing.hasPulmonary = true;
        }
        else if(!contains){
            scope.localEditing.hasPulmonary = false;
        }
    };

    // initialise the check box
    scope.sitesChange();

    if(episode.diagnosis.length){
        if(episode.diagnosis[0].condition.indexOf("Extra") !== -1){
            scope.localEditing.pulmonary = "Extra-Pulmonary TB";
        }
        else{
            scope.localEditing.pulmonary = "Pulmonary TB";
        }
        diagnosisId = episode.diagnosis[0].id;
        diagnosisConsistencyToken = episode.diagnosis[0].consistency_token
        scope.localEditing.site = episode.diagnosis[0].details;
    }

    scope.preSave = function(editing){
        editing.investigation = [];
        _.each(scope.tests, function(test){
          editing.investigation.push(test);
        });
        editing.diagnosis = [];
        editing.diagnosis = {
          condition: editing.stage + ' ' + scope.localEditing.pulmonary,
          details: scope.localEditing.site,
          id: diagnosisId,
          consistency_token: diagnosisConsistencyToken
         };
    };
});
