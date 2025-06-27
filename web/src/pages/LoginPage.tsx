import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import './ChatPage.css';

const LoginPage: React.FC = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    const base = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8001';
    try {
      const res = await fetch(`${base}/api/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      });
      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.error || 'Credenciales incorrectas');
      }
      const data = await res.json();
      localStorage.setItem('sheily_token', data.access_token);
      navigate('/chat');
    } catch (err: any) {
      setError(err.message);
    }
  };

  return (
    <div className="chat-container">
      <h1>Login</h1>
      <form onSubmit={handleSubmit} className="chat-form" style={{ maxWidth: '400px' }}>
        <input
          className="chat-input"
          placeholder="Usuario"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          className="chat-input"
          type="password"
          placeholder="Contraseña"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button type="submit" className="chat-submit">
          Entrar
        </button>
      </form>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <Link to="/">Volver al inicio</Link>
    </div>
  );
};

export default LoginPage;
