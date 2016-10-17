describe('TBAddPatientCtrl', function(){
  var controller, scope, $rootScope, $controller;

  beforeEach(function(){
    module('opal.controllers');
    inject(function($injector){
        $rootScope   = $injector.get('$rootScope');
        $controller  = $injector.get('$controller');
    });
    scope = $rootScope.$new();
    controller = $controller('TBAddPatientCtrl', {
      scope: scope,
      step: {},
      episode: {}
    });
  });

  describe('populatedDemographics', function(){
    it("if demographics doesn't exist it should re turn false", function(){
      scope.editing = {};
      expect(scope.populatedDemographics()).toBe(false);
    });

    it("if one of the fields is missing it should return false", function(){
      scope.editing = {demographics: {first_name: "James", surname: "Bond"}};
      expect(scope.populatedDemographics()).toBe(false);
    });

    it("if all of the fields are missing it should return false", function(){
      scope.editing = {demographics: {
        first_name: "James",
        surname: "Bond",
        date_of_birth: new Date()
      }};
      expect(scope.populatedDemographics()).toBe(true);
    });
  });

  describe("valid", function(){
    var form;
    beforeEach(function(){
      form = {
        demographics_hospital_number: {$setValidity: function(){}}
      };
    });

    it("should set valid if demographics are populated", function(){
      spyOn(form.demographics_hospital_number, "$setValidity");
      spyOn(scope, "populatedDemographics").and.returnValue(true);
      scope.editing = {demographics: {hospital_number: "12"}};
      scope.valid(form);
      expect(form.demographics_hospital_number.$setValidity).toHaveBeenCalledWith(
        'no_personal_info', true
      );
    });

    it("should set invalid if name is not populated", function(){
      spyOn(form.demographics_hospital_number, "$setValidity").and.returnValue(false);
      scope.editing = {demographics: {hospital_number: "12"}};
      spyOn(scope, "populatedDemographics").and.returnValue(false);
      scope.valid(form);
      expect(form.demographics_hospital_number.$setValidity).toHaveBeenCalledWith(
        'no_personal_info', false
      );
    });

    it("should set invalid if hospital number is not populated", function(){
      spyOn(form.demographics_hospital_number, "$setValidity").and.returnValue(true);
      scope.editing = {demographics: {hospital_number: undefined}};
      spyOn(scope, "populatedDemographics").and.returnValue(true);
      scope.valid(form);
      expect(form.demographics_hospital_number.$setValidity).toHaveBeenCalledWith(
        'no_personal_info', false
      );
    });
  });
});
