import '@testing-library/jest-dom';
import { cleanup } from '@testing-library/react';

// Limpiar el entorno después de cada prueba
afterEach(() => {
  cleanup();
});

// Configuración global para las pruebas
const originalConsoleError = console.error;
const jsDomCssError = 'Error: Could not parse CSS stylesheet';

// Ignorar errores específicos de CSS en las pruebas
console.error = (...args) => {
  if (args.some((arg) => arg.toString().includes(jsDomCssError))) {
    return;
  }
  originalConsoleError(...args);
};

// Configurar el entorno para las pruebas de React
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: jest.fn().mockImplementation((query) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: jest.fn(),
    removeListener: jest.fn(),
    addEventListener: jest.fn(),
    removeEventListener: jest.fn(),
    dispatchEvent: jest.fn(),
  })),
});

// Mock para react-router-dom
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: () => jest.fn(),
  useLocation: () => ({
    pathname: '/',
    search: '',
    hash: '',
    state: null,
    key: 'test-key',
  }),
}));
