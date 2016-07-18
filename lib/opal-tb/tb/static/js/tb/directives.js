directives.directive("timeline", function () {
  return {
    scope: false,
    templateUrl: "/templates/timeline.html",
    link: function(scope, element, attr){
        "use strict";

        var getTemplateUrl = function(columnName){
            return "/templates/record/" + columnName + '.html';
        };

        var getIcon = function(columnName){
            return scope.fields[columnName].icon;
        }

        var metaInformation = [
            {
              columnName: "patient_consultation",
              when: 'when',
            },
            {
              columnName: 'symptom_complex',
              when: 'created'
            },
            {
              columnName: 'investigation',
              when: 'date_ordered'
            },
            {
              columnName: 'treatment',
              when: 'start_date',
            },
            {
              columnName: 'treatment',
              when: 'end_date',
            },
        ];

        metaInformation = _.map(metaInformation, function(m){
            if(!m.icon){
              m.icon = getIcon(m.columnName);
            }
            if(!m.templateUrl){
              m.templateUrl = getTemplateUrl(m.columnName);
            }

            return m;
        });

        var getMetaDataForSubrecord = function(item){
            return _.filter(metaInformation, function(x){
                return x.columnName === item.columnName;
            });
        };

        var getReleventSubrecords = function(){
            var columnNames = _.unique(_.pluck(metaInformation, "columnName"));
            return _.reduce(_.keys(scope.episode), function(memo, k){
                if(_.contains(columnNames, k)){
                  memo = memo.concat(scope.episode[k]);
                }

                return memo;
            }, []);
        };

        var constructTimelineMetaData = function(subrecords){
            var timelineMetaData = [];
            _.each(subrecords, function(subrecord){
                var metaData = getMetaDataForSubrecord(subrecord);
                 _.each(metaData, function(x){
                   if(subrecord[x.when]){
                      var metaDataCopy = angular.copy(x);
                      metaDataCopy.subrecord = subrecord;
                      timelineMetaData.push(metaDataCopy);
                   }
                });
            });

            return timelineMetaData;
        };

        var sortMetaData = function(timelineData){
            return _.sortBy(timelineData, function(x){
              return x.subrecord[x.when].toDate();
            }).reverse();
        };

        scope.getIndex = function(item){
            var columnName = item.columnName;
            var result = _.findIndex(scope.episode[columnName], function(x){
                return x.id === item.id;
            });
            return result;
        };

        var constructTimeline = function(){
          // gets an array of all the relevent subrecords
          var timelineRecords = getReleventSubrecords();

          // constructs an array of meta data where each one has a subrecord attatched
          // note there can be more than one per subrecord
          var timelineData = constructTimelineMetaData(timelineRecords);

          // sorts the meta data according to the when fields and
          // sticks it in
          scope.timelineData = sortMetaData(timelineData);
        };

        constructTimeline();
    }
  };
});
