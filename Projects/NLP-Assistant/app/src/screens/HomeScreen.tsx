import React, { useState, useEffect } from 'react';
import { View, StyleSheet, FlatList, TouchableOpacity } from 'react-native';
import { Text, FAB, ActivityIndicator, Appbar, Card, IconButton } from 'react-native-paper';
import { useNavigation } from '@react-navigation/native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { StatusBar } from 'expo-status-bar';
import { MaterialIcons, MaterialCommunityIcons } from '@expo/vector-icons';

import { useAssistant } from '../contexts/AssistantContext';

type ConversationItemProps = {
  text: string;
  type: 'user' | 'assistant';
  timestamp: Date;
};

const ConversationItem: React.FC<ConversationItemProps> = ({ text, type, timestamp }) => {
  const isUser = type === 'user';
  
  return (
    <View style={[styles.messageContainer, isUser ? styles.userMessage : styles.assistantMessage]}>
      <View style={styles.messageContent}>
        {!isUser && (
          <View style={styles.assistantIcon}>
            <MaterialCommunityIcons name="robot" size={20} color="#6200ee" />
          </View>
        )}
        <View style={[styles.messageBubble, isUser ? styles.userBubble : styles.assistantBubble]}>
          <Text style={styles.messageText}>{text}</Text>
        </View>
        {isUser && (
          <View style={styles.userIcon}>
            <MaterialIcons name="person" size={20} color="#6200ee" />
          </View>
        )}
      </View>
      <Text style={styles.timestamp}>
        {timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
      </Text>
    </View>
  );
};

const HomeScreen: React.FC = () => {
  const navigation = useNavigation();
  const {
    isConnected,
    connect,
    isListening,
    startListening,
    stopListening,
    sendTextCommand,
    conversationHistory,
    clearConversation,
  } = useAssistant();
  
  const [textInput, setTextInput] = useState('');
  const [connecting, setConnecting] = useState(false);
  
  // Auto-connect on component mount if we have a server address
  useEffect(() => {
    const autoConnect = async () => {
      if (!isConnected) {
        setConnecting(true);
        await connect();
        setConnecting(false);
      }
    };
    
    autoConnect();
  }, []);
  
  // Handle microphone button press
  const handleMicPress = async () => {
    if (isListening) {
      await stopListening();
    } else {
      await startListening();
    }
  };
  
  // Handle text input submission
  const handleSendText = async () => {
    if (textInput.trim()) {
      await sendTextCommand(textInput.trim());
      setTextInput('');
    }
  };
  
  // Render empty conversation state
  const renderEmptyConversation = () => (
    <View style={styles.emptyContainer}>
      <MaterialCommunityIcons name="robot" size={80} color="#d0d0d0" />
      <Text style={styles.emptyTitle}>No Conversation Yet</Text>
      <Text style={styles.emptySubtitle}>
        Tap the microphone button below and start speaking to the assistant.
      </Text>
    </View>
  );
  
  return (
    <SafeAreaView style={styles.container}>
      <Appbar.Header>
        <Appbar.Content title="NLP Assistant" />
        {isConnected ? (
          <Appbar.Action 
            icon="wifi" 
            color="#4CAF50" 
            onPress={() => navigation.navigate('Connection' as never)} 
          />
        ) : (
          <Appbar.Action 
            icon="wifi-off" 
            color="#F44336" 
            onPress={() => navigation.navigate('Connection' as never)} 
          />
        )}
        <Appbar.Action 
          icon="cog" 
          onPress={() => navigation.navigate('Settings' as never)} 
        />
      </Appbar.Header>
      
      <View style={styles.content}>
        {connecting ? (
          <View style={styles.loadingContainer}>
            <ActivityIndicator size="large" color="#6200ee" />
            <Text style={styles.loadingText}>Connecting to assistant...</Text>
          </View>
        ) : !isConnected ? (
          <Card style={styles.connectionCard}>
            <Card.Content>
              <Text style={styles.connectionTitle}>Not Connected</Text>
              <Text style={styles.connectionText}>
                You are not connected to the assistant server. Please go to the connection screen to set up your connection.
              </Text>
            </Card.Content>
            <Card.Actions>
              <TouchableOpacity 
                style={styles.connectionButton}
                onPress={() => navigation.navigate('Connection' as never)}
              >
                <Text style={styles.connectionButtonText}>Connect</Text>
              </TouchableOpacity>
            </Card.Actions>
          </Card>
        ) : (
          <>
            <FlatList
              data={conversationHistory}
              keyExtractor={(item) => item.id}
              renderItem={({ item }) => (
                <ConversationItem
                  text={item.text}
                  type={item.type}
                  timestamp={item.timestamp}
                />
              )}
              contentContainerStyle={styles.conversationContainer}
              ListEmptyComponent={renderEmptyConversation}
              inverted={conversationHistory.length > 0}
            />
            
            {conversationHistory.length > 0 && (
              <IconButton
                icon="delete"
                size={24}
                style={styles.clearButton}
                onPress={clearConversation}
              />
            )}
          </>
        )}
      </View>
      
      <FAB
        style={[
          styles.fab,
          isListening ? styles.listeningFab : null,
          !isConnected ? styles.disabledFab : null
        ]}
        icon={isListening ? "microphone-off" : "microphone"}
        onPress={handleMicPress}
        disabled={!isConnected}
      />
      
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
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    marginTop: 16,
    fontSize: 16,
    color: '#666',
  },
  connectionCard: {
    marginTop: 20,
    elevation: 4,
  },
  connectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 8,
  },
  connectionText: {
    fontSize: 14,
    color: '#666',
    marginBottom: 8,
  },
  connectionButton: {
    backgroundColor: '#6200ee',
    paddingVertical: 8,
    paddingHorizontal: 16,
    borderRadius: 4,
  },
  connectionButtonText: {
    color: 'white',
    fontWeight: 'bold',
  },
  conversationContainer: {
    flexGrow: 1,
    paddingBottom: 80,
  },
  messageContainer: {
    marginVertical: 8,
    maxWidth: '80%',
  },
  userMessage: {
    alignSelf: 'flex-end',
  },
  assistantMessage: {
    alignSelf: 'flex-start',
  },
  messageContent: {
    flexDirection: 'row',
    alignItems: 'flex-end',
  },
  messageBubble: {
    borderRadius: 20,
    paddingHorizontal: 16,
    paddingVertical: 10,
    marginHorizontal: 8,
  },
  userBubble: {
    backgroundColor: '#e3f2fd',
  },
  assistantBubble: {
    backgroundColor: '#f0e4ff',
  },
  messageText: {
    fontSize: 16,
  },
  userIcon: {
    width: 30,
    height: 30,
    borderRadius: 15,
    backgroundColor: '#e3f2fd',
    justifyContent: 'center',
    alignItems: 'center',
  },
  assistantIcon: {
    width: 30,
    height: 30,
    borderRadius: 15,
    backgroundColor: '#f0e4ff',
    justifyContent: 'center',
    alignItems: 'center',
  },
  timestamp: {
    fontSize: 12,
    color: '#999',
    marginTop: 4,
    alignSelf: 'flex-end',
  },
  fab: {
    position: 'absolute',
    margin: 16,
    right: 0,
    bottom: 0,
    backgroundColor: '#6200ee',
  },
  listeningFab: {
    backgroundColor: '#f44336',
  },
  disabledFab: {
    backgroundColor: '#cccccc',
  },
  clearButton: {
    position: 'absolute',
    top: 0,
    right: 0,
  },
  emptyContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  emptyTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    marginTop: 20,
    marginBottom: 10,
    color: '#666',
  },
  emptySubtitle: {
    fontSize: 16,
    textAlign: 'center',
    color: '#999',
  },
});

export default HomeScreen;
