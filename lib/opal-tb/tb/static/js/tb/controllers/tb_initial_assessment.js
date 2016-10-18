angular.module('opal.controllers').controller('TBInitialAssessmentCtrl',
  function(step, scope, episode, $window, Item, recordLoader) {
    var Uk = 'United Kingdom';
    var vm = this;
    vm.step = step;

    if(!scope.editing.symptom_complex){
      scope.editing.symptom_complex = {};
      scope.editing.symptom_complex.symptoms  = [];
    }

    if(!scope.editing.symptom_complex.symptoms){
      scope.editing.symptom_complex.symptoms = [];
    }

    scope.birth_place_change = function(){
      if(scope.editing.demographics.birth_place && scope.editing.demographics.birth_place.length){
        if(scope.editing.demographics.birth_place === Uk){
          scope.show_arrival_in_the_uk = false;
          scope.editing.social_history.arrival_in_the_uk = undefined;
        }
        else{
          scope.show_arrival_in_the_uk = true;
        }
      }
    };

    var tests = [
      "Culture",
      "Smear",
      "Smear",
      "Smear",
      "GeneXpert"
    ];

    if(!scope.editing.investigation){
      scope.editing.investigation = [];
    }
    else if (!_.isArray(scope.editing.investigation)){
      scope.editing.investigation = [scope.editing.investigation];
    }

    scope.editing.investigation = _.filter(scope.editing.investigation, function(i){
      return i.test;
    });

    scope.addCommonTests = function(){
      _.each(tests, function(testTitle){
          test = {
            test: testTitle,
            date_ordered: moment()
          }
          test[testTitle.toLowerCase()] = "pending";
          scope.editing.investigation.push(test);
      });
    };

    scope.show_arrival_in_the_uk = false;
    scope.birth_place_change();

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
      var symptoms = scope.editing.symptom_complex.symptoms || [];

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

    scope.preSave = function(editing){
      if(!editing.patient_consultation.discussion || !editing.patient_consultation.discussion.length){
         delete editing.patient_consultation;
      }

      if(!scope.editing.symptom_complex.symptoms.length){
         delete editing.symptom_complex;
      }
    }

    scope.editing.patient_consultation = episode.newItem("patient_consultation").makeCopy();
});
