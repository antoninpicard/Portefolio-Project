import { createContext } from 'react';

// Create WebSocket context with default values
const WebSocketContext = createContext({
  connected: false,
  droneData: {
    numDrones: 0,
    dronePositions: [],
    droneOrientations: [],
    dronePaths: [],
    explorationStatus: []
  },
  sendCommand: () => {}
});

export default WebSocketContext;
