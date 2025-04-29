import React from 'react';
import { Link } from 'react-router-dom';
import { FaBell, FaCog, FaSignOutAlt, FaUser } from 'react-icons/fa';
import './Navbar.css';

const Navbar = ({ onLogout }) => {
  const [notifications, setNotifications] = React.useState([
    { id: 1, message: 'New device detected on network', read: false },
    { id: 2, message: 'Suspicious activity detected', read: false }
  ]);
  const [showNotifications, setShowNotifications] = React.useState(false);
  
  const toggleNotifications = () => {
    setShowNotifications(!showNotifications);
  };
  
  const markAsRead = (id) => {
    setNotifications(notifications.map(notification => 
      notification.id === id ? { ...notification, read: true } : notification
    ));
  };
  
  const unreadCount = notifications.filter(n => !n.read).length;

  return (
    <nav className="navbar">
      <div className="navbar-logo">
        <Link to="/">
          <h1>CyberGuard</h1>
        </Link>
      </div>
      
      <div className="navbar-actions">
        <div className="notification-container">
          <button className="icon-button" onClick={toggleNotifications}>
            <FaBell />
            {unreadCount > 0 && <span className="notification-badge">{unreadCount}</span>}
          </button>
          
          {showNotifications && (
            <div className="notification-dropdown">
              <h3>Notifications</h3>
              {notifications.length === 0 ? (
                <p className="no-notifications">No notifications</p>
              ) : (
                <ul>
                  {notifications.map(notification => (
                    <li 
                      key={notification.id} 
                      className={notification.read ? 'read' : 'unread'}
                      onClick={() => markAsRead(notification.id)}
                    >
                      {notification.message}
                    </li>
                  ))}
                </ul>
              )}
            </div>
          )}
        </div>
        
        <Link to="/settings" className="icon-button">
          <FaCog />
        </Link>
        
        <div className="user-menu">
          <button className="user-button">
            <FaUser />
            <span>Admin</span>
          </button>
          
          <div className="user-dropdown">
            <ul>
              <li><Link to="/profile">Profile</Link></li>
              <li><button onClick={onLogout}><FaSignOutAlt /> Logout</button></li>
            </ul>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
