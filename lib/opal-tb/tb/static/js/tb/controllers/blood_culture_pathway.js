angular.module('opal.controllers').controller('BloodCulturePathwayCtrl',
function( $modal, $q, ngProgressLite, $controller, scope, step, episode) {
      "use strict";

      scope.addAerobic = function(){
        scope.aerobicModels.push({
          aerobic: true
        });
      };

      scope.addAnaerobic = function(){
        scope.anaerobicModels.push({
          aerobic: false
        });
      };

      scope.deleteAnaerobic = function(index){
        scope.anaerobicModels.splice(index, 1);
      }

      scope.deleteAerobic = function(index){
        scope.aerobicModels.splice(index, 1);
      }

      scope.preSave = function(editing){
        // filter out completely empty fields
        var toUpdate = scope.aerobicModels.concat(scope.anaerobicModels);

        var nonEmpties = _.reject(toUpdate, function(x){
            return _.isEmpty(_.omit(x, "aerobic"));
        });

        editing.blood_culture.isolates = nonEmpties;
      };

      scope.initialise = function(item){
        if(item){
          var isolates = item.isolates || [];
          scope.aerobicModels = angular.copy(_.filter(isolates, function(x){
            return x.aerobic
          }));
          scope.anaerobicModels = angular.copy(_.filter(isolates, function(x){
            return !x.aerobic
          }));
        }
        else{
          scope.anaerobicModels = [];
          scope.aerobicModels = [];
        }
      };
      var item = scope.editing.blood_culture;
      scope.initialise(item);
});
