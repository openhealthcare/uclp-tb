angular.module('opal.controllers').controller('ObserveDOTCtrl',
 function(scope, $templateRequest, treatmentUtils, step, episode) {
   "use strict";
   var now = moment();

   scope.makeObservedTreatmentFromTreatment = function(treatment, date){
     return {
       drug: treatment.drug,
       dose: treatment.dose,
       observed: undefined,
       date: date,
       treatment: treatment
     };
   };

   scope.initialise = function(){
     scope.editing.observed_treatment = _.filter(scope.editing.observed_treatment, function(x){
       return x.drug && x.drug.length;
     });

     /*
     * we need to build up all missing observed treatments
     * if they haven't been for a few days we need
     * to build that history
     */
    _.each(scope.episode.treatment, function(treatment){
      var daysSince = now.diff(treatment.start_date, "d");
      var stopDate = treatmentUtils.getStopDate(treatment);
      var observedTreatments = _.clone(scope.editing.observed_treatment);

      _.times(daysSince, function(since){
        var forDate = moment(treatment.start_date).add(since, "d");
        if(forDate.isBefore(stopDate, "d")){
          var ot = _.find(observedTreatments, function(ot){
            var sameDay = moment(ot.date).isSame(forDate, "d");
            var sameDrug = ot.drug === treatment.drug;
            var sameDose = ot.dose === treatment.dose;
            return sameDay && sameDrug && sameDose;
          });

          if(!ot){
            scope.editing.observed_treatment.push(
              scope.makeObservedTreatmentFromTreatment(treatment, forDate)
            );
          }
        }
      });
    });

    scope.editing.observed_treatment = _.filter(scope.editing.observed_treatment, function(ot){
        return !_.isBoolean(ot.observed) || scope.isCurrent(ot);
    });

    scope.editing.observed_treatment = _.sortBy(scope.editing.observed_treatment, function(ot){
      return moment(ot.date).startOf('day');
    });

    scope.withUnobserved = false;

    scope.hasUnobserved = !!_.find(scope.editing.observed_treatment, function(ot){
      return !scope.isCurrent(ot);
    });
   };

   scope.showUnobserved = function(){
     scope.withUnobserved = !scope.withUnobserved;
   };

   scope.observeAllActiveTreatments = function(){
     if(!scope.withUnobserved){
       _.each(scope.editing.observed_treatment, function(ot){
         if(scope.isCurrent(ot)){
           ot.observed = true;
         }
       });
     }
     else{
       _.each(scope.editing.observed_treatment, function(ot){
           ot.observed = true;
       });
     }
   };

   scope.isCurrent = function(item){
     return !item.date || now.isSame(moment(item.date), "d");
   };

   scope.preSave = function(editing){
      editing.observed_treatment = _.filter(editing.observed_treatment, function(ot){
        return ot.date;
      });

      _.each(editing.observed_treatment, function(ot){
          delete ot.treatment;
      });
   };



   scope.initialise();
 }
);
