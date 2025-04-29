import React, { useState, useEffect } from 'react';
import { FaExclamationTriangle, FaFilter, FaSearch, FaShieldAlt } from 'react-icons/fa';
import './Threats.css';

const Threats = () => {
  const [threats, setThreats] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [filter, setFilter] = useState('all');
  
  useEffect(() => {
    // Simulate fetching threats from API
    setTimeout(() => {
      const mockThreats = [
        {
          id: 'threat1',
          timestamp: '2025-04-28T08:15:22Z',
          deviceId: 'dev4',
          deviceName: 'Unknown Device',
          deviceIp: '192.168.1.104',
          type: 'port_scan',
          severity: 'medium',
          details: 'Multiple port scan attempts detected',
          status: 'active'
        },
        {
          id: 'threat2',
          timestamp: '2025-04-27T22:43:10Z',
          deviceId: 'dev3',
          deviceName: 'Home Office PC',
          deviceIp: '192.168.1.103',
          type: 'suspicious_connection',
          severity: 'low',
          details: 'Connection to suspicious IP address',
          status: 'active'
        },
        {
          id: 'threat3',
          timestamp: '2025-04-27T14:22:05Z',
          deviceId: 'dev7',
          deviceName: 'Guest Laptop',
          deviceIp: '192.168.1.107',
          type: 'malware_signature',
          severity: 'high',
          details: 'Potential malware signature detected in network traffic',
          status: 'resolved'
        },
        {
          id: 'threat4',
          timestamp: '2025-04-26T19:11:33Z',
          deviceId: 'dev2',
          deviceName: 'Kitchen Tablet',
          deviceIp: '192.168.1.102',
          type: 'unusual_traffic',
          severity: 'low',
          details: 'Unusual traffic pattern detected',
          status: 'resolved'
        },
        {
          id: 'threat5',
          timestamp: '2025-04-26T10:05:18Z',
          deviceId: 'dev4',
          deviceName: 'Unknown Device',
          deviceIp: '192.168.1.104',
          type: 'brute_force',
          severity: 'high',
          details: 'Multiple failed login attempts detected',
          status: 'active'
        }
      ];
      
      setThreats(mockThreats);
      setLoading(false);
    }, 1000);
  }, []);
  
  // Format date for display
  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleString();
  };
  
  // Get severity class for styling
  const getSeverityClass = (severity) => {
    switch (severity) {
      case 'high':
        return 'status-danger';
      case 'medium':
        return 'status-warning';
      case 'low':
        return 'status-safe';
      default:
        return 'status-unknown';
    }
  };
  
  // Format threat type for display
  const formatThreatType = (type) => {
    return type.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
  };
  
  // Filter and search threats
  const filteredThreats = threats.filter(threat => {
    const matchesSearch = 
      threat.deviceName.toLowerCase().includes(searchTerm.toLowerCase()) || 
      threat.deviceIp.includes(searchTerm) ||
      threat.type.toLowerCase().includes(searchTerm.toLowerCase()) ||
      threat.details.toLowerCase().includes(searchTerm.toLowerCase());
    
    if (filter === 'all') return matchesSearch;
    if (filter === 'active') return threat.status === 'active' && matchesSearch;
    if (filter === 'resolved') return threat.status === 'resolved' && matchesSearch;
    return threat.severity === filter && matchesSearch;
  });

  return (
    <div className="threats-page">
      <h1>Security Threats</h1>
      
      <div className="threats-controls">
        <div className="search-container">
          <FaSearch className="search-icon" />
          <input 
            type="text" 
            placeholder="Search threats..." 
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="search-input"
          />
        </div>
        
        <div className="filter-container">
          <FaFilter className="filter-icon" />
          <select 
            value={filter} 
            onChange={(e) => setFilter(e.target.value)}
            className="filter-select"
          >
            <option value="all">All Threats</option>
            <option value="active">Active Threats</option>
            <option value="resolved">Resolved Threats</option>
            <option value="high">High Severity</option>
            <option value="medium">Medium Severity</option>
            <option value="low">Low Severity</option>
          </select>
        </div>
      </div>
      
      {loading ? (
        <div className="loading">Loading threats...</div>
      ) : (
        <>
          <div className="threats-summary">
            <div className="summary-item">
              <div className="summary-icon high">
                <FaExclamationTriangle />
              </div>
              <div className="summary-info">
                <h3>High Severity</h3>
                <p>{threats.filter(t => t.severity === 'high' && t.status === 'active').length} active</p>
              </div>
            </div>
            
            <div className="summary-item">
              <div className="summary-icon medium">
                <FaExclamationTriangle />
              </div>
              <div className="summary-info">
                <h3>Medium Severity</h3>
                <p>{threats.filter(t => t.severity === 'medium' && t.status === 'active').length} active</p>
              </div>
            </div>
            
            <div className="summary-item">
              <div className="summary-icon low">
                <FaExclamationTriangle />
              </div>
              <div className="summary-info">
                <h3>Low Severity</h3>
                <p>{threats.filter(t => t.severity === 'low' && t.status === 'active').length} active</p>
              </div>
            </div>
            
            <div className="summary-item">
              <div className="summary-icon resolved">
                <FaShieldAlt />
              </div>
              <div className="summary-info">
                <h3>Resolved</h3>
                <p>{threats.filter(t => t.status === 'resolved').length} threats</p>
              </div>
            </div>
          </div>
          
          <div className="threats-list">
            {filteredThreats.length === 0 ? (
              <div className="no-threats">No threats match your search criteria</div>
            ) : (
              filteredThreats.map(threat => (
                <div key={threat.id} className={`threat-card ${threat.status === 'active' ? 'threat-active' : 'threat-resolved'}`}>
                  <div className="threat-header">
                    <div className="threat-type">
                      <FaExclamationTriangle className={`threat-icon ${getSeverityClass(threat.severity)}`} />
                      <h3>{formatThreatType(threat.type)}</h3>
                    </div>
                    <div className="threat-severity">
                      <span className={`status ${getSeverityClass(threat.severity)}`}>
                        {threat.severity}
                      </span>
                    </div>
                  </div>
                  
                  <div className="threat-details">
                    <p className="threat-description">{threat.details}</p>
                    <div className="threat-meta">
                      <div className="threat-device">
                        <strong>Device:</strong> {threat.deviceName} ({threat.deviceIp})
                      </div>
                      <div className="threat-time">
                        <strong>Detected:</strong> {formatDate(threat.timestamp)}
                      </div>
                    </div>
                  </div>
                  
                  <div className="threat-actions">
                    {threat.status === 'active' ? (
                      <>
                        <button className="btn-resolve">Mark as Resolved</button>
                        <button className="btn-block">Block Traffic</button>
                      </>
                    ) : (
                      <div className="resolved-status">
                        <FaShieldAlt /> Resolved
                      </div>
                    )}
                  </div>
                </div>
              ))
            )}
          </div>
        </>
      )}
    </div>
  );
};

export default Threats;
