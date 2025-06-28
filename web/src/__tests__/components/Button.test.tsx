import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { Button } from '@/components/ui/button';

describe('Button Component', () => {
  it('renders button with default variant and size', () => {
    render(<Button>Click me</Button>);
    const button = screen.getByRole('button', { name: /click me/i });
    
    // Verificar que el botón está en el documento
    expect(button).toBeInTheDocument();
    
    // Verificar que tiene las clases de Tailwind por defecto
    expect(button).toHaveClass('inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 h-10 px-4 py-2');
  });

  it('applies custom className', () => {
    render(<Button className="custom-class">Custom Button</Button>);
    const button = screen.getByRole('button', { name: /custom button/i });
    
    // Verificar que se aplica la clase personalizada
    expect(button).toHaveClass('custom-class');
  });

  it('handles click events', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click me</Button>);
    const button = screen.getByRole('button', { name: /click me/i });
    
    // Simular clic
    button.click();
    
    // Verificar que se llamó al manejador de clic
    expect(handleClick).toHaveBeenCalledTimes(1);
  });
});
