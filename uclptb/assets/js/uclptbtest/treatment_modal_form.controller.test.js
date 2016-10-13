fdescribe('TreatmentRecord', function(){
  "use strict";
  var $controller, $rootScope, controller, scope, modalInstance, item;

  beforeEach(function(){
    module('opal.controllers');
    inject(function($injector){
      $controller = $injector.get('$controller');
      $rootScope = $injector.get('$rootScope');
    });

    scope = $rootScope.$new();
    modalInstance = {};
    modalInstance.close = function(x){};
    spyOn(modalInstance, "close");

    item = {
      makeCopy: function(){ return {}; },
      episode: {demographics: [{}]},
      columnName: "treatment",
      save: function(){}
    };
    spyOn(item, "save");

    controller = $controller('TreatmentFormCtrl', {
        $scope: scope,
        $modalInstance: modalInstance,
        item: item,
        profile: {},
        referencedata: {
          toLookuplists: function(){ return {}; }
        },
        episode: {
          makeCopy: function(){ return {}; },
          demographics: [{}],
        },
        metadata: {}
    });
  });

  describe("stop treatment", function(){
    it("should stop treatment and close the modal instance", function(){
      scope.stopTreatment();
      var endDate = moment(scope.editing.treatment.end_date);
      expect(endDate.isSame(moment(), "d")).toBe(true);
      expect(item.save).toHaveBeenCalled();
    });
  });
});
