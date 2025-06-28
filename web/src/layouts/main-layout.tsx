import { Outlet } from 'react-router-dom';
import { Toaster } from '@/components/ui/toaster';
import { Navbar } from '@/components/navbar';

export function MainLayout() {
  return (
    <div className="min-h-screen bg-background flex flex-col">
      <Navbar />
      <main className="flex-1">
        <Outlet />
      </main>
      <Toaster />
    </div>
  );
}

export default MainLayout;
