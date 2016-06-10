angular.module('opal.controllers').controller('InvestigationFormCtrl',
  function(Options, $controller, step, scope, episode) {
      "use strict";

      var parentCtrl = $controller("MultiSaveCtrl", {
        step: step,
        episode: episode,
        scope: scope
      });
      var vm = this;

      _.extend(vm, parentCtrl);
      scope.tagging_display_list = [];
      scope.display_tag_to_name = {};
      scope.selectedTags = [];

      Options.then(function(options){
        // TODO - don't hardcode this
        var columnName = 'investigation';
		    scope.microbiology_test_list = [];
		    scope.microbiology_test_lookup = {};
		    scope.micro_test_defaults =  options.micro_test_defaults;

		    for (var name in options){
			    if (name.indexOf('micro_test') == 0) {
				    for (var ix = 0; ix < options[name].length; ix++) {
					    scope.microbiology_test_list.push(options[name][ix]);
					    scope.microbiology_test_lookup[options[name][ix]] = name;
				    }
			    }
		    }

        var watchName = "editing.investigation.test"

		    scope.$watch(watchName, function(testName) {

          _.each(_.keys(scope.editing.investigation), function(field){
              if(field !== "test" && field !== "id" && field !== "episode_id" && field !== "consistency_token"){
                scope.editing.investigation[field] = undefined;
              }
          });

			    scope.testType = scope.microbiology_test_lookup[testName];
          if( _.isUndefined(testName) || _.isUndefined(vm.testType) ){
              return;
          }

          if(scope.testType in scope.micro_test_defaults){
            _.each(_.pairs(scope.micro_test_defaults[scope.testType]), function(values){
                    var field =  values[0];
                    var val =  values[1];
                    scope.editing.investigation[field] = val;
            });
          }
		    });
      });
});
