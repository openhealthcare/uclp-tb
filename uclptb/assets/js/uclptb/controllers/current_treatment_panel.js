angular.module('opal.controllers').controller('CurrentTreatmentPanelCtrl', function(treatmentUtils){
  "use strict";
  this.getActiveTreatments = treatmentUtils.getActiveTreatments;
});
