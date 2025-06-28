import React from 'react';
import { mount } from '@cypress/react';
import { MemoryRouter } from 'react-router-dom';
import { ThemeProvider } from '@/contexts/theme-context';
import Navbar from '@/components/navbar';

// Mock del contexto de autenticación si es necesario
const MockProviders = ({ children }: { children: React.ReactNode }) => (
  <MemoryRouter>
    <ThemeProvider>
      {children}
    </ThemeProvider>
  </MemoryRouter>
);

describe('<Navbar />', () => {
  beforeEach(() => {
    // Renderizar el componente Navbar para cada prueba
    mount(
      <MockProviders>
        <Navbar />
      </MockProviders>
    );
  });

  it('renders the navbar with logo and navigation links', () => {
    // Verificar que el logo esté presente
    cy.contains('Sheily').should('be.visible');
    
    // Verificar que los enlaces de navegación estén presentes
    cy.contains('Inicio').should('be.visible');
    cy.contains('Acerca de').should('be.visible');
    cy.contains('Contacto').should('be.visible');
    
    // Verificar que los botones de autenticación estén presentes
    cy.contains('Iniciar sesión').should('be.visible');
    cy.contains('Registrarse').should('be.visible');
  });

  it('navigates to the correct routes when links are clicked', () => {
    // Verificar que los enlaces tengan las rutas correctas
    cy.get('a[href="/"]').should('exist');
    cy.get('a[href="/about"]').should('exist');
    cy.get('a[href="/contact"]').should('exist');
    cy.get('a[href="/login"]').should('exist');
    cy.get('a[href="/register"]').should('exist');
  });

  it('toggles theme when theme button is clicked', () => {
    // Verificar que el botón de tema esté presente
    cy.get('button[aria-label="Toggle theme"]').should('be.visible');
    
    // Hacer clic en el botón de tema
    cy.get('button[aria-label="Toggle theme"]').click();
    
    // Verificar que el tema haya cambiado (ajustar según tu implementación)
    cy.get('html').should('have.class', 'dark');
  });

  it('has proper accessibility attributes', () => {
    // Verificar atributos ARIA
    cy.get('nav').should('have.attr', 'aria-label', 'Navegación principal');
    cy.get('button[aria-label="Toggle theme"]').should('have.attr', 'aria-pressed');
    
    // Verificar que los enlaces tengan texto descriptivo
    cy.contains('a', 'Inicio').should('have.attr', 'aria-label', 'Ir a la página de inicio');
  });
});
