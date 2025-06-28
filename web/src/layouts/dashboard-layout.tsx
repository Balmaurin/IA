import { Outlet } from 'react-router-dom';
import { Sidebar } from '@/components/sidebar';
import { Toaster } from '@/components/ui/toaster';

export function DashboardLayout() {
  return (
    <div className="flex h-screen overflow-hidden bg-background">
      <Sidebar />
      <div className="flex-1 overflow-auto">
        <main className="p-6">
          <Outlet />
        </main>
      </div>
      <Toaster />
    </div>
  );
}

export default DashboardLayout;
