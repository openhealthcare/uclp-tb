angular.module('opal.controllers').controller('TBTreatmentCtrl',
function( $modal, $q, ngProgressLite, $controller, scope, step, episode) {
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

    if(existing_smear_test){
      scope.localEditing.smear_tests = existing_smear_test.result;
      smearId = existing_smear_test.id;
      smearConsistencyToken = existing_smear_test.consistency_token;
    }
    else{
      scope.localEditing.smear_tests = 'Not Done';
    }

    var existing_culture_test = _.find(episode.investigation, function(e){
      return e.test === "Sputum Culture";
    });

    if(existing_culture_test){
      scope.localEditing.culture_tests = existing_culture_test.result;
      cultureId = existing_culture_test.id;
      cultureConsistencyToken = existing_culture_test.consistency_token;
    }
    else{
      scope.localEditing.culture_tests = 'Not Done';
    }

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
