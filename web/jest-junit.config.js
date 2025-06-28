module.exports = {
  suiteName: 'Jest Tests',
  output: './coverage/junit.xml',
  ancestorSeparator: ' > ',
  addFileAttribute: 'true',
  classNameTemplate: '{classname}-{title}',
  titleTemplate: '{classname}-{title}',
  includeConsoleOutput: true,
  outputName: 'JEST_TEST_RESULTS',
  suiteNameTemplate: '{filepath}',
  addAttributeOptions: {
    'data-cy': 'true',
  },
  includeShortConsoleOutput: true,
  reportTestResults: true,
  reportTestSuiteErrors: true,
  reportTestCaseSync: true,
  testCaseSwitchClassnameAndName: false,
  rootDir: '.',
  usePathForSuiteName: true,
};

// This configuration generates JUnit-style XML reports for test results, which can be used by CI/CD pipelines.
// The reports include detailed information about test execution, making it easier to track test failures and performance.
// The output is saved in the coverage directory for easy access and integration with other tools.
