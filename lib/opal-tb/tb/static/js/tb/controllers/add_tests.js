angular.module('opal.controllers').controller('AddTestsCtrl',
function(scope, step, episode, LabTestCollectionFormHelper) {
    "use strict";

    if(!scope.editing.lab_test_collection.lab_tests){
      scope.editing.lab_test_collection.lab_tests = [];
    }

    scope.editing.lab_test_collection._formHelper = new LabTestCollectionFormHelper(
      scope.editing.lab_test_collection
    );

    scope.addTest = function(testName){
      scope.editing.lab_test_collection.lab_tests.push({
          test_name: testName,
          date_ordered: moment(),
          status: "pending"
      });
    };

    scope.removeTest = function($index){
        scope.editing.lab_test_collection.lab_tests.splice($index, 1);
    };

    scope.preSave = function(editing){
        scope.editing.lab_test_collection._formHelper.preSave(editing);
        delete editing.lab_test_collection._formHelper;
    };
});
