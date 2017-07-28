angular.module('opal.services').service(
    'TreatmentRecord', function(){
    "use strict";

    return function(item){
        var now = moment();
        item.formController = "TreatmentFormCtrl";

        // the actual date we stopped if it exists
        item.stoppedDate = item.end_date || item.planned_end_date;
        item.ongoing = item.stoppedD  ate && now.isBefore(item.stoppedDate, "d");

        // we have completed a treatment if we went all the way to the
        // planned end date
        if(item.ongoing){
          item.completed = false;
        }
        else if (!item.planned_end_date){
          item.completed = false;
        }
        else{
          if(item.end_date && item.end_date.isBefore(item.planned_end_date, "d")){
            item.completed = false;
          }
          else{
            item.completed = true;
          }
        }

        // we have a planned end date but we finished early
        item.stoppedEarly = !item.completed && item.planned_end_date && item.end_date && item.planned_end_date.isAfter(item.end_date, "d");
    };
});
