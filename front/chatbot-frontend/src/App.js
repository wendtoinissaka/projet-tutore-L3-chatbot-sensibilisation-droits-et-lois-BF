import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Chatbot from './components/Chatbot';
import Login from './components/auth/LoginForm';
import Register from './components/auth/RegisterForm';  // Nouvelle page d'inscription
import LegalInfo from './components/legalInformations/LegalInfo';
import Navbar from './components/Navbar';

function App() {
  return (
    <Router>
      <div className="App">
        <Navbar />
        <Routes>
          <Route path="/" element={<Chatbot />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />  {/* Nouvelle route */}
          <Route path="/legal" element={<LegalInfo />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
