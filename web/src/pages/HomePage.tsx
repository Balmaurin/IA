import React from 'react';
import { Link } from 'react-router-dom';

const HomePage: React.FC = () => (
  <div style={{ maxWidth: 400, margin: '0 auto', textAlign: 'center' }}>
    <h1>Bienvenido a Sheily-Light</h1>
    <p>Accede a las funciones principales:</p>
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1em', alignItems: 'center' }}>
      <Link className="chat-submit" to="/login">Iniciar sesión</Link>
      <Link className="chat-submit" to="/register">Registrarse</Link>
      <Link className="chat-submit" to="/chat">Ir al chat</Link>
    </div>
  </div>
);

export default HomePage;
