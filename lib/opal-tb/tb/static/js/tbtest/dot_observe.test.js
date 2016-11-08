describe('ObserveDOTCtrl', function(){
  "use strict";

  var controller, scope, $rootScope, $controller
  var today = moment();
  var yesterday = moment().subtract(1, "d");
  var two_days_ago = moment().subtract(2, "d");
  var tomorrow = moment().add(1, "d");
  var treatments = [];


  beforeEach(function(){
    module('opal.controllers');
    inject(function($injector){
        $rootScope   = $injector.get('$rootScope');
        $controller  = $injector.get('$controller');
    });

    $rootScope.fields = {
      observed_treatment: {
        date: {type: 'date'}
      },
      treatment: {
        start_date: {type: 'date'},
        planned_end_date: {type: 'date'},
        end_date: {type: 'date'}
      }
    }

    scope = $rootScope.$new();
    scope.editing = {observed_treatment: []};
    scope.episode = {treatment: []}

    controller = $controller('ObserveDOTCtrl', {
      scope: scope,
      step: {},
      episode: {}
    });
  })

  describe("it should give me a count of those that are in the past and not observed", function(){
    it('should only count those in the past', function(){
      scope.editing.observed_treatment.push({
          observed: undefined,
          date: today,
          drug: "asprin",
          dose: "10mgs"
      });
      scope.editing.observed_treatment.push({
          observed: undefined,
          date: yesterday,
          drug: "asprin",
          dose: "10mgs"
      });

      expect(scope.getUnobservedCount()).toBe(1);
    });

    it('should only count those that have not been observed', function(){
        scope.editing.observed_treatment.push({
            observed: undefined,
            date: yesterday,
            drug: "asprin",
            dose: "10mgs"
        });
        scope.editing.observed_treatment.push({
            observed: false,
            date: two_days_ago,
            drug: "asprin",
            dose: "10mgs"
        });

      expect(scope.getUnobservedCount()).toBe(1);
    });
  });

  describe("it should load the relevent treatments onto the scope", function(){
    it('should show treatments that have no end date but a created timestamp', function(){
      var treatments = [{
          drug: "asprin",
          dose: "10mgs",
          created: today,
      }];
      var ots = scope.getReleventTreatments([], treatments);
      expect(ots.length).toBe(1);
      expect(ots[0].date.isSame(today, "d")).toBe(true);
      expect(ots[0].observed).toBe(undefined);
    });

    it('should remove previously observed treatments', function(){
      var treatments = [{
          drug: "asprin",
          dose: "10mgs",
          start_date: yesterday,
          planned_end_date: tomorrow
      }];
      var observedTreatments = [
        {
          observed: true,
          date: yesterday,
          drug: "asprin",
          dose: "10mgs"
        },
        {
          observed: false,
          date: today,
          drug: "asprin",
          dose: "10mgs"
        },
      ];

      var ots = scope.getReleventTreatments(observedTreatments, treatments);
      expect(ots.length).toBe(1);
      expect(ots[0].date.isSame(today, "d")).toBe(true);
      expect(ots[0].observed).toBe(false);
    });

    it("should populate observed treatments for dates we're missing", function(){
      var treatments = [{
          drug: "asprin",
          dose: "10mgs",
          start_date: yesterday,
          planned_end_date: tomorrow
      }];
      var observedTreatments = [
        {
          observed: false,
          date: today,
          drug: "asprin",
          dose: "10mgs"
        },
      ];

      var ots = scope.getReleventTreatments(observedTreatments, treatments);
      expect(ots.length).toBe(2);
      expect(ots[0].date.isSame(yesterday, "d")).toBe(true);
      expect(ots[0].observed).toBe(undefined);

      expect(ots[1].date.isSame(today, "d")).toBe(true);
      expect(ots[1].observed).toBe(false);
    });

    it('should order treatments by date', function(){
      var treatments = [{
          drug: "asprin",
          dose: "10mgs",
          start_date: two_days_ago,
          planned_end_date: tomorrow
      }];
      var observedTreatments = [
        {
          observed: null,
          date: two_days_ago,
          drug: "asprin",
          dose: "10mgs"
        },
        {
          observed: false,
          date: today,
          drug: "asprin",
          dose: "10mgs"
        },
      ];

      var ots = scope.getReleventTreatments(observedTreatments, treatments);
      expect(ots.length).toBe(3);
      expect(ots[0].date.isSame(two_days_ago, "d")).toBe(true);
      expect(ots[1].date.isSame(yesterday, "d")).toBe(true);
      expect(ots[2].date.isSame(today, "d")).toBe(true);
    });
  });
});
