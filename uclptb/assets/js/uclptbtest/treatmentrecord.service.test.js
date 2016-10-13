fdescribe('TreatmentRecord', function(){
  "use strict";
  var TreatmentRecord;
  var today = moment();
  var yesterday = moment().subtract(1, "d");
  var two_days_ago = moment().subtract(2, "d");

  beforeEach(function(){
    module('opal.services');
    inject(function($injector){
        TreatmentRecord = $injector.get('TreatmentRecord');
    });
  });

  it("should set the stopped date to the end date if available", function(){
    var item = {
      end_date: yesterday,
      planned_end_date: today
    };
    TreatmentRecord(item);
    expect(item.stoppedDate).toEqual(yesterday);
  });

  it("should set the default the stopped date to the planned_end_date", function(){
    var item = {
      planned_end_date: today
    };
    TreatmentRecord(item);
    expect(item.stoppedDate).toEqual(today);
  });

  it("should not set completed if there is no planned end date", function(){
    var item = {};
    TreatmentRecord(item);
    expect(item.completed).toBe(false);
  });

  it("should set completed if there is no end date and we're before today", function(){
    var item = {planned_end_date: yesterday};
    TreatmentRecord(item);
    expect(item.completed).toBe(true);
  });

  it("should not set completed if the end date is before the planned end date", function(){
    var item = {
      end_date: two_days_ago,
      planned_end_date: yesterday
    };
    TreatmentRecord(item);
    expect(item.completed).toBe(false);
  });

  it("should set completed if the end date is after the planned end date", function(){
    var item = {
      end_date: yesterday,
      planned_end_date: two_days_ago
    };
    TreatmentRecord(item);
    expect(item.completed).toBe(true);
  });

  it("should set stopped early if the end date is before the planned end date", function(){
    var item = {
      end_date: two_days_ago,
      planned_end_date: yesterday
    };
    TreatmentRecord(item);
    expect(item.stoppedEarly).toBe(true);
  });
});
