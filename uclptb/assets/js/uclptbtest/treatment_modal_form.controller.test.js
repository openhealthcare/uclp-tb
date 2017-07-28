describe('TreatmentRecord', function(){
  "use strict";
  var $controller, $rootScope, controller, scope, modalInstance, item, opalTestHelper;

  beforeEach(function(){
    module('opal.controllers');
    module('opal.test');
    inject(function($injector){
      $controller = $injector.get('$controller');
      $rootScope = $injector.get('$rootScope');
      opalTestHelper = $injector.get('opalTestHelper');
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
    var episode = opalTestHelper.newEpisode($rootScope);

    controller = $controller('TreatmentFormCtrl', {
        $scope: scope,
        $modalInstance: modalInstance,
        item: item,
        profile: {},
        referencedata: {
          toLookuplists: function(){ return {}; }
        },
        episode: episode,
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
