angular.module('opal.controllers').controller('TBTypeFormCtrl',
  function(step, scope, episode) {
    "use strict";

    var vm = this;
    vm.step = step;
    var toEdit = scope.editing[step.api_name];
    scope.toTbType = function(stage){
        scope.editing[step.api_name] = stage;
        scope.goNext();
    };
    scope.hideFooter = true;
    scope.tbStages = ["Active TB", "Latent TB", "NTM"];
});
