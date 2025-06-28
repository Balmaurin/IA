import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { useTheme } from '@/contexts/theme-context';

export function Navbar() {
  const { theme, toggleTheme } = useTheme();

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-14 items-center">
        <div className="mr-4 flex">
          <Link to="/" className="mr-6 flex items-center space-x-2">
            <span className="font-bold">Sheily</span>
          </Link>
          <nav className="flex items-center space-x-6 text-sm font-medium">
            <Link to="/" className="transition-colors hover:text-foreground/80 text-foreground/60">
              Inicio
            </Link>
            <Link
              to="/about"
              className="transition-colors hover:text-foreground/80 text-foreground/60"
            >
              Acerca de
            </Link>
            <Link
              to="/contact"
              className="transition-colors hover:text-foreground/80 text-foreground/60"
            >
              Contacto
            </Link>
          </nav>
        </div>
        <div className="flex flex-1 items-center justify-between space-x-2 md:justify-end">
          <div className="w-full flex-1 md:w-auto md:flex-none">
            {/* Search bar could go here */}
          </div>
          <nav className="flex items-center space-x-2">
            <Button variant="ghost" size="icon" onClick={toggleTheme} aria-label="Toggle theme">
              {theme === 'dark' ? (
                <span className="i-lucide-sun h-4 w-4" />
              ) : (
                <span className="i-lucide-moon h-4 w-4" />
              )}
            </Button>
            <Button asChild variant="outline">
              <Link to="/login">Iniciar sesión</Link>
            </Button>
            <Button asChild>
              <Link to="/register">Registrarse</Link>
            </Button>
          </nav>
        </div>
      </div>
    </header>
  );
}

export default Navbar;
