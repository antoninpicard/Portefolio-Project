import React, { useState, useEffect } from 'react';
import { FaDesktop, FaTabletAlt, FaMobileAlt, FaQuestion, FaSearch } from 'react-icons/fa';
import './Devices.css';

const Devices = () => {
  const [devices, setDevices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [filter, setFilter] = useState('all');
  
  useEffect(() => {
    // Simulate fetching devices from API
    setTimeout(() => {
      const mockDevices = [
        { id: 'dev1', name: 'Living Room TV', ip: '192.168.1.101', mac: 'AA:BB:CC:11:22:33', type: 'media', status: 'safe', lastSeen: '2025-04-28T11:30:45Z' },
        { id: 'dev2', name: 'Kitchen Tablet', ip: '192.168.1.102', mac: 'AA:BB:CC:11:22:44', type: 'tablet', status: 'safe', lastSeen: '2025-04-28T11:25:12Z' },
        { id: 'dev3', name: 'Home Office PC', ip: '192.168.1.103', mac: 'AA:BB:CC:11:22:55', type: 'computer', status: 'safe', lastSeen: '2025-04-28T11:32:08Z' },
        { id: 'dev4', name: 'Unknown Device', ip: '192.168.1.104', mac: 'AA:BB:CC:11:22:66', type: 'unknown', status: 'suspicious', lastSeen: '2025-04-28T10:15:33Z' },
        { id: 'dev5', name: 'Smartphone', ip: '192.168.1.105', mac: 'AA:BB:CC:11:22:77', type: 'mobile', status: 'safe', lastSeen: '2025-04-28T11:28:19Z' },
        { id: 'dev6', name: 'Smart Thermostat', ip: '192.168.1.106', mac: 'AA:BB:CC:11:22:88', type: 'iot', status: 'safe', lastSeen: '2025-04-28T11:05:51Z' },
        { id: 'dev7', name: 'Guest Laptop', ip: '192.168.1.107', mac: 'AA:BB:CC:11:22:99', type: 'computer', status: 'warning', lastSeen: '2025-04-28T09:45:22Z' },
      ];
      
      setDevices(mockDevices);
      setLoading(false);
    }, 1000);
  }, []);
  
  // Get device icon based on type
  const getDeviceIcon = (type) => {
    switch (type) {
      case 'computer':
        return <FaDesktop />;
      case 'tablet':
        return <FaTabletAlt />;
      case 'mobile':
        return <FaMobileAlt />;
      default:
        return <FaQuestion />;
    }
  };
  
  // Format date for display
  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleString();
  };
  
  // Filter and search devices
  const filteredDevices = devices.filter(device => {
    const matchesSearch = device.name.toLowerCase().includes(searchTerm.toLowerCase()) || 
                         device.ip.includes(searchTerm) ||
                         device.mac.toLowerCase().includes(searchTerm.toLowerCase());
    
    if (filter === 'all') return matchesSearch;
    if (filter === 'suspicious') return device.status !== 'safe' && matchesSearch;
    return device.type === filter && matchesSearch;
  });

  return (
    <div className="devices-page">
      <h1>Network Devices</h1>
      
      <div className="devices-controls">
        <div className="search-container">
          <FaSearch className="search-icon" />
          <input 
            type="text" 
            placeholder="Search devices..." 
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="search-input"
          />
        </div>
        
        <div className="filter-container">
          <label>Filter by:</label>
          <select 
            value={filter} 
            onChange={(e) => setFilter(e.target.value)}
            className="filter-select"
          >
            <option value="all">All Devices</option>
            <option value="suspicious">Suspicious Only</option>
            <option value="computer">Computers</option>
            <option value="mobile">Mobile Devices</option>
            <option value="tablet">Tablets</option>
            <option value="iot">IoT Devices</option>
            <option value="media">Media Devices</option>
          </select>
        </div>
      </div>
      
      {loading ? (
        <div className="loading">Loading devices...</div>
      ) : (
        <>
          <div className="devices-summary">
            <p>Showing {filteredDevices.length} of {devices.length} devices</p>
          </div>
          
          <div className="devices-grid">
            {filteredDevices.map(device => (
              <div key={device.id} className={`device-card ${device.status !== 'safe' ? 'device-warning' : ''}`}>
                <div className="device-icon">
                  {getDeviceIcon(device.type)}
                </div>
                <div className="device-info">
                  <h3>{device.name}</h3>
                  <p className="device-ip">{device.ip}</p>
                  <p className="device-mac">{device.mac}</p>
                  <p className="device-last-seen">Last seen: {formatDate(device.lastSeen)}</p>
                </div>
                <div className="device-status">
                  <span className={`status status-${device.status}`}>
                    {device.status}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
};

export default Devices;
