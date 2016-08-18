describe('TBDOTHistory', function(){
  var controller, scope, $rootScope, $controller;

  beforeEach(function(){
    module('opal.controllers');
    inject(function($injector){
        $rootScope   = $injector.get('$rootScope');
        $controller  = $injector.get('$controller');
    });

    scope = $rootScope.$new();
    scope.editing = {demographics: {}, social_history: {}};

    controller = $controller('DOTHistoryCtrl', {
      scope: scope,
      step: {},
      episode: {}
    });
  });



  describe('history chunking', function(){
    beforeEach(function(){
      var observedTreatments = [
        {date: moment(new Date(2016, 5, 5)), drug: "Aspirin", dose: "200g"},
        {date: moment(new Date(2016, 5, 5)), drug: "Paracetomol", dose: "100g"},
        {date: moment(new Date(2016, 5, 6)), drug: "Aspirin", dose: "200g"},
        {date: moment(new Date(2016, 5, 6)), drug: "Paracetomol", dose: "100g"},
        {date: moment(new Date(2016, 5, 7)), drug: "Aspirin", dose: "100g"},
        {date: moment(new Date(2016, 5, 7)), drug: "Paracetomol", dose: "100g"},
      ];
      scope.chunkArray(observedTreatments);
    });

    it('should chunk the array based on treatments', function(){
      // we expect 2 chunks for the 2 different treatments (because aspirin changes does)
      expect(scope.treatmentChunks.length).toBe(2);
    });

    it('should order the chunks by negative date', function(){
        expect(scope.treatmentChunks[0][0].date.isSame(moment(new Date(2016, 5, 7)), "d"));
    });

    it('should extract the drugs from the first chunk', function(){
        expect(scope.treatmentChunks[0][0].drugs).toEqual(['Aspirin', 'Paracetomol']);
        expect(scope.treatmentChunks[0][0].doses).toEqual(['100g', '100g']);
    })

    it('should order the internal chunks by negative date', function(){
        expect(scope.treatmentChunks[1][0].date.isSame(moment(new Date(2016, 5, 6)), "d"));
        expect(scope.treatmentChunks[1][0].date.isSame(moment(new Date(2016, 5, 5)), "d"));
    });

    it('should sort drugs and doses and within chunks these should be the same order', function(){
        expect(scope.treatmentChunks[0][0].drugs).toEqual(['Aspirin', 'Paracetomol']);
        expect(scope.treatmentChunks[0][0].doses).toEqual(['100g', '100g']);
        expect(scope.treatmentChunks[1][0].drugs).toEqual(scope.treatmentChunks[1][1].drugs);
        expect(scope.treatmentChunks[1][0].dose).toEqual(scope.treatmentChunks[1][1].dose);
    });
  });
});
