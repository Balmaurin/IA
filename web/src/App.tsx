import { QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { Toaster } from 'react-hot-toast';
import { RouterProvider } from 'react-router-dom';
import { ThemeProvider } from '@/contexts/theme-context';
import { queryClient } from '@/lib/react-query';
import { router } from '@/routes';
import { TooltipProvider } from '@/components/ui/tooltip';
import { DialogProvider } from '@/components/ui/dialog';
import { Tooltip } from '@/components/ui/tooltip';
import { AuthProvider } from '@/hooks/use-auth';

// Importar estilos globales
import '@/styles/globals.css';

// Componente principal de la aplicación
function App() {
  return (
    <ThemeProvider defaultTheme="system" storageKey="sheily-theme">
      <QueryClientProvider client={queryClient}>
        <AuthProvider>
          <TooltipProvider>
            <DialogProvider>
            <div className="min-h-screen bg-background font-sans antialiased">
              <RouterProvider router={router} />
              <Toaster
                position="top-right"
                toastOptions={{
                  duration: 5000,
                  style: {
                    background: 'hsl(var(--background))',
                    color: 'hsl(var(--foreground))',
                    border: '1px solid hsl(var(--border))',
                    borderRadius: 'var(--radius)',
                    padding: '0.75rem 1rem',
                    boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)',
                  },
                }}
              />
              {import.meta.env.DEV && (
                <ReactQueryDevtools initialIsOpen={false} position="bottom-right" />
              )}
            </div>
          </DialogProvider>
        </TooltipProvider>
      </QueryClientProvider>
      <ReactQueryDevtools initialIsOpen={false} />
    </ThemeProvider>
  );
}

export default App;
