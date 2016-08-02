describe('TBInitialAssessmentCtrl', function(){
  "use strict";
  var controller, scope, $rootScope, $controller;

  beforeEach(function(){
      module('opal.controllers');
      inject(function($injector){
          $rootScope   = $injector.get('$rootScope');
          $controller  = $injector.get('$controller');
      });

      scope = $rootScope.$new();
      scope.editing = {demographics: {}, social_history: {}};

      controller = $controller('TBInitialAssessmentCtrl', {
          Options: function(a){
              return {then: function(fn) { fn(); }};
          },
          $controller: $controller,
          step: {},
          scope: scope,
          episode: {
              newItem: function(){
                  return {
                      makeCopy: function(){}
                  }
              }
          }
      });
  })

  describe('test change', function(){
    beforeEach(function(){
      _.each(scope.tbSymptomFields, function(v, k){
        scope.tbSymptom[k] = false;
      });
    });

    it('should update the radio buttons according to the symptoms model changes', function(){
        var symptomField = 'chills'
        scope.tbSymptom[symptomField] = true;
        scope.updateSymptoms(symptomField);
        expect(_.contains(scope.editing.symptom_complex.symptoms, "Chills")).toBe(true);
    });

    it('should update the model based on radio button changes', function(){
        var symptomField = "Chills";
        scope.editing.symptom_complex.symptoms.push(symptomField);
        scope.updateTbSymptoms()
        expect(scope.tbSymptom["chills"]).toBe(true);
    });

  });

  describe('Geographics change', function(){
    it('should init to the uk if not set', function(){
      expect(scope.editing.demographics.birth_place).toEqual("United Kingdom");
      expect(scope.show_arrival_in_the_uk).toBe(false);
    });

    it('should show arrival to the uk if birth place !== UK', function(){
      scope.editing.demographics.birth_place = "France";
      scope.birth_place_change();
      expect(scope.show_arrival_in_the_uk).toBe(true);
    });

    it('should remove arrived in the uk and clean the field if set back to the uk', function(){
      scope.editing.demographics.birth_place = "France";
      scope.birth_place_change();
      scope.arrival_in_the_uk = "2012";
      scope.editing.demographics.birth_place = "United Kingdom";
      scope.birth_place_change();
      expect(scope.show_arrival_in_the_uk).toBe(false);
      expect(scope.editing.social_history.arrival_in_the_uk).toBe(undefined);
    });
  });
});
