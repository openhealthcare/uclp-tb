angular.module('opal.controllers').controller('TBDiagnosis', function(scope, step, episode){
  var tbTypeToStage = {
      "Active": "Active TB Treatment",
      "Latent": "Latent TB Treatment",
      "NTM": "NTM Treatment"
  }
  "use strict";

  var stageToTbType = _.invert(tbTypeToStage);
  var diagnosisId;
  var diagnosisConsistencyToken;
  scope.tbTypes = _.keys(tbTypeToStage);
  scope.localEditing = {condition: stageToTbType[episode.stage]};

  scope.editing.stage = [tbTypeToStage[scope.localEditing.condition]];

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
    editing.diagnosis = [];
    editing.diagnosis = {
      condition: scope.localEditing.condition,
      details: scope.localEditing.site,
      id: diagnosisId,
      consistency_token: diagnosisConsistencyToken
     };
     editing.stage = [tbTypeToStage[scope.localEditing.condition]];
  }
});
