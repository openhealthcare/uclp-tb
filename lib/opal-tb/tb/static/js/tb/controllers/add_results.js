angular.module('opal.controllers').controller('AddResultsCtrl',
function(scope, $templateRequest, step, episode) {
    "use strict";

    scope.loading = true;

    $templateRequest("/templates/forms/test_result.html").then(function(){
        scope.loading = false;
    });

    scope.editing.test_result = _.filter(scope.editing.test_result, function(tr){
      return tr.status === "Pending";
    });

    scope.preSave = function(editing){
      _.each(editing, function(v, k){
          if(k !== "test_result"){
            delete editing[k];
          }
      });
    };

});
