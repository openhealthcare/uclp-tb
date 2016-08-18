angular.module('opal.controllers').controller('DOTHistoryCtrl',
 function(scope, step, episode) {
   if(!_.isArray(scope.editing.observed_treatment)){
      if(scope.editing.observed_treatment){
        scope.editing.observed_treatment = [scope.editing.observed_treatment];
      }
      else{
        scope.editing.observed_treatment = [];
      }
   }

   scope.chunkArray = function(ots){
     /*
     * creates an array of array of arrays
     * 1. aggregate the observed treatments by date
     * 2. split that array into chunks of the same treatment
     *
     * e.g. if day 1 they're on aspirin 200g
     *      day 2 they are still on that
     *      day 3 they're on apsirin 100g
     *
     * we get back [[day 3 OT], [day 2 OT, day 1 OT]]
     */

     scope.treatmentChunks = [];

     var Row = function(otArray){
        this.treatments = otArray;
        this.treatments = _.sortBy(this.treatments, function(ot){
            return ot.dose;
        });
        this.treatments = _.sortBy(this.treatments, function(ot){
            return ot.drug;
        });

        this.drugs = _.pluck(this.treatments, "drug");
        this.doses = _.pluck(this.treatments, "dose");
        this.date = otArray[0].date;

     }

     scope.getDrugsAndDosesFromRow = function(otArray){
      return _.reduce(otArray, function(m, v){
         m[v.drug] = m[v.dose];
         return m;
       }, {});
     }

     var byDate = {};

     _.each(ots, function(ot){
        if(ot.date){
          var key = moment(ot.date).format("DD/MM/YYYY");
          if(!byDate[key]){
            byDate[key] = [];
          }

          byDate[key].push(ot);
        }
     });

     var sortedByDate = _.sortBy(_.values(byDate), function(otArray){
        return -moment(otArray[0].date).unix();
     });

     var existingDrugRegimen = {};
     var currentRigmen = [];
     _.each(sortedByDate, function(otArray, i){
       var drugsAndDoses = scope.getDrugsAndDosesFromRow(otArray);

       if(!_.isEqual(drugsAndDoses, existingDrugRegimen) && currentRigmen.length){
         scope.treatmentChunks.push(currentRigmen);
         currentRigmen = [new Row(otArray)];
         existingDrugRegimen = drugsAndDoses;
       }
       else{
         currentRigmen.push(new Row(otArray));
       }
    });
    // push the last one on the pile
    scope.treatmentChunks.push(currentRigmen);
   };

   scope.chunkArray(scope.editing.observed_treatment);
 }
);
