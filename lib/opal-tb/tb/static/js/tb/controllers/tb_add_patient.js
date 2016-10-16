angular.module('opal.controllers').controller('TBAddPatientCtrl',
function(scope, step, episode) {
  "use strict";

  scope.populatedDemographics = function(){
    var personalFields = ["date_of_birth", "first_name", "surname"]

    if(scope.editing.demographics){
      return _.all(personalFields, function(pf){
        return scope.editing.demographics[pf];
      });
    }
    else{
      return false;
    }
  };

  scope.valid = function(form){
    // do all our valid checks ie demogaphics etc
    var hasHn;

    if(scope.editing.demographics){
      if(scope.editing.demographics.hospital_number){
        hasHn = true;
      }
    }

    if(form.demographics_hospital_number){
      if(!scope.populatedDemographics() || !hasHn){
        form.demographics_hospital_number.$setValidity('no_personal_info', false);
      }
      else{
        form.demographics_hospital_number.$setValidity('no_personal_info', true);
      }
    }

    return form;
  };
});
