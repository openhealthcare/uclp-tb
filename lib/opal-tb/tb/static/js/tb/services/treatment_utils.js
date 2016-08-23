angular.module('opal.services').service('treatmentUtils', function(){
    "use strict";
    this.getActiveTreatments = function(treatments){
      // active treatments are treatments that are between the start date and the planned_end_date
      // or between the start date and the end date, whichever is sooner
      var activeTreatments = [];
      var now = moment();

      _.each(treatments, function(treatment){
        var endDate;
        if(!treatment.planned_end_date || !treatment.end_date){
          endDate = treatment.planned_end_date || treatment.end_date;
        }
        else if(treatment.end_date.isBefore(treatment.planned_end_date)){
          endDate = treatment.end_date;
        }
        else{
          endDate = treatment.planned_end_date;
        }

        if(!now.isBefore(treatment.start_date, "d")){
          if(endDate.isAfter(now, "d")){
            activeTreatments.push(treatment);
          }
        }
      });

      return activeTreatments;
    };
});
