import React, { useContext } from 'react';
import { FaDrone, FaMapMarkedAlt, FaCheckCircle, FaExclamationTriangle } from 'react-icons/fa';
import WebSocketContext from '../contexts/WebSocketContext';
import './Dashboard.css';

const Dashboard = () => {
  const { connected, droneData } = useContext(WebSocketContext);
  
  // Calculate mission statistics
  const totalDrones = droneData.numDrones;
  const activeDrones = droneData.dronePositions ? droneData.dronePositions.length : 0;
  const completionPercentage = droneData.explorationStatus ? 
    Math.round((droneData.explorationStatus.filter(status => status).length / totalDrones) * 100) : 0;
  
  return (
    <div className="dashboard">
      <h1>Mission Dashboard</h1>
      
      <div className="connection-banner">
        <div className={`connection-indicator ${connected ? 'connected' : 'disconnected'}`}></div>
        <span>{connected ? 'Connected to Swarm Control System' : 'Disconnected from Swarm Control System'}</span>
      </div>
      
      <div className="dashboard-grid">
        <div className="card">
          <div className="card-header">
            <h2 className="card-title">Drone Fleet</h2>
            <FaDrone className="card-icon" />
          </div>
          <div className="card-content">
            <div className="card-value">{activeDrones} / {totalDrones}</div>
          </div>
          <div className="card-footer">
            Active drones in the swarm
          </div>
        </div>
        
        <div className="card">
          <div className="card-header">
            <h2 className="card-title">Mission Progress</h2>
            <FaMapMarkedAlt className="card-icon" />
          </div>
          <div className="card-content">
            <div className="card-value">{completionPercentage}%</div>
            <div className="progress-bar">
              <div 
                className="progress-fill" 
                style={{ width: `${completionPercentage}%` }}
              ></div>
            </div>
          </div>
          <div className="card-footer">
            Overall mission completion
          </div>
        </div>
        
        <div className="card">
          <div className="card-header">
            <h2 className="card-title">System Status</h2>
            {connected ? 
              <FaCheckCircle className="card-icon status-ok" /> : 
              <FaExclamationTriangle className="card-icon status-warning" />
            }
          </div>
          <div className="card-content">
            <div className="status-list">
              <div className="status-item">
                <span className="status-label">Communication:</span>
                <span className={`status ${connected ? 'status-online' : 'status-offline'}`}>
                  {connected ? 'Online' : 'Offline'}
                </span>
              </div>
              <div className="status-item">
                <span className="status-label">Swarm AI:</span>
                <span className="status status-online">Active</span>
              </div>
              <div className="status-item">
                <span className="status-label">Mapping:</span>
                <span className="status status-online">Processing</span>
              </div>
            </div>
          </div>
          <div className="card-footer">
            Real-time system status
          </div>
        </div>
      </div>
      
      <div className="drone-list-container">
        <h2>Drone Fleet Status</h2>
        
        <div className="drone-list">
          {droneData.dronePositions && droneData.dronePositions.map((position, index) => (
            <div key={index} className="drone-item">
              <div className="drone-icon">
                <FaDrone />
              </div>
              <div className="drone-info">
                <h3>Drone {index + 1}</h3>
                <div className="drone-position">
                  Position: ({position[0].toFixed(2)}, {position[1].toFixed(2)}, {position[2].toFixed(2)})
                </div>
                <div className="drone-status">
                  <span className={`status ${droneData.explorationStatus && droneData.explorationStatus[index] ? 'status-online' : 'status-warning'}`}>
                    {droneData.explorationStatus && droneData.explorationStatus[index] ? 'Mission Complete' : 'In Progress'}
                  </span>
                </div>
              </div>
            </div>
          ))}
          
          {(!droneData.dronePositions || droneData.dronePositions.length === 0) && (
            <div className="no-drones">
              No active drones detected. Please check connection to the swarm controller.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
