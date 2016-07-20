angular.module('opal.controllers').controller('TBTreatmentCtrl',
function($modal, $q, ngProgressLite, $controller, scope, step, episode) {
    "use strict";

    /*
    * so with weight we'll store another row in observations if the
    * weighthas changed, otherwise keep it the same
    */
    var currentWeight;

    scope.editing.stage = episode.stage;

    if(!_.isArray(scope.editing.observations)){
        if(_.isObject(scope.editing.observations) && scope.editing.observations.weight){
          scope.editing.observations = [scope.editing.observations];
        }
        else{
          scope.editing.observations = [];
        }
    }

    // we should sort this via datetime
    if(!_.isArray(scope.editing.treatment)){
        if(_.isObject(scope.editing.treatment)){
          scope.editing.treatment = [scope.editing.treatment];
        }
        else{
          scope.editing.treatment = [{}];
        }
    }

    var existingTreatment = angular.copy(scope.editing.treatment);

    scope.existingTreatmentFilter = function(x){
        if(!x.end_date){
          return true;
        }
        return moment().diff(moment(x.end_date), 'days') !== 1;
    }

    scope.localEditing = {treatmentPlan: angular.copy(scope.editing.treatment)};

    if(scope.editing.observations.length){
      var lastObservation = _.last(_.sortBy(scope.editing.observations, function(x){
          // this should be a moment, not a date
          return x.datetime;
      }));

      currentWeight = _.last(_.sortBy(scope.editing.observations)).weight;
    }
    scope.localEditing.weight = currentWeight;
    scope.localEditing.treatmentStartDate = new Date();

    var smearId;
    var smearConsistencyToken;
    var cultureId;
    var cultureConsistencyToken;
    var diagnosisId;
    var diagnosisConsistencyToken;

    var tests = [
      "Culture",
      "Smear",
      "GeneXpert"
    ];
    scope.tests = [];

    _.each(tests, function(testTitle){
        var test = _.find(scope.editing.investigation, function(e){
            return e.test === testTitle;
        });

        if(!test){
            test = {test: testTitle, result: "Not Done"};
        }
        scope.tests.push(test);
    });

    scope.localEditing.hasPulmonary = false;
    scope.localEditing.otherSites = false;

    if(episode.diagnosis.length){
        if(episode.diagnosis[0].condition.indexOf("Extra") !== -1){
            scope.localEditing.pulmonary = "Extra-Pulmonary TB";
        }
        else{
            scope.localEditing.pulmonary = "Pulmonary TB";
        }
        diagnosisId = episode.diagnosis[0].id;
        diagnosisConsistencyToken = episode.diagnosis[0].consistency_token
        scope.localEditing.site = episode.diagnosis[0].details;
    }

    scope.preSave = function(editing){
        editing.investigation = [];
        _.each(scope.tests, function(test){
          editing.investigation.push(test);
        });
        editing.diagnosis = [];
        editing.diagnosis = {
          condition: editing.stage,
          details: scope.localEditing.site,
          id: diagnosisId,
          consistency_token: diagnosisConsistencyToken
         };

         if(scope.localEditing.weight.length && scope.localEditing.weight != currentWeight){
           scope.editing.observations.push({weight: scope.localEditing.weight});
         }

         editing.treatment = scope.localEditing.treatmentPlan;
    };

    scope.addTreatment = function(){
        scope.localEditing.treatmentPlan.push({});
    };

    scope.removeTreatment = function($index){
        scope.localEditing.treatmentPlan.splice($index, 1);
    };

    scope.stopTreatment = function($index){
        scope.localEditing.treatmentPlan[$index].end_date = new Date();
    }

    scope.today = function(date){
      if(!date){
        return false;
      }
      return moment(new Date()).format("DD/MM/YYYY") === moment(date).format("DD/MM/YYYY");
    }

    scope.useTreatmentPlan = function(){
        var rifampicin_dose = '600mg';
        var pyrazinamide_dose = '2g';
        if(parseInt(scope.localEditing.weight) < 50){
            rifampicin_dose = '450mg';
            pyrazinamide_dose = '1.5g';
        }
        var ethambutol_dose = 15 * parseInt(scope.localEditing.weight);
        ethambutol_dose += 'mg';

        scope.localEditing.treatmentPlan = scope.localEditing.treatmentPlan.concat([
            {
                drug: 'Isoniazid',
                dose: '300mg',
                start_date: scope.localEditing.treatmentStartDate,
                planned_end_date: moment(scope.localEditing.treatmentStartDate).add(6, 'months').toDate()
            },
            {
                drug: 'Pyridoxine',
                dose: '10mg',
                start_date: scope.localEditing.treatmentStartDate,
                planned_end_date: moment(scope.localEditing.treatmentStartDate).add(6, 'months').toDate()
            },
            {
                drug: 'Rifampicin',
                dose: rifampicin_dose,
                start_date: scope.localEditing.treatmentStartDate,
                planned_end_date: moment(scope.localEditing.treatmentStartDate).add(6, 'months').toDate()
            },
            {
                drug: 'Pyrazinamide',
                dose: pyrazinamide_dose,
                start_date: scope.localEditing.treatmentStartDate,
                planned_end_date: moment(scope.localEditing.treatmentStartDate).add(2, 'months').toDate()
            },
            {
                drug: 'Ethambutol',
                dose: ethambutol_dose,
                start_date: scope.localEditing.treatmentStartDate,
                planned_end_date: moment(scope.localEditing.treatmentStartDate).add(2, 'months').toDate()
            },
        ]);
    }

    scope.editing.patient_consultation = episode.newItem("patient_consultation").makeCopy();
});
