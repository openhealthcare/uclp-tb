module.exports = function(config){
  var opalPath = process.env.OPAL_LOCATION;
  var karmaDefaults = require(opalPath + '/opal/tests/js_config/karma_defaults.js');
  var baseDir = __dirname + '/..';
  var coverageFiles = [
    __dirname + '/../lib/opal-tb/tb/static/js/**/*.js',
    __dirname + '/../uclptb/assets/js/uclptb/controllers/**/*.js',
    __dirname + '/../uclptb/assets/js/uclptb/services/**/*.js',

    // 'opaltest/*.js',

    // '../../../../elcid/elcid/assets/js/elcidtest/*.js',
  ];
  var includedFiles = [
    __dirname + '/../lib/opal-tb/tb/static/js/**/*.js',
    __dirname + '/../uclptb/assets/js/uclptb/controllers/**/*.js',
    __dirname + '/../uclptb/assets/js/uclptb/services/**/*.js',

    __dirname + '/../uclptb/assets/js/uclptbtest/**/*.js',
    __dirname + '/../lib/opal-tb/tb/static/js/tbtest/**/*.js',
  ];

  var defaultConfig = karmaDefaults(includedFiles, baseDir, coverageFiles);
  config.set(defaultConfig);
};
