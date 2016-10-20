directives.directive("timeline", function ($rootScope) {
  return {
    scope: false,
    templateUrl: "/templates/timeline/timeline.html",
    link: function(scope, element, attr){
        "use strict";

        var getTemplateUrl = function(columnName){
            return "/templates/record/" + columnName + '.html';
        };

        var getIcon = function(columnName){
            return scope.fields[columnName].icon;
        }

        var getDisplayName = function(columnName){
            return scope.fields[columnName].display_name;
        }

        scope.today = new Date();
        scope.isMomentToday = function(m){
            return m.startOf('day').isSame(moment(scope.today).startOf('day'));
        }

        scope.timelineAddVisible = false;

        scope.metaInformation = [
            {
              columnName: 'referral_route',
              when: 'date_of_referral',
              aggregateTemplateUrl: "/templates/timeline/referral_route.html",
              addable: false,
              priority: 4
            },
            {
              columnName: "patient_consultation",
              when: 'when',
              addable: true,
              priority: 5
            },
            {
              columnName: 'symptom_complex',
              when: 'created',
              addable: true,
              priority: 6
            },
            {
              columnName: 'treatment',
              when: 'start_date',
              name: 'treatment_start',
              aggregateTemplateUrl: "/templates/timeline/started_treatment.html",
              addable: true,
              priority: 9,
            },
            {
              columnName: 'treatment',
              when: 'end_date',
              name: 'treatment_stop',
              aggregateTemplateUrl: "/templates/timeline/stopped_treatment.html",
              addable: true,
              priority: 10,
            },
            {
              columnName: 'investigation',
              when: 'date_ordered',
              aggregateTemplateUrl: '/templates/timeline/investigation.html',
              addable: false,
              priority: 9
            },
            {
              columnName: 'tb_history',
              when: 'created',
              aggregateTemplateUrl: '/templates/timeline/tb_history.html',
              addable: false,
              priority: 8
            }
        ];

        scope.metaInformation = _.map(scope.metaInformation, function(m){
            if(!m.icon){
              m.icon = getIcon(m.columnName);
            }
            if(!m.templateUrl){
              m.templateUrl = getTemplateUrl(m.columnName);
            }
            if(!m.name){
              m.name = m.columnName;
            }
            if(!m.display_name){
              m.display_name = getDisplayName(m.columnName);
            }

            if(!m.index){
              m.index = 5;
            }

            if(!m.aggregateTemplateUrl){
              m.aggregateTemplateUrl = "/templates/timeline/aggregate_template.html";
            }

            return m;
        });

        scope.metaInformation = _.sortBy(scope.metaInformation, function(x){
          return x.priority;
        }).reverse();

        var columnNames = _.unique(_.pluck(scope.metaInformation, "columnName"));

        var getWhen = function(metaData){
            return metaData.subrecord[metaData.when].format("DD/MM/YYYY");
        };

        var getMetaDataForSubrecord = function(item){
            return _.filter(scope.metaInformation, function(x){
                return x.columnName === item.columnName;
            });
        };

        var getReleventSubrecords = function(){
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
                var index = String(metaData.index);

                if(!newMetaDataInformation[when]){
                  newMetaDataInformation[when] = {};
                }

                if(!newMetaDataInformation[when][index]){
                  newMetaDataInformation[when][index] = {};
                }

                if(!newMetaDataInformation[when][index][metaData.columnName]){
                  newMetaDataInformation[when][index][metaData.columnName] = {};
                }

                if(!newMetaDataInformation[when][index][metaData.columnName][metaData.when]){
                  newMetaDataInformation[when][index][metaData.columnName][metaData.when] = [];
                }

                newMetaDataInformation[when][index][metaData.columnName][metaData.when].push(metaData);
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

        scope.getSubrecordFromDateAndMetaInfo = function(someMoment, fieldMetaData){
            /*
            * takes in meta data and pulls out the subrecords
            */
            var dateString = someMoment.format("DD/MM/YYYY");
            var index = String(fieldMetaData.index);

            var keys = [dateString, index, fieldMetaData.columnName, fieldMetaData.when];

            var searchingFor = scope.reducedMetaData;
            var found = true;
            keys.every(function(key){
                if(searchingFor[key]){
                    searchingFor = searchingFor[key];
                    return true;
                }
                else{
                    found = false;
                    return false;
                }
            });

            if(!found){
              return [];
            }
            var result =  _.map(searchingFor, function(searched){
              return searched.subrecord;
            });

            return result;
        };

        var constructTimeline = function(){
          // gets an array of all the relevent subrecords
          var timelineRecords = getReleventSubrecords();

          // constructs an array of meta data where each one has a subrecord attatched
          // note there can be more than one per subrecord
          var timelineData = constructTimelineMetaData(timelineRecords);

          // we sort the data via date string
          scope.reducedMetaData = reduceMetaData(timelineData)

          // remove the dates for display
          scope.dates = getDates(scope.reducedMetaData);
        };

        var getIndexForSubrecord = function(subrecord){
           return _.findIndex(scope.episode[subrecord.columnName], function(episodeSubrecord){
                return episodeSubrecord.id === subrecord.id;
           });
        };

        scope.editItem = function(item){
            scope.episode.recordEditor.editItem(item.columnName, getIndexForSubrecord(item))
        };

        var metaInformationDisplay = _.reduce(
            _.filter(scope.metaInformation, function(mi){ return mi.addable}),
            function(memo, mi){
                memo[mi.columnName] = {columnName: mi.columnName, icon: mi.icon, display_name: mi.display_name}
                return memo;
            }, {});

        scope.metaInformationDisplay = _.map(metaInformationDisplay, function(v, k){
            return v;
        });

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
