angular.module('opal.controllers').controller('CurrentTreatmentPanelCtrl', function(treatmentUtils){
  this.getActiveTreatments = treatmentUtils.getActiveTreatments;
});
