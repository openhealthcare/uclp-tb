angular.module('opal.controllers').controller('AddResultsCtrl',
function(scope, $templateRequest, step, episode, LabTestCollectionFormHelper) {
    "use strict";

    scope.editing.lab_test_collection._form_helper = new LabTestCollectionFormHelper(
      scope.editing.lab_test_collection
    )
});
