import React from 'react';
import { NavLink } from 'react-router-dom';
import { FaHome, FaCube, FaMapMarkedAlt, FaCog } from 'react-icons/fa';
import './Sidebar.css';

const Sidebar = () => {
  return (
    <aside className="sidebar">
      <nav className="sidebar-nav">
        <ul>
          <li>
            <NavLink to="/" className={({ isActive }) => isActive ? 'active' : ''}>
              <FaHome className="nav-icon" />
              <span>Dashboard</span>
            </NavLink>
          </li>
          <li>
            <NavLink to="/visualization" className={({ isActive }) => isActive ? 'active' : ''}>
              <FaCube className="nav-icon" />
              <span>3D Visualization</span>
            </NavLink>
          </li>
          <li>
            <NavLink to="/mission" className={({ isActive }) => isActive ? 'active' : ''}>
              <FaMapMarkedAlt className="nav-icon" />
              <span>Mission Planner</span>
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
        <p>SwarmDrone v0.1.0</p>
      </div>
    </aside>
  );
};

export default Sidebar;
