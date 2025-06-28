import { Link, useLocation } from 'react-router-dom';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import { useTheme } from '@/contexts/theme-context';

const navItems = [
  {
    title: 'Dashboard',
    href: '/dashboard',
    icon: 'i-lucide-layout-dashboard',
  },
  {
    title: 'Entrenamientos',
    href: '/dashboard/trainings',
    icon: 'i-lucide-dumbbell',
  },
  {
    title: 'Métricas',
    href: '/dashboard/metrics',
    icon: 'i-lucide-bar-chart-2',
  },
  {
    title: 'Perfil',
    href: '/dashboard/profile',
    icon: 'i-lucide-user',
  },
  {
    title: 'Configuración',
    href: '/dashboard/settings',
    icon: 'i-lucide-settings',
  },
];

export function Sidebar() {
  const location = useLocation();
  const { theme, toggleTheme } = useTheme();

  return (
    <div className="hidden w-64 border-r bg-background md:flex flex-col">
      <div className="flex h-16 items-center border-b px-6">
        <Link to="/" className="flex items-center space-x-2">
          <span className="text-xl font-bold">Sheily</span>
        </Link>
      </div>
      <nav className="flex-1 space-y-1 p-4">
        {navItems.map((item) => (
          <Button
            key={item.href}
            asChild
            variant={location.pathname === item.href ? 'secondary' : 'ghost'}
            className={cn(
              'w-full justify-start',
              location.pathname === item.href && 'font-medium'
            )}
          >
            <Link to={item.href} className="flex items-center">
              <span className={cn('mr-2 h-4 w-4', item.icon)} />
              {item.title}
            </Link>
          </Button>
        ))}
      </nav>
      <div className="border-t p-4">
        <Button
          variant="ghost"
          size="sm"
          className="w-full justify-start"
          onClick={toggleTheme}
        >
          <span className="mr-2 h-4 w-4 i-lucide-moon" />
          {theme === 'dark' ? 'Modo Claro' : 'Modo Oscuro'}
        </Button>
      </div>
    </div>
  );
}

export default Sidebar;
