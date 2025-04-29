import React, { createContext, useState, useEffect, useContext } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Audio } from 'expo-av';

// Define the context types
type AssistantContextType = {
  serverAddress: string;
  setServerAddress: (address: string) => void;
  isConnected: boolean;
  connect: () => Promise<boolean>;
  disconnect: () => void;
  isListening: boolean;
  startListening: () => Promise<void>;
  stopListening: () => Promise<void>;
  sendTextCommand: (text: string) => Promise<void>;
  lastResponse: string | null;
  lastRecognizedText: string | null;
  lastIntent: string | null;
  conversationHistory: ConversationItem[];
  clearConversation: () => void;
};

type ConversationItem = {
  id: string;
  type: 'user' | 'assistant';
  text: string;
  timestamp: Date;
};

// Create the context with default values
const AssistantContext = createContext<AssistantContextType>({
  serverAddress: '',
  setServerAddress: () => {},
  isConnected: false,
  connect: async () => false,
  disconnect: () => {},
  isListening: false,
  startListening: async () => {},
  stopListening: async () => {},
  sendTextCommand: async () => {},
  lastResponse: null,
  lastRecognizedText: null,
  lastIntent: null,
  conversationHistory: [],
  clearConversation: () => {},
});

// Provider component
export const AssistantProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [serverAddress, setServerAddress] = useState<string>('');
  const [socket, setSocket] = useState<WebSocket | null>(null);
  const [isConnected, setIsConnected] = useState<boolean>(false);
  const [isListening, setIsListening] = useState<boolean>(false);
  const [lastResponse, setLastResponse] = useState<string | null>(null);
  const [lastRecognizedText, setLastRecognizedText] = useState<string | null>(null);
  const [lastIntent, setLastIntent] = useState<string | null>(null);
  const [conversationHistory, setConversationHistory] = useState<ConversationItem[]>([]);
  const [recording, setRecording] = useState<Audio.Recording | null>(null);

  // Load server address from storage on component mount
  useEffect(() => {
    const loadServerAddress = async () => {
      try {
        const savedAddress = await AsyncStorage.getItem('@server_address');
        if (savedAddress) {
          setServerAddress(savedAddress);
        }
      } catch (error) {
        console.error('Error loading server address:', error);
      }
    };

    loadServerAddress();
  }, []);

  // Save server address when it changes
  useEffect(() => {
    const saveServerAddress = async () => {
      try {
        if (serverAddress) {
          await AsyncStorage.setItem('@server_address', serverAddress);
        }
      } catch (error) {
        console.error('Error saving server address:', error);
      }
    };

    if (serverAddress) {
      saveServerAddress();
    }
  }, [serverAddress]);

  // Connect to the WebSocket server
  const connect = async (): Promise<boolean> => {
    if (!serverAddress) {
      return false;
    }

    try {
      // Close existing connection if any
      if (socket) {
        socket.close();
      }

      // Create new WebSocket connection
      const newSocket = new WebSocket(serverAddress);

      // Set up event handlers
      newSocket.onopen = () => {
        console.log('Connected to server');
        setIsConnected(true);
      };

      newSocket.onclose = () => {
        console.log('Disconnected from server');
        setIsConnected(false);
        setSocket(null);
      };

      newSocket.onerror = (error) => {
        console.error('WebSocket error:', error);
        setIsConnected(false);
      };

      newSocket.onmessage = (event) => {
        handleServerMessage(event.data);
      };

      setSocket(newSocket);
      return true;
    } catch (error) {
      console.error('Error connecting to server:', error);
      return false;
    }
  };

  // Disconnect from the WebSocket server
  const disconnect = () => {
    if (socket) {
      socket.close();
      setSocket(null);
      setIsConnected(false);
    }
  };

  // Handle messages from the server
  const handleServerMessage = (data: string) => {
    try {
      const message = JSON.parse(data);

      switch (message.type) {
        case 'welcome':
          console.log('Received welcome message:', message.message);
          break;

        case 'recognition':
          setLastRecognizedText(message.text);
          addToConversation('user', message.text);
          break;

        case 'intent':
          setLastIntent(message.intent);
          break;

        case 'response':
          setLastResponse(message.text);
          addToConversation('assistant', message.text);
          
          // Play audio response if available
          if (message.audio) {
            playAudioResponse(message.audio);
          }
          break;

        case 'error':
          console.error('Server error:', message.message);
          break;

        default:
          console.log('Received unknown message type:', message.type);
      }
    } catch (error) {
      console.error('Error parsing server message:', error);
    }
  };

  // Add item to conversation history
  const addToConversation = (type: 'user' | 'assistant', text: string) => {
    const newItem: ConversationItem = {
      id: Date.now().toString(),
      type,
      text,
      timestamp: new Date(),
    };

    setConversationHistory((prev) => [...prev, newItem]);
  };

  // Clear conversation history
  const clearConversation = () => {
    setConversationHistory([]);
    setLastResponse(null);
    setLastRecognizedText(null);
    setLastIntent(null);
  };

  // Play audio response
  const playAudioResponse = async (audioData: string) => {
    try {
      // In a real implementation, this would play the audio data
      console.log('Would play audio response');
    } catch (error) {
      console.error('Error playing audio response:', error);
    }
  };

  // Start recording audio
  const startListening = async () => {
    try {
      if (isListening) {
        return;
      }

      console.log('Requesting permissions');
      await Audio.requestPermissionsAsync();
      await Audio.setAudioModeAsync({
        allowsRecordingIOS: true,
        playsInSilentModeIOS: true,
      });

      console.log('Starting recording');
      const { recording } = await Audio.Recording.createAsync(
        Audio.RECORDING_OPTIONS_PRESET_HIGH_QUALITY
      );
      setRecording(recording);
      setIsListening(true);
    } catch (error) {
      console.error('Failed to start recording', error);
    }
  };

  // Stop recording and send audio to server
  const stopListening = async () => {
    try {
      if (!recording) {
        return;
      }

      console.log('Stopping recording');
      setIsListening(false);
      await recording.stopAndUnloadAsync();

      const uri = recording.getURI();
      if (!uri) {
        throw new Error('No recording URI available');
      }

      console.log('Recording stopped and stored at', uri);
      setRecording(null);

      // In a real implementation, this would send the audio to the server
      // For this demo, we'll simulate a recognized command
      if (socket && isConnected) {
        // Simulate sending audio and getting a response
        const simulatedCommands = [
          'turn on the lights',
          'what\'s the weather today',
          'set a timer for five minutes',
          'add milk to my shopping list',
          'play some music'
        ];
        
        const randomCommand = simulatedCommands[Math.floor(Math.random() * simulatedCommands.length)];
        
        // Add the command to conversation history
        addToConversation('user', randomCommand);
        setLastRecognizedText(randomCommand);
        
        // Send the command to the server
        await sendTextCommand(randomCommand);
      }
    } catch (error) {
      console.error('Failed to stop recording', error);
    }
  };

  // Send text command to server
  const sendTextCommand = async (text: string) => {
    if (!socket || !isConnected) {
      console.error('Cannot send command: not connected to server');
      return;
    }

    try {
      // Add command to conversation if not already added
      if (lastRecognizedText !== text) {
        addToConversation('user', text);
        setLastRecognizedText(text);
      }

      // Send command to server
      socket.send(JSON.stringify({
        type: 'text',
        text: text
      }));
    } catch (error) {
      console.error('Error sending text command:', error);
    }
  };

  // Context value
  const value: AssistantContextType = {
    serverAddress,
    setServerAddress,
    isConnected,
    connect,
    disconnect,
    isListening,
    startListening,
    stopListening,
    sendTextCommand,
    lastResponse,
    lastRecognizedText,
    lastIntent,
    conversationHistory,
    clearConversation,
  };

  return (
    <AssistantContext.Provider value={value}>
      {children}
    </AssistantContext.Provider>
  );
};

// Custom hook to use the assistant context
export const useAssistant = () => useContext(AssistantContext);

export default AssistantContext;
