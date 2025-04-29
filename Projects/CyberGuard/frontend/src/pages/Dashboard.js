import React, { useState, useEffect } from 'react';
import { FaShieldAlt, FaNetworkWired, FaExclamationTriangle, FaChartLine } from 'react-icons/fa';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';
import './Dashboard.css';

// Register ChartJS components
ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

const Dashboard = () => {
  const [networkStatus, setNetworkStatus] = useState({
    status: 'healthy',
    devices: 12,
    threats: 2,
    lastScan: '2025-04-28T09:30:45Z'
  });
  
  const [trafficData, setTrafficData] = useState({
    labels: ['00:00', '02:00', '04:00', '06:00', '08:00', '10:00', '12:00'],
    datasets: [
      {
        label: 'Network Traffic (MB)',
        data: [65, 59, 80, 81, 56, 55, 40],
        fill: false,
        borderColor: '#3498db',
        tension: 0.1
      }
    ]
  });
  
  const [recentThreats, setRecentThreats] = useState([
    {
      id: 'threat1',
      timestamp: '2025-04-28T08:15:22Z',
      deviceName: 'Unknown Device',
      type: 'port_scan',
      severity: 'medium'
    },
    {
      id: 'threat2',
      timestamp: '2025-04-27T22:43:10Z',
      deviceName: 'Home Office PC',
      type: 'suspicious_connection',
      severity: 'low'
    }
  ]);
  
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
  
  // Chart options
  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Network Traffic (Last 24 Hours)'
      }
    }
  };
  
  // Simulate data fetching
  useEffect(() => {
    // In a real app, this would fetch data from the backend API
    const fetchData = () => {
      // Simulate API call delay
      setTimeout(() => {
        // Update traffic data with random values to simulate real-time changes
        const newTrafficData = {...trafficData};
        newTrafficData.datasets[0].data = trafficData.datasets[0].data.map(() => 
          Math.floor(Math.random() * 100) + 20
        );
        setTrafficData(newTrafficData);
        
        // Update network status
        setNetworkStatus({
          ...networkStatus,
          lastScan: new Date().toISOString()
        });
      }, 5000);
    };
    
    fetchData();
    const interval = setInterval(fetchData, 30000); // Update every 30 seconds
    
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="dashboard">
      <h1>Network Dashboard</h1>
      
      <div className="dashboard-grid">
        <div className="card">
          <div className="card-header">
            <h2 className="card-title">Network Status</h2>
            <FaShieldAlt className="card-icon" />
          </div>
          <div className="card-content">
            <div className="card-value">
              <span className={`status status-${networkStatus.status === 'healthy' ? 'safe' : 'danger'}`}>
                {networkStatus.status === 'healthy' ? 'Protected' : 'At Risk'}
              </span>
            </div>
          </div>
          <div className="card-footer">
            Last scan: {formatDate(networkStatus.lastScan)}
          </div>
        </div>
        
        <div className="card">
          <div className="card-header">
            <h2 className="card-title">Connected Devices</h2>
            <FaNetworkWired className="card-icon" />
          </div>
          <div className="card-content">
            <div className="card-value">{networkStatus.devices}</div>
          </div>
          <div className="card-footer">
            <a href="/devices">View all devices</a>
          </div>
        </div>
        
        <div className="card">
          <div className="card-header">
            <h2 className="card-title">Active Threats</h2>
            <FaExclamationTriangle className="card-icon" />
          </div>
          <div className="card-content">
            <div className="card-value">{networkStatus.threats}</div>
          </div>
          <div className="card-footer">
            <a href="/threats">View all threats</a>
          </div>
        </div>
        
        <div className="card">
          <div className="card-header">
            <h2 className="card-title">Network Traffic</h2>
            <FaChartLine className="card-icon" />
          </div>
          <div className="card-content">
            <div className="card-value">42 MB/s</div>
          </div>
          <div className="card-footer">
            Peak today: 87 MB/s
          </div>
        </div>
      </div>
      
      <div className="dashboard-row">
        <div className="card chart-card">
          <div className="card-header">
            <h2 className="card-title">Traffic Analysis</h2>
          </div>
          <div className="chart-container">
            <Line data={trafficData} options={chartOptions} />
          </div>
        </div>
      </div>
      
      <div className="dashboard-row">
        <div className="card">
          <div className="card-header">
            <h2 className="card-title">Recent Threats</h2>
          </div>
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Time</th>
                  <th>Device</th>
                  <th>Type</th>
                  <th>Severity</th>
                </tr>
              </thead>
              <tbody>
                {recentThreats.map(threat => (
                  <tr key={threat.id}>
                    <td>{formatDate(threat.timestamp)}</td>
                    <td>{threat.deviceName}</td>
                    <td>{threat.type.replace('_', ' ')}</td>
                    <td>
                      <span className={`status ${getSeverityClass(threat.severity)}`}>
                        {threat.severity}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
