import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import ChatPage from './pages/ChatPage';
import LoginPage from './pages/LoginPage';
import RegisterForm from './components/auth/RegisterForm';
import PrivateRoute from './components/auth/PrivateRoute';
const App: React.FC = () => (
  <BrowserRouter>
    <Routes>
      <Route path='/' element={<HomePage />} />
      <Route path='/login' element={<LoginPage />} />
      <Route path='/register' element={<RegisterForm />} />
      <Route path='/chat' element={<PrivateRoute><ChatPage /></PrivateRoute>} />
    </Routes>
  </BrowserRouter>
);
export default App;
