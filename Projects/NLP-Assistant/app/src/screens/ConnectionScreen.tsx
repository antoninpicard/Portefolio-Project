import React, { useState, useEffect } from 'react';
import { View, StyleSheet, TouchableOpacity, Alert } from 'react-native';
import { Text, TextInput, Button, Card, ActivityIndicator } from 'react-native-paper';
import { useNavigation } from '@react-navigation/native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { StatusBar } from 'expo-status-bar';
import { MaterialCommunityIcons } from '@expo/vector-icons';

import { useAssistant } from '../contexts/AssistantContext';

const ConnectionScreen: React.FC = () => {
  const navigation = useNavigation();
  const { serverAddress, setServerAddress, isConnected, connect, disconnect } = useAssistant();
  
  const [address, setAddress] = useState(serverAddress || 'ws://');
  const [connecting, setConnecting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  // Handle connection
  const handleConnect = async () => {
    if (!address) {
      setError('Please enter a server address');
      return;
    }
    
    if (!address.startsWith('ws://') && !address.startsWith('wss://')) {
      setError('Address must start with ws:// or wss://');
      return;
    }
    
    setError(null);
    setConnecting(true);
    
    try {
      // Update server address in context
      setServerAddress(address);
      
      // Try to connect
      const success = await connect();
      
      if (success) {
        // Navigate to home screen on successful connection
        navigation.navigate('Home' as never);
      } else {
        setError('Failed to connect to server');
      }
    } catch (error) {
      console.error('Connection error:', error);
      setError('An error occurred while connecting');
    } finally {
      setConnecting(false);
    }
  };
  
  // Handle disconnection
  const handleDisconnect = () => {
    disconnect();
    Alert.alert('Disconnected', 'You have been disconnected from the server');
  };
  
  // Handle continue without connecting
  const handleContinueWithoutConnecting = () => {
    navigation.navigate('Home' as never);
  };
  
  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.content}>
        <View style={styles.header}>
          <MaterialCommunityIcons name="robot" size={80} color="#6200ee" />
          <Text style={styles.title}>Connect to Assistant</Text>
          <Text style={styles.subtitle}>
            Enter the WebSocket address of your NLP Assistant server
          </Text>
        </View>
        
        <Card style={styles.card}>
          <Card.Content>
            <TextInput
              label="Server Address"
              value={address}
              onChangeText={setAddress}
              mode="outlined"
              autoCapitalize="none"
              autoCorrect={false}
              disabled={connecting || isConnected}
              style={styles.input}
              placeholder="ws://192.168.1.100:8765"
            />
            
            {error && <Text style={styles.errorText}>{error}</Text>}
            
            <View style={styles.buttonContainer}>
              {connecting ? (
                <ActivityIndicator size="large" color="#6200ee" style={styles.loader} />
              ) : isConnected ? (
                <>
                  <Text style={styles.connectedText}>
                    Connected to {serverAddress}
                  </Text>
                  <Button
                    mode="contained"
                    onPress={handleDisconnect}
                    style={styles.button}
                    color="#F44336"
                  >
                    Disconnect
                  </Button>
                  <Button
                    mode="contained"
                    onPress={() => navigation.navigate('Home' as never)}
                    style={styles.button}
                  >
                    Continue
                  </Button>
                </>
              ) : (
                <>
                  <Button
                    mode="contained"
                    onPress={handleConnect}
                    style={styles.button}
                  >
                    Connect
                  </Button>
                  <TouchableOpacity
                    onPress={handleContinueWithoutConnecting}
                    style={styles.skipButton}
                  >
                    <Text style={styles.skipButtonText}>
                      Continue without connecting
                    </Text>
                  </TouchableOpacity>
                </>
              )}
            </View>
          </Card.Content>
        </Card>
        
        <View style={styles.helpContainer}>
          <Text style={styles.helpTitle}>Need Help?</Text>
          <Text style={styles.helpText}>
            The NLP Assistant server should be running on your local network.
            Make sure the server is running and that your device is connected
            to the same network.
          </Text>
          <Text style={styles.helpText}>
            The default address format is:
            {'\n'}ws://[SERVER_IP]:[PORT]
          </Text>
        </View>
      </View>
      
      <StatusBar style="auto" />
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f6f6f6',
  },
  content: {
    flex: 1,
    padding: 16,
    justifyContent: 'center',
  },
  header: {
    alignItems: 'center',
    marginBottom: 24,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginTop: 16,
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    color: '#666',
    textAlign: 'center',
    marginBottom: 16,
  },
  card: {
    marginBottom: 24,
    elevation: 4,
  },
  input: {
    marginBottom: 16,
  },
  errorText: {
    color: '#F44336',
    marginBottom: 16,
  },
  buttonContainer: {
    alignItems: 'center',
  },
  button: {
    width: '100%',
    marginBottom: 12,
  },
  loader: {
    marginVertical: 16,
  },
  connectedText: {
    color: '#4CAF50',
    fontWeight: 'bold',
    marginBottom: 16,
  },
  skipButton: {
    padding: 8,
  },
  skipButtonText: {
    color: '#666',
    textDecorationLine: 'underline',
  },
  helpContainer: {
    padding: 16,
    backgroundColor: '#e3f2fd',
    borderRadius: 8,
  },
  helpTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 8,
  },
  helpText: {
    fontSize: 14,
    color: '#333',
    marginBottom: 8,
  },
});

export default ConnectionScreen;
