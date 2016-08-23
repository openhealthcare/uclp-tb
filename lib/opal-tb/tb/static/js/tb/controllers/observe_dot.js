angular.module('opal.controllers').controller('ObserveDOTCtrl',
 function(scope, $templateRequest, treatmentUtils, step, episode) {
   var now = moment();

   scope.initialise = function(){
     activeTreatments = treatmentUtils.getActiveTreatments(scope.episode.treatment);

     scope.editing.observed_treatment = _.filter(scope.episode.observed_treatment, function(x){
       return x.drug && x.drug.length;
     });

     scope.withHistorical = false;

     scope.hasHistory = _.find(scope.episode.observed_treatment, function(ot){
       return !now.isSame(ot.date, 'd');
     });

     var todaysObservations = _.filter(scope.episode.observed_treatment, function(ot){
       return now.isSame(ot.date, 'd');
     });

     _.each(activeTreatments, function(treatment){
       var exists = _.find(todaysObservations, function(ot){
         return ot.drug === treatment.drug && ot.dose === treatment.dose;
       });


       if(!exists){
         scope.editing.observed_treatment.push({
           drug: treatment.drug,
           dose: treatment.dose
         });
       }
     });
   };

   scope.showHistorical = function(){
     scope.withHistorical = !scope.withHistorical;
   };

   scope.setDate = function(item){
      if(!item.date){
        item.date = moment();
      }
   };

   scope.observeAllActiveTreatments = function(){
      _.each(scope.editing.observed_treatment, function(ot){
        if(scope.isCurrent(ot)){
          ot.observed = true;
          ot.date = moment();
        }
      });
   };

   scope.isCurrent = function(item){
     return !item.date || moment().isSame(moment(item.date), "d");
   };

   scope.preSave = function(editing){
    editing.observed_treatment = _.filter(editing.observed_treatment, function(ot){
    return ot.date;
    });
   };

   scope.initialise();
 }
);
