import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { GoogleLogin } from 'react-google-login';
function LoginForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('/api/auth/login', { email, password });
      if (response.data.message === 'Login successful') {
        alert('Login successful');
        navigate('/');  // Redirection après connexion réussie
      }
    } catch (error) {
      alert('Login failed');
    }
  };

  const handleGoogleLoginSuccess = async (response) => {
    try {
      const result = await axios.get('/api/auth/google-login', {
        headers: {
          Authorization: `Bearer ${response.tokenId}`,
        },
      });
      alert(result.data.message);
      navigate('/');  // Redirection après connexion Google
    } catch (error) {
      alert('Google login failed');
    }
  };

  return (
    <div className="login-container">
      <h2>Login</h2>
      <form onSubmit={handleLogin}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button type="submit">Login</button>
      </form>
      <div className="google-login">
        <GoogleLogin
          clientId={process.env.REACT_APP_GOOGLE_CLIENT_ID}
          buttonText="Login with Google"
          onSuccess={handleGoogleLoginSuccess}
          onFailure={(response) => console.log('Google login failed', response)}
          cookiePolicy={'single_host_origin'}
          redirectUri="http://localhost:3000"  // URI qui doit correspondre à celui autorisé dans Google Cloud
        />
      </div>
    </div>
  );
}

export default LoginForm;
