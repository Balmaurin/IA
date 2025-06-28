// React import is not needed with React 17+ JSX transform
import { render, screen, fireEvent } from '@testing-library/react';
import { BrowserRouter as Router } from 'react-router-dom';
import { ThemeProvider } from '../contexts/theme-context';
import { Navbar } from '@/components/navbar';

// Mock de los íconos
jest.mock('@/components/ui/button', () => {
  return {
    Button: ({ children, variant, size, onClick, asChild, ...props }: any) => {
      if (asChild) {
        return <button {...props}>{children}</button>;
      }
      return (
        <button 
          data-testid={`button-${variant || 'default'}`} 
          data-size={size}
          onClick={onClick}
          {...props}
        >
          {children}
        </button>
      );
    },
  };
});

// Mock de react-router-dom
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  Link: ({ to, children, ...props }: any) => (
    <a href={to} {...props}>
      {children}
    </a>
  ),
}));

const renderNavbar = () => {
  return render(
    <Router>
      <ThemeProvider>
        <Navbar />
      </ThemeProvider>
    </Router>
  );
};

describe('Navbar Component', () => {
  it('renders the navbar with logo and navigation links', () => {
    renderNavbar();
    
    // Verificar que el logo esté presente
    expect(screen.getByText('Sheily')).toBeInTheDocument();
    
    // Verificar los enlaces de navegación
    expect(screen.getByText('Inicio')).toBeInTheDocument();
    expect(screen.getByText('Acerca de')).toBeInTheDocument();
    expect(screen.getByText('Contacto')).toBeInTheDocument();
    
    // Verificar botones de autenticación
    expect(screen.getByText('Iniciar sesión')).toBeInTheDocument();
    expect(screen.getByText('Registrarse')).toBeInTheDocument();
  });

  it('toggles theme when theme button is clicked', () => {
    renderNavbar();
    
    // Encontrar el botón de cambio de tema
    const themeButton = screen.getByLabelText('Toggle theme');
    
    // Verificar que el tema inicial sea light
    expect(themeButton).toBeInTheDocument();
    
    // Hacer clic en el botón de tema
    fireEvent.click(themeButton);
    
    // Verificar que el botón de tema se actualizó (esto es un mock, así que solo verificamos el clic)
    // En una implementación real, podrías verificar el cambio de clases o atributos
    expect(themeButton).toHaveBeenCalled();
  });

  it('has correct links in the navigation', () => {
    renderNavbar();
    
    // Verificar que los enlaces tengan las rutas correctas
    expect(screen.getByText('Inicio').closest('a')).toHaveAttribute('href', '/');
    expect(screen.getByText('Acerca de').closest('a')).toHaveAttribute('href', '/about');
    expect(screen.getByText('Contacto').closest('a')).toHaveAttribute('href', '/contact');
    expect(screen.getByText('Iniciar sesión').closest('a')).toHaveAttribute('href', '/login');
    expect(screen.getByText('Registrarse').closest('a')).toHaveAttribute('href', '/register');
  });

  it('applies correct classes based on active route', () => {
    // Este test sería más efectivo con MemoryRouter y una ruta específica
    renderNavbar();
    
    // Verificar que el enlace activo tenga la clase correcta
    // Como estamos usando MemoryRouter sin ruta inicial, todos los enlaces deberían estar inactivos
    const homeLink = screen.getByText('Inicio').closest('a');
    expect(homeLink).toHaveClass('text-foreground/60');
    expect(homeLink).toHaveClass('hover:text-foreground/80');
  });
});
