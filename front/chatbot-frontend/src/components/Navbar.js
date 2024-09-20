import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
  return (
    <nav>
      <ul>
        <li><Link to="/">Chatbot</Link></li>
        <li><Link to="/login">Login</Link></li>
        <li><Link to="/legal">Legal Info</Link></li>
      </ul>
    </nav>
  );
};

export default Navbar;
