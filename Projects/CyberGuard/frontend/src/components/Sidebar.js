import React from 'react';
import { NavLink } from 'react-router-dom';
import { FaHome, FaNetworkWired, FaShieldAlt, FaCog } from 'react-icons/fa';
import './Sidebar.css';

const Sidebar = () => {
  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <h2>Navigation</h2>
      </div>
      
      <nav className="sidebar-nav">
        <ul>
          <li>
            <NavLink to="/" className={({ isActive }) => isActive ? 'active' : ''}>
              <FaHome className="nav-icon" />
              <span>Dashboard</span>
            </NavLink>
          </li>
          <li>
            <NavLink to="/devices" className={({ isActive }) => isActive ? 'active' : ''}>
              <FaNetworkWired className="nav-icon" />
              <span>Devices</span>
            </NavLink>
          </li>
          <li>
            <NavLink to="/threats" className={({ isActive }) => isActive ? 'active' : ''}>
              <FaShieldAlt className="nav-icon" />
              <span>Threats</span>
            </NavLink>
          </li>
          <li>
            <NavLink to="/settings" className={({ isActive }) => isActive ? 'active' : ''}>
              <FaCog className="nav-icon" />
              <span>Settings</span>
            </NavLink>
          </li>
        </ul>
      </nav>
      
      <div className="sidebar-footer">
        <div className="system-status">
          <div className="status-indicator online"></div>
          <span>System Online</span>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;
