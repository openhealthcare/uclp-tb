directives.directive("timeline", function () {
  return {
    scope: false,
    templateUrl: "/templates/timeline.html",
    link: function(scope, element, attr){
        "use strict";

        var included = {
            patient_consultation: {
                when: 'when',
                templateUrl: undefined,
                icon: undefined
            }
        }

        scope.included = _.mapObject(included, function(v, k){
            // we need to decide if we're pulling this from schema
            // item utils, for the time being hard code
            if(!v.templateUrl){
              v.templateUrl = "/templates/record/" + k + '.html'
            }
            v.icon = "fa fa-comments"
        });

        var timelineSubrecordTypes = ['patient_consultation'];

        var timelineSubrecords = [];

        _.each(timelineSubrecordTypes, function(timelineSubrecordType){
            timelineSubrecords = timelineSubrecords.concat(scope.episode[timelineSubrecordType]);
        });

        scope.timelineSubrecords = _.sortBy(timelineSubrecords, function(x){
        });
    }
  };
});
