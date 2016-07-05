angular.module('opal.controllers').controller('TBSymptomsFormCtrl',
  function(Options, $controller, step, scope, episode, recordLoader) {
    var parentCtrl = $controller("MultistageDefault");
    var vm = this;
    _.extend(vm, parentCtrl);
    vm.step = step;

    recordLoader.then(function(columnSchema){
        if(episode.social_history && episode.social_history.length){
            scope.editing.social_history = episode.social_history[0].makeCopy();
        }
    });


    if(episode.symptom_complex.length){
      scope.editing.symptom_complex = {
        symptoms: episode.symptom_complex[0].symptoms,
        duration: episode.symptom_complex[0].duration,
        details: episode.symptom_complex[0].details
      }
    }
    else{
      scope.editing.symptom_complex = {};
      scope.editing.symptom_complex.symptoms  = [];
    }

    scope.tbSymptomFields = {
      "chills": "Chills",
      "cough": "Cough",
      "fatigue": "Fatigue",
      "fever": "Fever",
      "loss_of_appetite": "Loss of Appetite",
      "night_sweats": "Night Sweats",
      "haemoptysis": "Haemoptysis",
      "weight_loss": "Weight Loss"
    };
    scope.tbSymptom = {};

    var tbValues = _.keys(scope.tbSymptomFields);

    column1 = tbValues.slice(0, tbValues.length/2);
    column2 = tbValues.slice(tbValues.length/2);
    scope.columns = [column1, column2];

    scope.updateTbSymptoms = function(){
      var symptoms = scope.editing.symptom_complex.symptoms;

      var relevent = _.intersection(_.values(scope.tbSymptomFields), symptoms);

      _.each(scope.tbSymptomFields, function(v, k){
        var toAdd = _.contains(relevent, v);

        if(scope.tbSymptom[k]){
          scope.tbSymptom[k] = toAdd;
        }
        else if(!scope.tbSymptom[k] && toAdd){
          scope.tbSymptom[k] = toAdd;
        }
      });
    };

    scope.updateTbSymptoms();

    scope.updateSymptoms = function(symptomField){
      var symptoms = scope.editing.symptom_complex.symptoms;

      var symptomValue = scope.tbSymptomFields[symptomField]
      var inSymptoms = _.find(symptoms, function(x){
         return x === symptomValue;
      });
      var toAdd = scope.tbSymptom[symptomField];

      if(!inSymptoms && toAdd){
        symptoms.push(symptomValue);
      }
      else if(inSymptoms && !toAdd){
        symptoms = _.filter(symptoms, function(x){
            return x !== symptomValue;
        });

        scope.editing.symptom_complex.symptoms = symptoms;
      }
    };
});
