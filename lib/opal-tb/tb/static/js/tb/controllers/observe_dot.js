angular.module('opal.controllers').controller('ObserveDOTCtrl',
 function(scope, $templateRequest, treatmentUtils, step, episode) {
   "use strict";
   var now = moment();

   scope.initialise = function(){

    scope.editing.observed_treatment = scope.getReleventTreatments(
      scope.editing.observed_treatment,
      scope.episode.treatment
    );

    scope.withUnobserved = false;


    scope.unobservedCount = scope.getUnobservedCount();
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
   };

   scope.makeObservedTreatmentFromTreatment = function(treatment, date){
     return {
       drug: treatment.drug,
       dose: treatment.dose,
       observed: undefined,
       date: date,
     };
   };

   /*
   * get the count of those that are not today and have not been observed
   */
   scope.getUnobservedCount = function(){
       return _.filter(scope.editing.observed_treatment, function(ot){
         return !scope.isCurrent(ot) && !_.isBoolean(ot.observed);
       }).length;
    };

   /*
   * removes previously observed treatments and adds in observed treatments
   * if we're missing any
   */
   scope.getReleventTreatments = function(observedTreatments, treatments){
     observedTreatments = _.filter(observedTreatments, function(x){
       return x.drug && x.drug.length;
     });

     /*
     * we need to build up all missing observed treatments
     * if they haven't been for a few days we need
     * to build that history
     */
    _.each(treatments, function(treatment){
      var startDate = treatment.start_date || treatment.created;

      // we add one to include today
      var daysSince = now.diff(startDate, "d") + 1;
      var stopDate = treatmentUtils.getStopDate(treatment);
      var clonedObservedTreatments = _.clone(observedTreatments);

      _.times(daysSince, function(since){
        var forDate;
        forDate = moment(startDate).add(since, "d");
        if(!forDate){
          forDate = treatment.created;
        }

        if(!stopDate || forDate.isBefore(stopDate, "d")){
          var ot = _.find(clonedObservedTreatments, function(ot){
            var sameDay = moment(ot.date).isSame(forDate, "d");
            var sameDrug = ot.drug === treatment.drug;
            var sameDose = ot.dose === treatment.dose;
            return sameDay && sameDrug && sameDose;
          });

          if(!ot){
            observedTreatments.push(
              scope.makeObservedTreatmentFromTreatment(treatment, forDate)
            );
          }
        }
      });
    });

    /*
    * remove previous treatments that have been observed, we don't care about these
    */
    observedTreatments = _.filter(observedTreatments, function(ot){
        return !_.isBoolean(ot.observed) || scope.isCurrent(ot);
    });

    // sort by date then drug
    observedTreatments = _.sortBy(observedTreatments, function(ot){
      return ot.drug;
    });

    return _.sortBy(observedTreatments, function(ot){
      return moment(ot.date).startOf('day');
    });
  };

   scope.initialise();
 }
);
