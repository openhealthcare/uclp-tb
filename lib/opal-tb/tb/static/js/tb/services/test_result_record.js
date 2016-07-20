angular.module('opal.services').service(
    'TestResultRecord', function(item){

      if(!item.status){
          item.status = "pending";
      }

      if(!item.date_ordered){
          item.date_ordered = moment();
      }
});
