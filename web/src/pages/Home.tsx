// React import is not needed with React 17+ JSX transform
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';

export default function Home() {
  return (
    <div className="min-h-screen bg-background">
      <main className="container mx-auto px-4 py-16 text-center">
        <h1 className="text-4xl font-bold tracking-tight text-foreground sm:text-5xl md:text-6xl">
          Bienvenido a Sheily
        </h1>
        <p className="mx-auto mt-6 max-w-2xl text-lg text-muted-foreground">
          Una aplicación moderna construida con React, TypeScript y Vite.
        </p>
        <div className="mt-10 flex justify-center gap-4">
          <Button asChild size="lg">
            <Link to="/register">Comenzar</Link>
          </Button>
          <Button asChild variant="outline" size="lg">
            <Link to="/about">Saber más</Link>
          </Button>
        </div>
      </main>
    </div>
  );
}
