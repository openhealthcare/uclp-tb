angular.module('opal.services').service('treatmentUtils', function(FieldTranslater){
    "use strict";
    var self = this;
    self.getStopDate = function(treatment){
      var endDate;
      if(!treatment.planned_end_date || !treatment.end_date){
        return treatment.planned_end_date || treatment.end_date;
      }
      else if(treatment.end_date.isBefore(treatment.planned_end_date)){
        return treatment.end_date;
      }
      else{
        return treatment.planned_end_date;
      }
    }

    self.getActiveTreatments = function(treatments){
      // active treatments are treatments that are between the start date and the planned_end_date
      // or between the start date and the end date, whichever is sooner
      var activeTreatments = [];
      var now = moment();

      _.each(treatments, function(treatment){
        treatment = FieldTranslater.subRecordToJs(treatment, "treatment");
        var endDate = self.getStopDate(treatment);
        if(!now.isBefore(treatment.start_date, "d")){
          if(endDate.isAfter(now, "d")){
            activeTreatments.push(treatment);
          }
        }
      });

      return activeTreatments;
    };
});
