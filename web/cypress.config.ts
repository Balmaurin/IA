import { defineConfig } from 'cypress';

export default defineConfig({
  projectId: 'sheily-light',
  viewportWidth: 1280,
  viewportHeight: 800,
  defaultCommandTimeout: 10000,
  video: false,
  retries: {
    runMode: 1,
    openMode: 0,
  },
  e2e: {
    baseUrl: 'http://localhost:3000',
    specPattern: 'cypress/e2e/**/*.cy.{js,jsx,ts,tsx}',
    supportFile: 'cypress/support/e2e.ts',
    setupNodeEvents(on, config) {
      // Configuración de plugins
      require('@cypress/code-coverage/task')(on, config);
      return config;
    },
  },
  component: {
    devServer: {
      framework: 'react',
      bundler: 'vite',
      // Especifica la configuración de Vite
      viteConfig: {
        // Configuración específica de Vite si es necesario
      }
    },
    indexHtmlFile: 'cypress/support/component-index.html',
    specPattern: [
      'src/**/*.cy.{js,jsx,ts,tsx}',
      'cypress/component/**/*.cy.{js,jsx,ts,tsx}'
    ],
    supportFile: 'cypress/support/component.ts',
    setupNodeEvents(on, config) {
      // Configuración de plugins
      require('@cypress/code-coverage/task')(on, config);
      return config;
    },
  },
  // Configuración de cobertura de código
  env: {
    codeCoverage: {
      exclude: [
        'cypress/**/*',
        '**/*.d.ts',
        '**/*.cy.{js,jsx,ts,tsx}',
        '**/*.spec.{js,jsx,ts,tsx}',
        '**/__tests__/**',
        '**/coverage/**',
        '**/node_modules/**',
      ],
    },
  },
});
