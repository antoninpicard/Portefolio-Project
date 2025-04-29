import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';

// Import components
import Dashboard from './pages/Dashboard';
import Devices from './pages/Devices';
import Threats from './pages/Threats';
import Settings from './pages/Settings';
import Login from './pages/Login';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import ProtectedRoute from './components/ProtectedRoute';

function App() {
  const [isAuthenticated, setIsAuthenticated] = React.useState(false);
  
  // Check if user is already logged in
  React.useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      setIsAuthenticated(true);
    }
  }, []);
  
  const handleLogin = (token, user) => {
    localStorage.setItem('token', token);
    localStorage.setItem('user', JSON.stringify(user));
    setIsAuthenticated(true);
  };
  
  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setIsAuthenticated(false);
  };

  return (
    <Router>
      <div className="app">
        {isAuthenticated && (
          <>
            <Navbar onLogout={handleLogout} />
            <div className="container">
              <Sidebar />
              <main className="content">
                <Routes>
                  <Route path="/" element={
                    <ProtectedRoute isAuthenticated={isAuthenticated}>
                      <Dashboard />
                    </ProtectedRoute>
                  } />
                  <Route path="/devices" element={
                    <ProtectedRoute isAuthenticated={isAuthenticated}>
                      <Devices />
                    </ProtectedRoute>
                  } />
                  <Route path="/threats" element={
                    <ProtectedRoute isAuthenticated={isAuthenticated}>
                      <Threats />
                    </ProtectedRoute>
                  } />
                  <Route path="/settings" element={
                    <ProtectedRoute isAuthenticated={isAuthenticated}>
                      <Settings />
                    </ProtectedRoute>
                  } />
                </Routes>
              </main>
            </div>
          </>
        )}
        
        {!isAuthenticated && (
          <Routes>
            <Route path="*" element={<Login onLogin={handleLogin} />} />
          </Routes>
        )}
      </div>
    </Router>
  );
}

export default App;
