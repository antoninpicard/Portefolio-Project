import React, { useState, useContext, useRef } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Grid } from '@react-three/drei';
import * as THREE from 'three';
import { FaPlay, FaStop, FaSync, FaSave, FaUpload } from 'react-icons/fa';
import WebSocketContext from '../contexts/WebSocketContext';
import './MissionPlanner.css';

// 3D area selection component
const AreaSelector = ({ area, onAreaChange }) => {
  const boxRef = useRef();
  
  // Extract area dimensions
  const width = area.xMax - area.xMin;
  const height = area.yMax - area.yMin;
  const depth = area.zMax - area.zMin;
  
  // Calculate center position
  const centerX = (area.xMax + area.xMin) / 2;
  const centerY = (area.yMax + area.yMin) / 2;
  const centerZ = (area.zMax + area.zMin) / 2;
  
  return (
    <mesh 
      ref={boxRef}
      position={[centerX, centerY, centerZ]}
    >
      <boxGeometry args={[width, height, depth]} />
      <meshStandardMaterial color="#00b0ff" transparent opacity={0.2} />
      <boxHelper args={[boxRef.current, '#00b0ff']} />
    </mesh>
  );
};

// Mission Planner Component
const MissionPlanner = () => {
  const { connected, droneData, sendCommand } = useContext(WebSocketContext);
  
  // Mission area state
  const [missionArea, setMissionArea] = useState({
    xMin: -5,
    yMin: -5,
    zMin: 0,
    xMax: 5,
    yMax: 5,
    zMax: 5
  });
  
  // Mission parameters
  const [missionParams, setMissionParams] = useState({
    alpha: 1.0,  // Goal attraction
    beta: 2.0,   // Collision avoidance
    gamma: 0.5,  // Swarm cohesion
    delta: 0.1   // Velocity damping
  });
  
  // Mission status
  const [missionActive, setMissionActive] = useState(false);
  
  // Handle area input changes
  const handleAreaChange = (e) => {
    const { name, value } = e.target;
    setMissionArea({
      ...missionArea,
      [name]: parseFloat(value)
    });
  };
  
  // Handle parameter input changes
  const handleParamChange = (e) => {
    const { name, value } = e.target;
    setMissionParams({
      ...missionParams,
      [name]: parseFloat(value)
    });
  };
  
  // Start mission
  const startMission = () => {
    if (!connected) return;
    
    // Send exploration area command
    sendCommand('set_exploration_area', [
      missionArea.xMin, missionArea.yMin, missionArea.zMin,
      missionArea.xMax, missionArea.yMax, missionArea.zMax
    ]);
    
    // Send algorithm parameters
    sendCommand('update_parameters', [
      missionParams.alpha,
      missionParams.beta,
      missionParams.gamma,
      missionParams.delta
    ]);
    
    setMissionActive(true);
  };
  
  // Stop mission
  const stopMission = () => {
    if (!connected) return;
    
    // In a real implementation, this would send a stop command
    // For now, we'll just update the UI state
    setMissionActive(false);
  };
  
  // Reset mission
  const resetMission = () => {
    setMissionArea({
      xMin: -5,
      yMin: -5,
      zMin: 0,
      xMax: 5,
      yMax: 5,
      zMax: 5
    });
    
    setMissionParams({
      alpha: 1.0,
      beta: 2.0,
      gamma: 0.5,
      delta: 0.1
    });
    
    setMissionActive(false);
  };
  
  // Save mission configuration
  const saveMission = () => {
    const missionConfig = {
      area: missionArea,
      params: missionParams
    };
    
    const configJson = JSON.stringify(missionConfig, null, 2);
    const blob = new Blob([configJson], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    
    const a = document.createElement('a');
    a.href = url;
    a.download = 'mission_config.json';
    a.click();
    
    URL.revokeObjectURL(url);
  };
  
  // Load mission configuration
  const loadMission = (e) => {
    const file = e.target.files[0];
    if (!file) return;
    
    const reader = new FileReader();
    reader.onload = (event) => {
      try {
        const config = JSON.parse(event.target.result);
        if (config.area) setMissionArea(config.area);
        if (config.params) setMissionParams(config.params);
      } catch (error) {
        console.error('Error parsing mission configuration:', error);
      }
    };
    
    reader.readAsText(file);
  };

  return (
    <div className="mission-planner-page">
      <h1>Mission Planner</h1>
      
      <div className="mission-planner">
        <div className="mission-controls">
          <h2>Mission Configuration</h2>
          
          <div className="control-section">
            <h3>Exploration Area</h3>
            
            <div className="form-row">
              <div className="form-group">
                <label>X Min</label>
                <input 
                  type="number" 
                  name="xMin" 
                  value={missionArea.xMin} 
                  onChange={handleAreaChange}
                  disabled={missionActive}
                />
              </div>
              
              <div className="form-group">
                <label>X Max</label>
                <input 
                  type="number" 
                  name="xMax" 
                  value={missionArea.xMax} 
                  onChange={handleAreaChange}
                  disabled={missionActive}
                />
              </div>
            </div>
            
            <div className="form-row">
              <div className="form-group">
                <label>Y Min</label>
                <input 
                  type="number" 
                  name="yMin" 
                  value={missionArea.yMin} 
                  onChange={handleAreaChange}
                  disabled={missionActive}
                />
              </div>
              
              <div className="form-group">
                <label>Y Max</label>
                <input 
                  type="number" 
                  name="yMax" 
                  value={missionArea.yMax} 
                  onChange={handleAreaChange}
                  disabled={missionActive}
                />
              </div>
            </div>
            
            <div className="form-row">
              <div className="form-group">
                <label>Z Min</label>
                <input 
                  type="number" 
                  name="zMin" 
                  value={missionArea.zMin} 
                  onChange={handleAreaChange}
                  disabled={missionActive}
                />
              </div>
              
              <div className="form-group">
                <label>Z Max</label>
                <input 
                  type="number" 
                  name="zMax" 
                  value={missionArea.zMax} 
                  onChange={handleAreaChange}
                  disabled={missionActive}
                />
              </div>
            </div>
          </div>
          
          <div className="control-section">
            <h3>Algorithm Parameters</h3>
            
            <div className="form-group">
              <label>Goal Attraction (α)</label>
              <input 
                type="number" 
                name="alpha" 
                value={missionParams.alpha} 
                onChange={handleParamChange}
                step="0.1"
                min="0"
                max="5"
                disabled={missionActive}
              />
            </div>
            
            <div className="form-group">
              <label>Collision Avoidance (β)</label>
              <input 
                type="number" 
                name="beta" 
                value={missionParams.beta} 
                onChange={handleParamChange}
                step="0.1"
                min="0"
                max="5"
                disabled={missionActive}
              />
            </div>
            
            <div className="form-group">
              <label>Swarm Cohesion (γ)</label>
              <input 
                type="number" 
                name="gamma" 
                value={missionParams.gamma} 
                onChange={handleParamChange}
                step="0.1"
                min="0"
                max="5"
                disabled={missionActive}
              />
            </div>
            
            <div className="form-group">
              <label>Velocity Damping (δ)</label>
              <input 
                type="number" 
                name="delta" 
                value={missionParams.delta} 
                onChange={handleParamChange}
                step="0.1"
                min="0"
                max="1"
                disabled={missionActive}
              />
            </div>
          </div>
          
          <div className="mission-actions">
            {!missionActive ? (
              <button 
                className="btn-start" 
                onClick={startMission}
                disabled={!connected}
              >
                <FaPlay /> Start Mission
              </button>
            ) : (
              <button 
                className="btn-stop" 
                onClick={stopMission}
              >
                <FaStop /> Stop Mission
              </button>
            )}
            
            <button 
              className="btn-reset" 
              onClick={resetMission}
              disabled={missionActive}
            >
              <FaSync /> Reset
            </button>
            
            <div className="file-actions">
              <button 
                className="btn-save" 
                onClick={saveMission}
              >
                <FaSave /> Save Config
              </button>
              
              <div className="file-upload">
                <input 
                  type="file" 
                  id="load-mission" 
                  accept=".json" 
                  onChange={loadMission}
                  disabled={missionActive}
                />
                <label htmlFor="load-mission">
                  <FaUpload /> Load Config
                </label>
              </div>
            </div>
          </div>
        </div>
        
        <div className="mission-map">
          {connected ? (
            <Canvas camera={{ position: [10, 10, 10], fov: 60 }}>
              <ambientLight intensity={0.5} />
              <pointLight position={[10, 10, 10]} intensity={0.8} />
              
              <AreaSelector area={missionArea} />
              
              <gridHelper args={[20, 20, '#444444', '#222222']} />
              <axesHelper args={[5]} />
              
              <OrbitControls />
            </Canvas>
          ) : (
            <div className="map-disconnected">
              <p>Not connected to the swarm control system.</p>
              <p>Please check your connection and try again.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default MissionPlanner;
