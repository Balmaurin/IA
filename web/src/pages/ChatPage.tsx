import React, { useState, useRef, useEffect } from 'react';
import './ChatPage.css';
import { Link } from 'react-router-dom';

interface Message {
  id: number;
  text: string;
}

const ChatPage: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const nextId = useRef(0);
  const endRef = useRef<HTMLDivElement | null>(null);

  const addMessage = (text: string) => {
    setMessages((prev) => [...prev, { id: nextId.current++, text }]);
  };

  const addBotMessage = (text: string) => {
    setMessages((prev) => [...prev, { id: nextId.current++, text: `🤖 ${text}` }]);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const trimmed = input.trim();
    if (trimmed) {
      addMessage(trimmed);
      setInput('');

      const base = import.meta.env.VITE_API_URL || 'http://localhost:8001';
      let messageToSend = trimmed;
      // Solo añade la hora si el prompt lo pide (por ejemplo, contiene 'hora')
      if (/\bhora\b/i.test(trimmed)) {
        let now = new Date().toISOString();
        try {
          const timeRes = await fetch(`${base}/api/utils/time`);
          const timeData = await timeRes.json();
          if (timeData && timeData.now) now = timeData.now;
        } catch (err) {
          // Si falla, se mantiene la hora local
        }
        messageToSend += `\n\n[DATO] Hora actual: ${now}`;
      }
      // call backend
      const token = localStorage.getItem('sheily_token');
      if (!token) {
        window.location.href = '/login';
        return;
      }
      const headers: Record<string, string> = { 'Content-Type': 'application/json' };
      if (token) headers.Authorization = `Bearer ${token}`;
      fetch(`${base}/api/chat/chat/`, {
        method: 'POST',
        headers,
        body: JSON.stringify({ message: messageToSend }),
      })
        .then(async (r) => {
          if (r.status === 401) {
            // Token inválido o expirado: limpiamos y redirigimos
            localStorage.removeItem('sheily_token');
            window.location.href = '/login';
            return;
          }
          const data = await r.json();
          if (data.answer) addBotMessage(data.answer);
        })
        .catch((err) => {
          addBotMessage('Error: ' + err.message);
        });
    }
  };

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleLogout = () => {
    localStorage.removeItem('sheily_token');
    window.location.href = '/login';
  };

  return (
    <main className="chat-container" role="main">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h1>Chat</h1>
        <button onClick={handleLogout} className="chat-submit" style={{ marginLeft: '1em' }}>Logout</button>
      </div>
      <div className="chat-box" role="log" aria-live="polite" aria-relevant="additions">
        {messages.map((m) => (
          <div key={m.id} className="chat-message">
            {m.text}
          </div>
        ))}
        <div ref={endRef} />
      </div>
      <form onSubmit={handleSubmit} className="chat-form">
        <label htmlFor="chat-input" className="visually-hidden">Escribir mensaje</label>
        <input
          id="chat-input"
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Escribe un mensaje..."
          className="chat-input"
          aria-label="Escribe un mensaje"
        />
        <button type="submit" className="chat-submit" aria-label="Enviar mensaje">
          Enviar
        </button>
      </form>
      <Link to="/">Volver al inicio</Link>
    </main>
  );
};

export default ChatPage;
