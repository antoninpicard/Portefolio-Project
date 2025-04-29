import React, { useContext, useRef, useEffect } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Line, Text } from '@react-three/drei';
import * as THREE from 'three';
import WebSocketContext from '../contexts/WebSocketContext';
import './Visualization.css';

// Drone model component
const Drone = ({ position, orientation, color = '#3949ab' }) => {
  const droneRef = useRef();
  
  // Convert quaternion to Euler angles for visualization
  const quaternion = new THREE.Quaternion(
    orientation[1], orientation[2], orientation[3], orientation[0]
  );
  
  useEffect(() => {
    if (droneRef.current) {
      droneRef.current.position.set(position[0], position[1], position[2]);
      droneRef.current.quaternion.copy(quaternion);
    }
  }, [position, quaternion]);
  
  return (
    <group ref={droneRef} position={[position[0], position[1], position[2]]}>
      {/* Drone body */}
      <mesh>
        <boxGeometry args={[0.3, 0.1, 0.3]} />
        <meshStandardMaterial color={color} />
      </mesh>
      
      {/* Drone arms */}
      <mesh position={[0.2, 0, 0.2]}>
        <cylinderGeometry args={[0.05, 0.05, 0.05, 8]} />
        <meshStandardMaterial color="#e74c3c" />
      </mesh>
      
      <mesh position={[-0.2, 0, 0.2]}>
        <cylinderGeometry args={[0.05, 0.05, 0.05, 8]} />
        <meshStandardMaterial color="#e74c3c" />
      </mesh>
      
      <mesh position={[0.2, 0, -0.2]}>
        <cylinderGeometry args={[0.05, 0.05, 0.05, 8]} />
        <meshStandardMaterial color="#2ecc71" />
      </mesh>
      
      <mesh position={[-0.2, 0, -0.2]}>
        <cylinderGeometry args={[0.05, 0.05, 0.05, 8]} />
        <meshStandardMaterial color="#2ecc71" />
      </mesh>
      
      {/* Direction indicator */}
      <mesh position={[0, 0, 0.25]} rotation={[Math.PI / 2, 0, 0]}>
        <coneGeometry args={[0.05, 0.1, 8]} />
        <meshStandardMaterial color="#f39c12" />
      </mesh>
    </group>
  );
};

// Path visualization component
const DronePath = ({ path, color = '#00b0ff' }) => {
  if (!path || path.length < 2) return null;
  
  const points = path.map(point => new THREE.Vector3(point[0], point[1], point[2]));
  
  return (
    <Line
      points={points}
      color={color}
      lineWidth={1}
      dashed={false}
    />
  );
};

// Grid component for reference
const Grid = () => {
  return (
    <>
      <gridHelper args={[20, 20, '#444444', '#222222']} />
      <axesHelper args={[5]} />
    </>
  );
};

// Main visualization scene
const Scene = () => {
  const { droneData } = useContext(WebSocketContext);
  
  return (
    <>
      <ambientLight intensity={0.5} />
      <pointLight position={[10, 10, 10]} intensity={0.8} />
      
      <Grid />
      
      {/* Render drones */}
      {droneData.dronePositions && droneData.dronePositions.map((position, index) => (
        <React.Fragment key={index}>
          <Drone 
            position={position} 
            orientation={droneData.droneOrientations[index]} 
            color={droneData.explorationStatus && droneData.explorationStatus[index] ? '#2ecc71' : '#3949ab'}
          />
          
          {/* Render drone paths */}
          {droneData.dronePaths && droneData.dronePaths[index] && (
            <DronePath path={droneData.dronePaths[index]} />
          )}
          
          {/* Drone labels */}
          <Text
            position={[position[0], position[1] + 0.3, position[2]]}
            color="white"
            fontSize={0.2}
            anchorX="center"
            anchorY="middle"
          >
            Drone {index + 1}
          </Text>
        </React.Fragment>
      ))}
    </>
  );
};

const Visualization = () => {
  const { connected } = useContext(WebSocketContext);
  
  return (
    <div className="visualization-page">
      <h1>3D Swarm Visualization</h1>
      
      <div className="visualization-container">
        {connected ? (
          <Canvas camera={{ position: [5, 5, 5], fov: 60 }}>
            <Scene />
            <OrbitControls />
          </Canvas>
        ) : (
          <div className="visualization-disconnected">
            <p>Not connected to the swarm control system.</p>
            <p>Please check your connection and try again.</p>
          </div>
        )}
      </div>
      
      <div className="visualization-controls">
        <div className="control-panel">
          <h2>Visualization Controls</h2>
          <p className="control-instruction">
            <strong>Rotate:</strong> Left-click + drag
          </p>
          <p className="control-instruction">
            <strong>Pan:</strong> Right-click + drag
          </p>
          <p className="control-instruction">
            <strong>Zoom:</strong> Scroll wheel
          </p>
        </div>
        
        <div className="legend">
          <h2>Legend</h2>
          <div className="legend-item">
            <div className="legend-color" style={{ backgroundColor: '#3949ab' }}></div>
            <span>Active Drone</span>
          </div>
          <div className="legend-item">
            <div className="legend-color" style={{ backgroundColor: '#2ecc71' }}></div>
            <span>Mission Complete</span>
          </div>
          <div className="legend-item">
            <div className="legend-color" style={{ backgroundColor: '#00b0ff' }}></div>
            <span>Planned Path</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Visualization;
