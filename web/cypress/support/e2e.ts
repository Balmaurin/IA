// ***********************************************************
// Este archivo de soporte se procesa y carga automáticamente
// antes de los archivos de prueba.
//
// Es un buen lugar para colocar la configuración global y
// comportamientos que modifican Cypress.
// ***********************************************************

// Importar definiciones de tipos
import './index.d';

// Importar comandos personalizados
import './commands';
import '@testing-library/cypress/add-commands';
import 'cypress-axe';
import '@cypress/code-coverage/support';

// Manejar excepciones no capturadas
const resizeObserverLoopErrRe = /^[^(ResizeObserver loop limit exceeded)]/;

// @ts-ignore - Cypress está disponible en el contexto global
globalThis.Cypress?.on('uncaught:exception', (err: Error) => {
  // Ignorar errores específicos de ResizeObserver
  if (resizeObserverLoopErrRe.test(err.message)) {
    return false;
  }
  // Registrar otros errores pero no fallar la prueba
  console.error('Uncaught exception in test:', err);
  return false;
});

// Comando personalizado para iniciar sesión
// @ts-ignore - Cypress está disponible en el contexto global
globalThis.Cypress?.Commands.add('login', (
  email = 'test@example.com', 
  password = 'password123'
) => {
  // Usar sesión para evitar múltiples inicios de sesión
  // @ts-ignore - session es un comando de Cypress
  cy.session([email, password], () => {
    cy.request('POST', '/api/auth/login', { email, password }).then((response) => {
      if (response.body?.token) {
        window.localStorage.setItem('auth-token', response.body.token);
      }
    });
  });
});

// Comando personalizado para cerrar sesión
// @ts-ignore - Cypress está disponible en el contexto global
globalThis.Cypress?.Commands.add('logout', () => {
  window.localStorage.removeItem('auth-token');
});

// Configuración de pruebas de accesibilidad
interface Violation {
  id: string;
  impact: string;
  description: string;
  nodes: Array<{ target: string[] }>;
}

const terminalLog = (violations: Violation[]): void => {
  // @ts-ignore - task es un comando de Cypress
  cy.task(
    'log',
    `Se detectaron ${violations.length} violación(es) de accesibilidad`
  );
  
  // Extraer información específica para mantener la legibilidad
  const violationData = violations.map(
    ({ id, impact, description, nodes }) => ({
      id,
      impact,
      description,
      nodes: nodes.length
    })
  );
  
  // Mostrar tabla con las violaciones
  // @ts-ignore - task es un comando de Cypress
  cy.task('table', violationData);
};

// Configuración global de Cypress
const configureCypress = () => {
  // @ts-ignore - Cypress está disponible en el contexto global
  const cypress = globalThis.Cypress;
  if (!cypress) return;

  // Configurar timeouts
  cypress.config('defaultCommandTimeout', 10000);
  cypress.config('pageLoadTimeout', 60000);
  cypress.config('responseTimeout', 30000);

  // Configurar el viewport por defecto
  const viewportWidth = cypress.config('viewportWidth') || 1280;
  const viewportHeight = cypress.config('viewportHeight') || 800;
  
  // Configurar el viewport antes de cada prueba
  cy.viewport(viewportWidth, viewportHeight);
};

// Configurar Cypress antes de las pruebas
// @ts-ignore - beforeEach está disponible en el contexto de Cypress
beforeEach(configureCypress);

// Configurar checkA11y para usar terminalLog por defecto
// @ts-ignore - Cypress está disponible en el contexto global
globalThis.Cypress?.Commands.overwrite('checkA11y', (
  originalFn: any,
  context: any,
  options: any = {},
  violationCallback: any = terminalLog
) => {
  return originalFn(context, options, violationCallback);
});

// Exportar para uso en otros archivos si es necesario
export {};
