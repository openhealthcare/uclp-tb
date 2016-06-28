angular.module('opal.controllers').controller('TBSymptomsFormCtrl',
  function(Options, $controller, step, scope, episode) {
    var parentCtrl = $controller("MultistageDefault");
    var vm = this;
    _.extend(vm, parentCtrl);
    vm.step = step;
    scope.editing.symptom_complex.symptoms  = [];
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

    var tbValues = _.keys(scope.tbSymptomFields);

    column1 = tbValues.slice(0, tbValues.length/2);
    column2 = tbValues.slice(tbValues.length/2);
    scope.columns = [column1, column2];

    scope.updateTbSymptoms = function(){
      var symptoms = scope.editing.symptom_complex.symptoms;

      var relevent = _.intersection(_.values(scope.tbSymptomFields), symptoms);

      _.each(scope.tbSymptomFields, function(v, k){
        var toAdd = _.contains(relevent, v);

        if(scope.editing.tb_symptoms[k]){
          scope.editing.tb_symptoms[k] = toAdd;
        }
        else if(!scope.editing.tb_symptoms[k] && toAdd){
          scope.editing.tb_symptoms[k] = toAdd;
        }
      });
    };

    scope.updateSymptoms = function(symptomField){
      var symptoms = scope.editing.symptom_complex.symptoms;

      var symptomValue = scope.tbSymptomFields[symptomField]
      var inSymptoms = _.find(symptoms, function(x){
         return x === symptomValue;
      });
      var toAdd = scope.editing.tb_symptoms[symptomField];

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

    vm.valid = function(editing){
        var result = _.all(tbValues, function(required){
            result = editing.tb_symptoms[required] !== undefined
            return editing.tb_symptoms[required] !== undefined;
        });

        return result;
    };
});
