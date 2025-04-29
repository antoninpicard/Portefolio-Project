import React, { useContext } from 'react';
import { Link } from 'react-router-dom';
import { FaDrone, FaCog } from 'react-icons/fa';
import WebSocketContext from '../contexts/WebSocketContext';
import './Navbar.css';

const Navbar = () => {
  const { connected } = useContext(WebSocketContext);
  
  return (
    <nav className="navbar">
      <div className="navbar-logo">
        <Link to="/">
          <FaDrone className="logo-icon" />
          <h1>SwarmDrone</h1>
        </Link>
      </div>
      
      <div className="navbar-actions">
        <div className="connection-status">
          <div className={`connection-indicator ${connected ? 'connected' : 'disconnected'}`}></div>
          <span>{connected ? 'Connected' : 'Disconnected'}</span>
        </div>
        
        <Link to="/settings" className="icon-button">
          <FaCog />
        </Link>
      </div>
    </nav>
  );
};

export default Navbar;
