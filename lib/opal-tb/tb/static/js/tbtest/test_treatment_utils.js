describe('treatmentUtils', function(){
  var controller, scope, $rootScope, $controller;

  beforeEach(function(){
    module('opal.services');
    inject(function($injector){
        treatmentUtils  = $injector.get('treatmentUtils');
        $rootScope   = $injector.get('$rootScope');
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
    };
  });

  describe('get active treatments', function(){
    var today = moment();
    var sameDay = moment(today.format("YYYY-MM-DD"))
    var yesterday = moment().subtract(1, "d");
    var tomorrow = moment().add(1, "d");
    var treatments = [];

    it('it should show the treatment if the start date is in the past', function(){
        treatments = [{
          drug: "Aspirin",
          start_date: yesterday,
          planned_end_date: tomorrow,
          end_date: undefined
        }];

        var found = treatmentUtils.getActiveTreatments(treatments);
        expect(found).toEqual(treatments);
    });

    it('should show the treatment if the start date is today', function(){
      treatments = [{
        drug: "Aspirin",
        start_date: sameDay,
        planned_end_date: tomorrow,
        end_date: undefined
      }];

      var found = treatmentUtils.getActiveTreatments(treatments);
      expect(found).toEqual(treatments);
    });

    it('should not show the treatment if the end date is today', function(){
      treatments = [{
        drug: "Aspirin",
        start_date: yesterday,
        planned_end_date: sameDay,
        end_date: undefined
      }];

      var found = treatmentUtils.getActiveTreatments(treatments);
      expect(found).toEqual([]);
    });

    it('should use the end date if it is before the planned_end_date', function(){
      treatments = [{
        drug: "Aspirin",
        start_date: yesterday,
        planned_end_date: tomorrow,
        end_date: sameDay
      }];

      var found = treatmentUtils.getActiveTreatments(treatments);
      expect(found).toEqual([]);
    })
  });
});
