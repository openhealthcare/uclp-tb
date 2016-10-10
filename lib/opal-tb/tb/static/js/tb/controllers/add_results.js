angular.module('opal.controllers').controller('AddResultsCtrl',
function(scope, $templateRequest, step, episode, LabTestCollectionFormHelper) {
    "use strict";

    scope.editing.lab_test_collection._formHelper = new LabTestCollectionFormHelper(
      scope.editing.lab_test_collection
    );

    scope.preSave = function(editing){
        scope.editing.lab_test_collection._formHelper.preSave(editing);
        delete editing.lab_test_collection._formHelper;
    };
});
