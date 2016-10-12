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
    };

    self.getTreatmentIndexFromId = function(treatment, treatments){
        return _.findIndex(treatments, function(t){
            return t.id === treatment.id;
        });
    };

    self.getActiveTreatments = function(treatments){
      // if the page has loaded, cache the result of the function
      // so it never changes on update
      if(treatments.length){
        return self._getActiveTreatments(treatments);
      }

    };

    self._getActiveTreatments = _.once(function(treatments){
      // active treatments are treatments that are between the start date and the planned_end_date
      // or between the start date and the end date, whichever is sooner
      var activeTreatments = [];
      var now = moment();

      _.each(treatments, function(treatment){
        treatment = FieldTranslater.subRecordToJs(treatment, "treatment");
        var endDate = self.getStopDate(treatment);
        var start_date = treatment.start_date || treatment.created;
        if(!now.isBefore(start_date, "d")){
          if(!endDate || endDate.isAfter(now, "d")){
            activeTreatments.push(treatment);
          }
        }
      });

      return activeTreatments;
    });
});
