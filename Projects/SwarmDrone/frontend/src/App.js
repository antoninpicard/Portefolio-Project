import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';

// Import components
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import Visualization from './pages/Visualization';
import MissionPlanner from './pages/MissionPlanner';
import Settings from './pages/Settings';
import WebSocketContext from './contexts/WebSocketContext';

function App() {
  const [connected, setConnected] = useState(false);
  const [socket, setSocket] = useState(null);
  const [droneData, setDroneData] = useState({
    numDrones: 0,
    dronePositions: [],
    droneOrientations: [],
    dronePaths: [],
    explorationStatus: []
  });
  
  // Connect to WebSocket server
  useEffect(() => {
    // In a real deployment, this would use the actual server address
    const serverAddress = 'ws://localhost:9090';
    const ws = new WebSocket(serverAddress);
    
    ws.onopen = () => {
      console.log('Connected to WebSocket server');
      setConnected(true);
      setSocket(ws);
      
      // Request initial state
      ws.send(JSON.stringify({ type: 'request_state' }));
    };
    
    ws.onclose = () => {
      console.log('Disconnected from WebSocket server');
      setConnected(false);
      setSocket(null);
    };
    
    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
    
    ws.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data);
        
        if (message.type === 'initial_state') {
          // Process initial state
          setDroneData({
            numDrones: message.num_drones,
            dronePositions: message.drone_positions,
            droneOrientations: message.drone_orientations,
            dronePaths: message.drone_paths,
            explorationStatus: message.exploration_status
          });
          console.log('Received initial state');
        } 
        else if (message.type === 'state_update') {
          // Process state update
          setDroneData(prevData => ({
            ...prevData,
            dronePositions: message.drone_positions,
            droneOrientations: message.drone_orientations,
            dronePaths: message.drone_paths,
            explorationStatus: message.exploration_status
          }));
        }
      } catch (error) {
        console.error('Error parsing WebSocket message:', error);
      }
    };
    
    return () => {
      if (ws) {
        ws.close();
      }
    };
  }, []);
  
  // Function to send mission control commands
  const sendCommand = (command, params) => {
    if (socket && connected) {
      const message = {
        type: 'mission_control',
        command: command,
        params: params
      };
      
      socket.send(JSON.stringify(message));
      console.log('Sent command:', command);
    } else {
      console.warn('Cannot send command: WebSocket not connected');
    }
  };
  
  // WebSocket context value
  const webSocketValue = {
    connected,
    droneData,
    sendCommand
  };

  return (
    <WebSocketContext.Provider value={webSocketValue}>
      <Router>
        <div className="app">
          <Navbar />
          <div className="container">
            <Sidebar />
            <main className="content">
              <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/visualization" element={<Visualization />} />
                <Route path="/mission" element={<MissionPlanner />} />
                <Route path="/settings" element={<Settings />} />
              </Routes>
            </main>
          </div>
        </div>
      </Router>
    </WebSocketContext.Provider>
  );
}

export default App;
