directives.directive("timeline", function ($rootScope) {
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
              name: 'treatment_start',
            },
            {
              columnName: 'treatment',
              when: 'end_date',
              name: 'treatment_stop',
            },
        ];

        metaInformation = _.map(metaInformation, function(m){
            if(!m.icon){
              m.icon = getIcon(m.columnName);
            }
            if(!m.templateUrl){
              m.templateUrl = getTemplateUrl(m.columnName);
            }
            if(!m.name){
              m.name = m.columnName;
            }

            return m;
        });

        var getWhen = function(metaData){
            return metaData.subrecord[metaData.when].format("DD/MM/YYYY");
        };

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

        var reduceMetaData = function(timelineData){
            var newMetaDataInformation = {};
            _.each(timelineData, function(metaData){
                var when = getWhen(metaData);
                if(newMetaDataInformation[when]){
                    newMetaDataInformation[when].push(metaData);
                }
                else{
                    newMetaDataInformation[when] = [metaData];
                }
            });

            return newMetaDataInformation;
        };

        var getDates = function(timelineData){
            var allDates = _.reduce(timelineData, function(memo, v, k){
                memo.push(moment(k, "DD/MM/YYYY"));
                return memo;
            }, []);

            return _.sortBy(allDates, function(x){
                return x.toDate();
            }).reverse();
        };

        scope.getMetaDataFromMomentAndName = function(someMoment, name){
            var dateString = someMoment.format( "DD/MM/YYYY");
            var someMetaData = scope.metaDataByDate[dateString];
            return _.filter(someMetaData, function(metaData){
                return metaData.name === name;
            });
        };

        var constructTimeline = function(){
          // gets an array of all the relevent subrecords
          var timelineRecords = getReleventSubrecords();

          // constructs an array of meta data where each one has a subrecord attatched
          // note there can be more than one per subrecord
          var timelineData = constructTimelineMetaData(timelineRecords);

          scope.metaDataByDate = reduceMetaData(timelineData)

          // sorts the meta data according to the when fields and
          // sticks it in
          scope.dates = getDates(scope.metaDataByDate);
        };

        var getIndexForSubrecord = function(subrecord){
           return _.findIndex(scope.episode[subrecord.columnName], function(episodeSubrecord){
                return episodeSubrecord.id === subrecord.id;
           });
        };

        scope.editItem = function(item){
            scope.episode.recordEditor.editItem(item.columnName, getIndexForSubrecord(item))
        };

        var columnNames = _.unique(_.pluck(metaInformation, "columnName"));
        _.each(columnNames, function(columnName){
            // watching episode subrecords
            // creates a circular referene
            // as they have a pointer to episode
            $rootScope.$watch("state", function(){
              constructTimeline();
            }, true);
        });


        constructTimeline();
    }
  };
});
