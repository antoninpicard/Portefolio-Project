import React, { useState } from 'react';
import { FaSave, FaBell, FaShieldAlt, FaNetworkWired, FaEnvelope, FaMobile } from 'react-icons/fa';
import './Settings.css';

const Settings = () => {
  const [settings, setSettings] = useState({
    scanInterval: 30,
    autoBlockThreats: true,
    notifyOnNewDevice: true,
    notifyOnThreat: true,
    emailNotifications: false,
    smsNotifications: false,
    email: '',
    phone: '',
    scanDepth: 'standard'
  });
  
  const [saved, setSaved] = useState(false);
  
  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setSettings({
      ...settings,
      [name]: type === 'checkbox' ? checked : value
    });
    
    // Reset saved status when settings change
    if (saved) setSaved(false);
  };
  
  const handleSubmit = (e) => {
    e.preventDefault();
    
    // In a real app, this would save settings to the backend
    console.log('Saving settings:', settings);
    
    // Show saved confirmation
    setSaved(true);
    
    // Hide confirmation after 3 seconds
    setTimeout(() => {
      setSaved(false);
    }, 3000);
  };

  return (
    <div className="settings-page">
      <h1>Settings</h1>
      
      {saved && (
        <div className="save-confirmation">
          <FaSave /> Settings saved successfully
        </div>
      )}
      
      <form onSubmit={handleSubmit}>
        <div className="settings-section">
          <h2><FaShieldAlt /> Security Settings</h2>
          
          <div className="form-group">
            <label htmlFor="scanInterval">Network Scan Interval (minutes)</label>
            <input
              type="number"
              id="scanInterval"
              name="scanInterval"
              value={settings.scanInterval}
              onChange={handleChange}
              min="5"
              max="120"
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="scanDepth">Scan Depth</label>
            <select
              id="scanDepth"
              name="scanDepth"
              value={settings.scanDepth}
              onChange={handleChange}
            >
              <option value="quick">Quick (Low resource usage)</option>
              <option value="standard">Standard (Recommended)</option>
              <option value="deep">Deep (High resource usage)</option>
            </select>
          </div>
          
          <div className="form-group checkbox-group">
            <input
              type="checkbox"
              id="autoBlockThreats"
              name="autoBlockThreats"
              checked={settings.autoBlockThreats}
              onChange={handleChange}
            />
            <label htmlFor="autoBlockThreats">Automatically block high-severity threats</label>
          </div>
        </div>
        
        <div className="settings-section">
          <h2><FaNetworkWired /> Network Settings</h2>
          
          <div className="form-group checkbox-group">
            <input
              type="checkbox"
              id="notifyOnNewDevice"
              name="notifyOnNewDevice"
              checked={settings.notifyOnNewDevice}
              onChange={handleChange}
            />
            <label htmlFor="notifyOnNewDevice">Notify when new devices connect to network</label>
          </div>
        </div>
        
        <div className="settings-section">
          <h2><FaBell /> Notification Settings</h2>
          
          <div className="form-group checkbox-group">
            <input
              type="checkbox"
              id="notifyOnThreat"
              name="notifyOnThreat"
              checked={settings.notifyOnThreat}
              onChange={handleChange}
            />
            <label htmlFor="notifyOnThreat">Show notifications for detected threats</label>
          </div>
          
          <div className="form-group checkbox-group">
            <input
              type="checkbox"
              id="emailNotifications"
              name="emailNotifications"
              checked={settings.emailNotifications}
              onChange={handleChange}
            />
            <label htmlFor="emailNotifications"><FaEnvelope /> Email notifications</label>
          </div>
          
          {settings.emailNotifications && (
            <div className="form-group">
              <label htmlFor="email">Email Address</label>
              <input
                type="email"
                id="email"
                name="email"
                value={settings.email}
                onChange={handleChange}
                placeholder="Enter your email address"
              />
            </div>
          )}
          
          <div className="form-group checkbox-group">
            <input
              type="checkbox"
              id="smsNotifications"
              name="smsNotifications"
              checked={settings.smsNotifications}
              onChange={handleChange}
            />
            <label htmlFor="smsNotifications"><FaMobile /> SMS notifications</label>
          </div>
          
          {settings.smsNotifications && (
            <div className="form-group">
              <label htmlFor="phone">Phone Number</label>
              <input
                type="tel"
                id="phone"
                name="phone"
                value={settings.phone}
                onChange={handleChange}
                placeholder="Enter your phone number"
              />
            </div>
          )}
        </div>
        
        <div className="form-actions">
          <button type="submit" className="btn-save">
            <FaSave /> Save Settings
          </button>
        </div>
      </form>
    </div>
  );
};

export default Settings;
