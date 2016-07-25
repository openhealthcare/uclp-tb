angular.module('opal.controllers').controller('AddTestsCtrl',
function(scope, step, episode) {
    "use strict";

    scope.editing.test_result = [];

    scope.addTest = function(testName){
      var test_result = episode.newItem("test_result");
      test_result.name = testName;
      scope.editing.test_result.push(test_result.makeCopy());
    };

    scope.removeTest = function($index){
        scope.editing.test_result.splice($index, 1);
    };

    scope.preSave = function(editing){
      _.each(editing, function(v, k){
          if(k !== "test_result"){
            delete editing[k];
          }
      });
    };
});
