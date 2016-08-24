angular.module('opal.services').service(
    'TreatmentRecord', function(){

    return function(x){
        x.formController = "TreatmentFormCtrl";
    };
});
