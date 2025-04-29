import React, { useState } from 'react';
import { FaShieldAlt, FaLock, FaUser } from 'react-icons/fa';
import './Login.css';

const Login = ({ onLogin }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  
  const handleSubmit = (e) => {
    e.preventDefault();
    setError('');
    
    if (!username || !password) {
      setError('Please enter both username and password');
      return;
    }
    
    setLoading(true);
    
    // In a real app, this would make an API call to authenticate
    // For this demo, we'll simulate a successful login after a short delay
    setTimeout(() => {
      // For demo purposes, accept any login
      const token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.example-token';
      const user = { username, role: 'admin' };
      
      setLoading(false);
      onLogin(token, user);
    }, 1000);
  };

  return (
    <div className="login-container">
      <div className="login-form">
        <div className="login-logo">
          <FaShieldAlt className="logo-icon" />
          <h1>CyberGuard</h1>
          <p>Network Security Platform</p>
        </div>
        
        {error && <div className="login-error">{error}</div>}
        
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <div className="input-icon-wrapper">
              <FaUser className="input-icon" />
              <input
                type="text"
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                disabled={loading}
              />
            </div>
          </div>
          
          <div className="form-group">
            <div className="input-icon-wrapper">
              <FaLock className="input-icon" />
              <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                disabled={loading}
              />
            </div>
          </div>
          
          <button 
            type="submit" 
            className="login-button"
            disabled={loading}
          >
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>
        
        <div className="login-footer">
          <p>Demo credentials:</p>
          <p>Username: admin | Password: password</p>
        </div>
      </div>
    </div>
  );
};

export default Login;
