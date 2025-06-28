/// <reference types="cypress" />

describe('Home Page', () => {
  beforeEach(() => {
    // Visitar la página de inicio antes de cada prueba
    cy.visit('/');
  });

  it('should display the main heading', () => {
    // Verificar que el título principal esté visible
    cy.get('h1').should('be.visible').and('contain', 'Bienvenido a Sheily');
  });

  it('should display the welcome message', () => {
    // Verificar que el mensaje de bienvenida esté visible
    cy.contains('p', 'Una aplicación moderna construida con React, TypeScript y Vite.').should('be.visible');
  });

  it('should have a working "Comenzar" button', () => {
    // Verificar que el botón "Comenzar" redirija a la página de registro
    cy.contains('a', 'Comenzar')
      .should('have.attr', 'href', '/register')
      .click();
    
    // Verificar que la URL cambió a /register
    cy.url().should('include', '/register');
  });

  it('should have a working "Saber más" button', () => {
    // Verificar que el botón "Saber más" redirija a la página about
    cy.contains('a', 'Saber más')
      .should('have.attr', 'href', '/about')
      .click();
    
    // Verificar que la URL cambió a /about
    cy.url().should('include', '/about');
  });

  it('should pass accessibility tests', () => {
    // Verificar que no hay problemas de accesibilidad
    cy.injectAxe();
    cy.checkA11y();
  });

  it('should be responsive', () => {
    // Verificar que la página es responsive
    cy.viewport('iphone-6');
    cy.get('h1').should('be.visible');
    
    cy.viewport('ipad-2');
    cy.get('h1').should('be.visible');
    
    cy.viewport('macbook-13');
    cy.get('h1').should('be.visible');
  });
});
