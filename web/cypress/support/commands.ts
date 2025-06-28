// ***********************************************
// Cypress Custom Commands
// ***********************************************

// Import types from Cypress
/// <reference types="cypress" />

// Import React types
import React from 'react';
import { mount } from 'cypress/react';

// Local types
type MountOptions = {
  withRouter?: boolean;
  withTheme?: boolean;
  withQueryClient?: boolean;
  [key: string]: any;
};

type A11yContext = any;  // Can be improved with more specific types
type A11yOptions = any;  // Can be improved with more specific types

// Extend Cypress Chainable interface
declare global {
  // eslint-disable-next-line @typescript-eslint/no-namespace
  namespace Cypress {
    interface Chainable {
      getByTestId(selector: string, ...args: any[]): Chainable<JQuery<HTMLElement>>;
      navigateTo(path: string): Chainable<void>;
      assertRoute(path: string): Chainable<void>;
      login(email?: string, password?: string): Chainable<void>;
      logout(): Chainable<void>;
      checkA11y(
        context?: A11yContext,
        options?: A11yOptions,
        violationCallback?: (violations: any) => void
      ): Chainable<void>;
      mount(component: React.ReactNode, options?: MountOptions): Chainable<void>;
    }
  }
}

// Create a wrapper for command registration
const registerCommand = <T = any>(
  name: string,
  options: Cypress.CommandOptions,
  fn: Cypress.CommandFn<T>
): void => {
  // @ts-ignore - Cypress.Commands.add is dynamically typed
  Cypress.Commands.add(name, options, fn);
};

// Command to get elements by data-testid
registerCommand('getByTestId', { prevSubject: 'optional' }, (subject, selector: string, ...args: any[]) => {
  return cy.get(`[data-testid="${selector}"]`, ...args);
});

// Command to navigate to a route
registerCommand('navigateTo', {}, (path: string) => {
  return cy.visit(path);
});

// Command to verify current route
registerCommand('assertRoute', {}, (path: string) => {
  return cy.location('pathname').should('eq', path);
});

// Authentication commands
registerCommand('login', {}, (email = 'test@example.com', password = 'password123') => {
  return cy.request({
    method: 'POST',
    url: '/api/auth/login',
    body: { email, password },
    failOnStatusCode: false
  }).then((response) => {
    if (response.status === 200) {
      const { token, user } = response.body;
      window.localStorage.setItem('authToken', token);
      window.localStorage.setItem('user', JSON.stringify(user));
      return cy.wrap(user);
    }
    throw new Error(`Login failed: ${response.body?.message || 'Unknown error'}`);
  });
});

registerCommand('logout', {}, () => {
  window.localStorage.removeItem('authToken');
  window.localStorage.removeItem('user');
  return cy.visit('/login');
});

// Accessibility testing command
registerCommand(
  'checkA11y',
  {
    prevSubject: ['optional', 'element', 'window', 'document']
  },
  (
    subject: any,
    context: A11yContext = {},
    options: A11yOptions = {},
    violationCallback?: (violations: any) => void
  ) => {
    const checkContext = subject ? cy.wrap(subject) : cy.document();
    
    return checkContext.then(() => {
      return cy.window({ log: false }).then((win) => {
        const winWithAxe = win as typeof win & { axe?: any };
        
        return new Cypress.Promise<void>((resolve) => {
          if (winWithAxe.axe) {
            resolve();
          } else {
            const script = win.document.createElement('script');
            script.src = 'https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.4.3/axe.min.js';
            script.onload = () => resolve();
            win.document.head.appendChild(script);
          }
        }).then(() => {
          const defaultOptions: A11yOptions = {
            runOnly: {
              type: 'tag',
              values: ['wcag2a', 'wcag2aa', 'best-practice']
            }
          };

          const a11yOptions = { ...defaultOptions, ...options };
          
          return new Cypress.Promise<void>((resolve, reject) => {
            if (!winWithAxe.axe) {
              return reject(new Error('axe-core not loaded'));
            }

            winWithAxe.axe.run(
              context || win.document, 
              a11yOptions, 
              (err: Error, results: any) => {
                if (err) return reject(err);

                if (results.violations?.length > 0 && violationCallback) {
                  violationCallback(results.violations);
                }

                const criticalViolations = results.violations?.filter((v: any) => 
                  !a11yOptions.includedImpacts || 
                  a11yOptions.includedImpacts.includes(v.impact)
                ) || [];

                if (criticalViolations.length > 0) {
                  const errorMsg = `Found ${criticalViolations.length} accessibility violations`;
                  cy.log(errorMsg);
                  return reject(new Error(errorMsg));
                }
                
                resolve();
              }
            );
          });
        });
      });
    });
  }
);

// Component mounting command
registerCommand('mount', {}, (component: React.ReactNode, options: MountOptions = {}) => {
  const { withRouter = false, withTheme = false, withQueryClient = false, ...mountOptions } = options;
  let wrappedComponent = component;
  
  // Wrap with providers as needed
  // Example: if (withTheme) { wrappedComponent = <ThemeProvider>...</ThemeProvider> }
  
  return mount(wrappedComponent, mountOptions);
});

// Handle uncaught exceptions
Cypress.on('uncaught:exception', (err) => {
  console.error('Uncaught exception in test:', err);
  return false; // Prevent test from failing
});

// Export types for use in test files
export {};
