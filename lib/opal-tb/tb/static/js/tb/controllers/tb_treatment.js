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
        editing.investigation[0] = {test: 'Smear', result: scope.localEditing.smear_tests, id: smearId, consistency_token: smearConsistencyToken};
        editing.investigation[1] = {test: 'Sputum Culture', result: scope.localEditing.culture_tests, id: cultureId, consistency_token: cultureConsistencyToken};
        editing.diagnosis = [];
        editing.diagnosis = {
          condition: editing.stage + ' ' + scope.localEditing.pulmonary,
          details: scope.localEditing.site,
          id: diagnosisId,
          consistency_token: diagnosisConsistencyToken
         };
    };
});
