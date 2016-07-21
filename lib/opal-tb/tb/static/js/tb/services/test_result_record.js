angular.module('opal.services').service('TestResultRecord', function(){
    return function(item){
      if(!item.status){
          item.status = "Pending";
      }

      if(!item.date_ordered){
          item.date_ordered = moment();
      }
    };
});
