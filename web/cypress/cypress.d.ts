// Type definitions for Cypress custom commands

// This file is an ambient module declaration
export {};

declare global {
  // Import types from Cypress
  /// <reference types="cypress" />
  
  // Import JQuery type definitions
  /// <reference types="jquery" />
  
  // Import React type definitions
  /// <reference types="react" />

  // Define types for our custom commands
  interface MountOptions {
    withRouter?: boolean;
    withTheme?: boolean;
    withQueryClient?: boolean;
    [key: string]: any;
  }

  type A11yContext = any;
  type A11yOptions = any;

  // Extend the Window interface to include axe and Cypress
  interface Window {
    Cypress?: any;
    axe?: any;
  }

  // Extend the Cypress namespace
  namespace Cypress {
    interface Chainable<Subject = any> {
      /**
       * Custom command to select DOM element by data-testid attribute
       * @example cy.getByTestId('login-button')
       */
      getByTestId(selector: string, ...args: any[]): Chainable<JQuery<HTMLElement>>;
      
      /**
       * Custom command to login via API
       * @example cy.login('user@example.com', 'password123')
       */
      login(email?: string, password?: string): Chainable<void>;
      
      /**
       * Custom command to logout
       * @example cy.logout()
       */
      logout(): Chainable<void>;
      
      /**
       * Verify page accessibility
       * @example cy.checkA11y()
       */
      checkA11y(
        context?: A11yContext,
        options?: A11yOptions,
        violationCallback?: (violations: any) => void
      ): Chainable<void>;
      
      /**
       * Navigate to a specific route
       * @example cy.navigateTo('/dashboard')
       */
      navigateTo(path: string): Chainable<void>;
      
      /**
       * Assert current route
       * @example cy.assertRoute('/dashboard')
       */
      assertRoute(path: string): Chainable<void>;
      
      /**
       * Mount a React component
       * @example cy.mount(<MyComponent />)
       */
      mount(component: React.ReactNode, options?: MountOptions): Chainable<void>;
    }
  }
}
