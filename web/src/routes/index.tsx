import { lazy, Suspense } from 'react';
import { createBrowserRouter, Navigate } from 'react-router-dom';
import { Loader2 } from 'lucide-react';

// Layouts
const AuthLayout = lazy(() => import('@/layouts/auth-layout'));
const MainLayout = lazy(() => import('@/layouts/main-layout'));
const DashboardLayout = lazy(() => import('@/layouts/dashboard-layout'));

// Auth Pages
const LoginPage = lazy(() => import('@/pages/auth/login'));
const RegisterPage = lazy(() => import('@/pages/auth/register'));
const ForgotPasswordPage = lazy(() => import('@/pages/auth/forgot-password'));
const ResetPasswordPage = lazy(() => import('@/pages/auth/reset-password'));

// Main Pages
const HomePage = lazy(() => import('@/pages/home'));
const AboutPage = lazy(() => import('@/pages/about'));
const ContactPage = lazy(() => import('@/pages/contact'));
const PricingPage = lazy(() => import('@/pages/pricing'));
const DocsPage = lazy(() => import('@/pages/docs'));

// Dashboard Pages
const DashboardPage = lazy(() => import('@/pages/dashboard'));
const ProfilePage = lazy(() => import('@/pages/dashboard/profile'));
const TrainingsPage = lazy(() => import('@/pages/dashboard/trainings'));
const TrainingDetailPage = lazy(() => import('@/pages/dashboard/trainings/[id]'));
const MetricsPage = lazy(() => import('@/pages/dashboard/metrics'));
const SettingsPage = lazy(() => import('@/pages/dashboard/settings'));
const NotFoundPage = lazy(() => import('@/pages/not-found'));

// Admin Pages
const AdminLayout = lazy(() => import('@/layouts/admin-layout'));
const AdminDashboardPage = lazy(() => import('@/pages/admin'));
const UsersPage = lazy(() => import('@/pages/admin/users'));
const UserDetailPage = lazy(() => import('@/pages/admin/users/[id]'));
const RolesPage = lazy(() => import('@/pages/admin/roles'));
const PermissionsPage = lazy(() => import('@/pages/admin/permissions'));
const SystemLogsPage = lazy(() => import('@/pages/admin/system-logs'));

// Loading component
const LoadingSpinner = () => (
  <div className="flex h-screen w-full items-center justify-center">
    <Loader2 className="h-12 w-12 animate-spin text-primary" />
  </div>
);

// Suspense wrapper
const withSuspense = (Component: React.ComponentType) => (
  <Suspense fallback={<LoadingSpinner />}>
    <Component />
  </Suspense>
);

// Auth guard
const RequireAuth = ({ children }: { children: React.ReactNode }) => {
  // TODO: Implementar lógica de autenticación
  const isAuthenticated = true; // Ejemplo: usar un hook de autenticación
  
  if (!isAuthenticated) {
    return <Navigate to="/auth/login" replace />;
  }
  
  return <>{children}</>;
};

// Admin guard
const RequireAdmin = ({ children }: { children: React.ReactNode }) => {
  // TODO: Implementar lógica de autorización de administrador
  const isAdmin = true; // Ejemplo: verificar rol de administrador
  
  if (!isAdmin) {
    return <Navigate to="/dashboard" replace />;
  }
  
  return <>{children}</>;
};

// Router configuration
export const router = createBrowserRouter([
  {
    path: '/',
    element: withSuspense(MainLayout),
    children: [
      {
        index: true,
        element: withSuspense(HomePage),
      },
      {
        path: 'about',
        element: withSuspense(AboutPage),
      },
      {
        path: 'contact',
        element: withSuspense(ContactPage),
      },
      {
        path: 'pricing',
        element: withSuspense(PricingPage),
      },
      {
        path: 'docs',
        element: withSuspense(DocsPage),
      },
    ],
  },
  {
    path: '/auth',
    element: withSuspense(AuthLayout),
    children: [
      {
        path: 'login',
        element: withSuspense(LoginPage),
      },
      {
        path: 'register',
        element: withSuspense(RegisterPage),
      },
      {
        path: 'forgot-password',
        element: withSuspense(ForgotPasswordPage),
      },
      {
        path: 'reset-password',
        element: withSuspense(ResetPasswordPage),
      },
    ],
  },
  {
    path: '/dashboard',
    element: (
      <RequireAuth>
        <DashboardLayout />
      </RequireAuth>
    ),
    children: [
      {
        index: true,
        element: withSuspense(DashboardPage),
      },
      {
        path: 'profile',
        element: withSuspense(ProfilePage),
      },
      {
        path: 'trainings',
        children: [
          {
            index: true,
            element: withSuspense(TrainingsPage),
          },
          {
            path: ':id',
            element: withSuspense(TrainingDetailPage),
          },
        ],
      },
      {
        path: 'metrics',
        element: withSuspense(MetricsPage),
      },
      {
        path: 'settings',
        element: withSuspense(SettingsPage),
      },
    ],
  },
  {
    path: '/admin',
    element: (
      <RequireAuth>
        <RequireAdmin>
          <AdminLayout />
        </RequireAdmin>
      </RequireAuth>
    ),
    children: [
      {
        index: true,
        element: withSuspense(AdminDashboardPage),
      },
      {
        path: 'users',
        children: [
          {
            index: true,
            element: withSuspense(UsersPage),
          },
          {
            path: ':id',
            element: withSuspense(UserDetailPage),
          },
        ],
      },
      {
        path: 'roles',
        element: withSuspense(RolesPage),
      },
      {
        path: 'permissions',
        element: withSuspense(PermissionsPage),
      },
      {
        path: 'system-logs',
        element: withSuspense(SystemLogsPage),
      },
    ],
  },
  {
    path: '*',
    element: withSuspense(NotFoundPage),
  },
]);
