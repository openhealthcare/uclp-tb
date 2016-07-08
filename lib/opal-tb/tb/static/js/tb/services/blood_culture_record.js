angular.module('opal.services').service(
    'BloodCultureRecord', function(){

    return function(x){
        x.formController = "BloodCultureFormCtrl";
    };
});
