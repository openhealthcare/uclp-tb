describe('TBSymptomsFormCtrl', function(){
  "use strict";
  var controller, scope, $rootScope, $controller;

  beforeEach(function(){
      module('opal.controllers');
      inject(function($injector){
          $rootScope   = $injector.get('$rootScope');
          $controller  = $injector.get('$controller');
      });

      scope = $rootScope.$new();

      controller = $controller('TBSymptomsFormCtrl', {
          Options: function(a){
              return {then: function(fn) { fn(); }};
          },
          $controller: $controller,
          step: {},
          scope: scope,
          episode: {}
      });
  })

  describe('test valid', function(){
    beforeEach(function(){
      _.each(scope.tbSymptomFields, function(v, k){
        scope.tbSymptom[k] = false;
      });
    });

    it("should return invalid if the radio buttons aren't clicked", function(){
        var firstField = _.keys(scope.tbSymptomFields)[0];
        console.error(controller);
        scope.tbSymptom[firstField] = undefined;
        expect(controller.valid()).toBe(false);
    });

    it("should return invalid if the radio buttons aren't clicked", function(){
        expect(controller.valid()).toBe(true);
    });
  });


})
