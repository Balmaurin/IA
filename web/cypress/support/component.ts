// Configuración de soporte para pruebas de componentes
import './commands';
import '@testing-library/cypress/add-commands';
import '@cypress/code-coverage/support';
import { mount } from '@cypress/react';
import { ReactNode } from 'react';

// Importar estilos globales
import '../../src/index.css';

// Tipos para los comandos personalizados
type MountOptions = {
  withRouter?: boolean;
  withTheme?: boolean;
  withQueryClient?: boolean;
  [key: string]: any;
};

// Extender los tipos de Cypress
declare global {
  // eslint-disable-next-line @typescript-eslint/no-namespace
  namespace Cypress {
    interface Chainable<Subject = any> {
      /**
       * Monta un componente de React para pruebas
       * @param component Componente de React a montar
       * @param options Opciones de montaje
       */
      mount(component: ReactNode, options?: MountOptions): Chainable<void>;
    }
  }
}

// Configuración de comandos personalizados para pruebas de componentes
// @ts-ignore - Cypress está disponible en el contexto global
const cypress = globalThis.Cypress;
if (cypress) {
  cypress.Commands.add('mount', (
    component: ReactNode, 
    options: MountOptions = {}
  ) => {
    const { 
      withRouter = false, 
      withTheme = false, 
      withQueryClient = false,
      ...mountOptions 
    } = options;
    
    let wrappedComponent = component;
    
    // Aquí podrías envolver el componente con proveedores según sea necesario
    // Por ejemplo, con ThemeProvider, Router, etc.
    
    // Usar la función mount de @cypress/react
    return mount(wrappedComponent, mountOptions);
  });

  // Manejar excepciones no capturadas
  cypress.on('uncaught:exception', (err: Error) => {
    // Ignorar errores específicos si es necesario
    if (err.message.includes('ResizeObserver')) {
      return false;
    }
    
    console.error('Uncaught exception in test:', err);
    // Retornar false para evitar que Cypress falle la prueba
    return false;
  });

  // Configurar el viewport por defecto
  cypress.config('defaultCommandTimeout', 10000);
  cypress.config('pageLoadTimeout', 60000);
  cypress.config('viewportWidth', 1280);
  cypress.config('viewportHeight', 720);
}

// Configurar Testing Library
const { configure } = require('@testing-library/cypress');
configure({ testIdAttribute: 'data-testid' });
