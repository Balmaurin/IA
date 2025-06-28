export default {
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['<rootDir>/src/__tests__/setupTests.ts'],
  testMatch: ['**/__tests__/**/*.test.[jt]s?(x)'],
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1',
    '^(\\.{1,2}/.*)\\.js$': '$1',
    '^.+\\.(css|less|scss|sass|svg)$': 'identity-obj-proxy',
  },
  transform: {
    '^.+\\.(t|j)sx?$': ['@swc/jest', {
      jsc: {
        parser: {
          syntax: 'typescript',
          tsx: true,
          decorators: true,
        },
        transform: {
          react: {
            runtime: 'automatic',
          },
        },
      },
    }],
  },
  transformIgnorePatterns: [
    'node_modules/(?!(.*\\.mjs$|@?vite|@?react|@?@radix-ui|@?@headlessui|@?@testing-library|@?@babel|@?@tanstack))',
  ],
  moduleDirectories: ['node_modules', 'src'],
  moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx', 'json', 'node'],
  
  // Configuración de cobertura
  collectCoverage: true,
  collectCoverageFrom: [
    'src/**/*.{ts,tsx}',
    '!src/**/*.d.ts',
    '!src/main.tsx',
    '!src/vite-env.d.ts',
    '!src/__tests__/**/*',
    '!src/**/*.stories.{ts,tsx}',
    '!src/**/index.{ts,tsx}',
  ],
  coverageDirectory: 'coverage',
  coverageReporters: [
    'text',
    'lcov',
    'json',
    'text-summary',
    ['lcov', { projectRoot: '/' }],
  ],
  coverageThreshold: {
    global: {
      statements: 70,
      branches: 60,
      functions: 65,
      lines: 70,
    },
  },
  
  // Configuración de informes
  reporters: [
    'default',
    [
      'jest-html-reporter',
      {
        pageTitle: 'Test Report',
        outputPath: 'coverage/test-report.html',
        includeFailureMsg: true,
        includeConsoleLog: true,
      },
    ],
  ],
  
  // Configuración de visualización
  verbose: true,
  testLocationInResults: true,
  testResultsProcessor: 'jest-sonar-reporter',
};
