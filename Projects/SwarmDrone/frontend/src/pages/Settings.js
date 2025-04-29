import React, { useState, useContext } from 'react';
import { FaSave, FaServer, FaDrone, FaNetworkWired } from 'react-icons/fa';
import WebSocketContext from '../contexts/WebSocketContext';
import './Settings.css';

const Settings = () => {
  const { connected } = useContext(WebSocketContext);
  
  const [settings, setSettings] = useState({
    serverAddress: 'ws://localhost:9090',
    connectionTimeout: 5000,
    updateInterval: 100,
    droneCount: 3,
    commRange: 10.0,
    safeDistance: 2.0,
    visualizationQuality: 'high'
  });
  
  const [saved, setSaved] = useState(false);
  
  const handleChange = (e) => {
    const { name, value, type } = e.target;
    setSettings({
      ...settings,
      [name]: type === 'number' ? parseFloat(value) : value
    });
    
    // Reset saved status when settings change
    if (saved) setSaved(false);
  };
  
  const handleSubmit = (e) => {
    e.preventDefault();
    
    // In a real app, this would save settings to local storage or backend
    localStorage.setItem('swarmDroneSettings', JSON.stringify(settings));
    
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
          <h2><FaServer /> Connection Settings</h2>
          
          <div className="form-group">
            <label htmlFor="serverAddress">WebSocket Server Address</label>
            <input
              type="text"
              id="serverAddress"
              name="serverAddress"
              value={settings.serverAddress}
              onChange={handleChange}
              placeholder="ws://localhost:9090"
            />
            <p className="form-help">
              The address of the WebSocket server that bridges to the ROS system.
              Changes will take effect after page reload.
            </p>
          </div>
          
          <div className="form-group">
            <label htmlFor="connectionTimeout">Connection Timeout (ms)</label>
            <input
              type="number"
              id="connectionTimeout"
              name="connectionTimeout"
              value={settings.connectionTimeout}
              onChange={handleChange}
              min="1000"
              max="30000"
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="updateInterval">UI Update Interval (ms)</label>
            <input
              type="number"
              id="updateInterval"
              name="updateInterval"
              value={settings.updateInterval}
              onChange={handleChange}
              min="50"
              max="1000"
            />
            <p className="form-help">
              How frequently the UI updates with new data from the server.
              Lower values provide smoother visualization but may impact performance.
            </p>
          </div>
        </div>
        
        <div className="settings-section">
          <h2><FaDrone /> Drone Configuration</h2>
          
          <div className="form-group">
            <label htmlFor="droneCount">Number of Drones</label>
            <input
              type="number"
              id="droneCount"
              name="droneCount"
              value={settings.droneCount}
              onChange={handleChange}
              min="1"
              max="10"
            />
            <p className="form-help">
              The number of drones in the swarm.
              Changes will take effect after system restart.
            </p>
          </div>
          
          <div className="form-group">
            <label htmlFor="commRange">Communication Range (meters)</label>
            <input
              type="number"
              id="commRange"
              name="commRange"
              value={settings.commRange}
              onChange={handleChange}
              min="1"
              max="50"
              step="0.5"
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="safeDistance">Safe Distance (meters)</label>
            <input
              type="number"
              id="safeDistance"
              name="safeDistance"
              value={settings.safeDistance}
              onChange={handleChange}
              min="0.5"
              max="5"
              step="0.1"
            />
            <p className="form-help">
              Minimum safe distance between drones for collision avoidance.
            </p>
          </div>
        </div>
        
        <div className="settings-section">
          <h2><FaNetworkWired /> Visualization Settings</h2>
          
          <div className="form-group">
            <label htmlFor="visualizationQuality">Visualization Quality</label>
            <select
              id="visualizationQuality"
              name="visualizationQuality"
              value={settings.visualizationQuality}
              onChange={handleChange}
            >
              <option value="low">Low (Better Performance)</option>
              <option value="medium">Medium</option>
              <option value="high">High (Better Quality)</option>
            </select>
          </div>
        </div>
        
        <div className="form-actions">
          <button type="submit" className="btn-save">
            <FaSave /> Save Settings
          </button>
        </div>
      </form>
      
      <div className="settings-info">
        <h2>System Information</h2>
        
        <div className="info-item">
          <span className="info-label">Connection Status:</span>
          <span className={`info-value ${connected ? 'connected' : 'disconnected'}`}>
            {connected ? 'Connected' : 'Disconnected'}
          </span>
        </div>
        
        <div className="info-item">
          <span className="info-label">Frontend Version:</span>
          <span className="info-value">0.1.0</span>
        </div>
        
        <div className="info-item">
          <span className="info-label">Backend Version:</span>
          <span className="info-value">{connected ? '0.1.0' : 'Unknown'}</span>
        </div>
      </div>
    </div>
  );
};

export default Settings;
