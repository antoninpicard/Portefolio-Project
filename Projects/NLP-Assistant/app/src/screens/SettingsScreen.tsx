import React, { useState } from 'react';
import { View, StyleSheet, ScrollView, Switch, Alert } from 'react-native';
import { Text, Divider, List, Button, Dialog, Portal, RadioButton } from 'react-native-paper';
import { useNavigation } from '@react-navigation/native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { StatusBar } from 'expo-status-bar';
import AsyncStorage from '@react-native-async-storage/async-storage';

import { useAssistant } from '../contexts/AssistantContext';

const SettingsScreen: React.FC = () => {
  const navigation = useNavigation();
  const { serverAddress, clearConversation } = useAssistant();
  
  // Settings state
  const [voiceEnabled, setVoiceEnabled] = useState(true);
  const [autoListenEnabled, setAutoListenEnabled] = useState(false);
  const [darkModeEnabled, setDarkModeEnabled] = useState(false);
  const [voiceType, setVoiceType] = useState('default');
  
  // Dialog state
  const [voiceDialogVisible, setVoiceDialogVisible] = useState(false);
  
  // Handle clear conversation
  const handleClearConversation = () => {
    Alert.alert(
      'Clear Conversation',
      'Are you sure you want to clear the entire conversation history?',
      [
        {
          text: 'Cancel',
          style: 'cancel',
        },
        {
          text: 'Clear',
          onPress: () => {
            clearConversation();
            Alert.alert('Conversation Cleared', 'Your conversation history has been cleared.');
          },
          style: 'destructive',
        },
      ]
    );
  };
  
  // Handle reset settings
  const handleResetSettings = () => {
    Alert.alert(
      'Reset Settings',
      'Are you sure you want to reset all settings to their default values?',
      [
        {
          text: 'Cancel',
          style: 'cancel',
        },
        {
          text: 'Reset',
          onPress: () => {
            setVoiceEnabled(true);
            setAutoListenEnabled(false);
            setDarkModeEnabled(false);
            setVoiceType('default');
            Alert.alert('Settings Reset', 'All settings have been reset to their default values.');
          },
        },
      ]
    );
  };
  
  return (
    <SafeAreaView style={styles.container}>
      <ScrollView style={styles.content}>
        <List.Section>
          <List.Subheader>Connection</List.Subheader>
          <List.Item
            title="Server Address"
            description={serverAddress || 'Not connected'}
            left={props => <List.Icon {...props} icon="server" />}
            onPress={() => navigation.navigate('Connection' as never)}
          />
        </List.Section>
        
        <Divider />
        
        <List.Section>
          <List.Subheader>Voice & Speech</List.Subheader>
          <List.Item
            title="Voice Responses"
            description="Enable spoken responses from the assistant"
            left={props => <List.Icon {...props} icon="volume-high" />}
            right={props => (
              <Switch
                value={voiceEnabled}
                onValueChange={setVoiceEnabled}
              />
            )}
          />
          
          <List.Item
            title="Voice Type"
            description={voiceType === 'default' ? 'Default Voice' : 
                       voiceType === 'male' ? 'Male Voice' : 
                       voiceType === 'female' ? 'Female Voice' : 'Custom Voice'}
            left={props => <List.Icon {...props} icon="account-voice" />}
            onPress={() => setVoiceDialogVisible(true)}
            disabled={!voiceEnabled}
          />
          
          <List.Item
            title="Auto-Listen Mode"
            description="Automatically start listening after assistant response"
            left={props => <List.Icon {...props} icon="microphone" />}
            right={props => (
              <Switch
                value={autoListenEnabled}
                onValueChange={setAutoListenEnabled}
              />
            )}
          />
        </List.Section>
        
        <Divider />
        
        <List.Section>
          <List.Subheader>Appearance</List.Subheader>
          <List.Item
            title="Dark Mode"
            description="Use dark color theme"
            left={props => <List.Icon {...props} icon="theme-light-dark" />}
            right={props => (
              <Switch
                value={darkModeEnabled}
                onValueChange={setDarkModeEnabled}
              />
            )}
          />
        </List.Section>
        
        <Divider />
        
        <List.Section>
          <List.Subheader>Data & Privacy</List.Subheader>
          <List.Item
            title="Clear Conversation History"
            description="Delete all conversation data"
            left={props => <List.Icon {...props} icon="delete" />}
            onPress={handleClearConversation}
          />
        </List.Section>
        
        <Divider />
        
        <List.Section>
          <List.Subheader>About</List.Subheader>
          <List.Item
            title="Version"
            description="1.0.0"
            left={props => <List.Icon {...props} icon="information" />}
          />
          <List.Item
            title="License"
            description="MIT"
            left={props => <List.Icon {...props} icon="license" />}
          />
        </List.Section>
        
        <View style={styles.buttonContainer}>
          <Button
            mode="outlined"
            onPress={handleResetSettings}
            style={styles.resetButton}
          >
            Reset All Settings
          </Button>
        </View>
      </ScrollView>
      
      {/* Voice Type Dialog */}
      <Portal>
        <Dialog
          visible={voiceDialogVisible}
          onDismiss={() => setVoiceDialogVisible(false)}
        >
          <Dialog.Title>Select Voice Type</Dialog.Title>
          <Dialog.Content>
            <RadioButton.Group
              onValueChange={value => setVoiceType(value)}
              value={voiceType}
            >
              <RadioButton.Item label="Default Voice" value="default" />
              <RadioButton.Item label="Male Voice" value="male" />
              <RadioButton.Item label="Female Voice" value="female" />
              <RadioButton.Item label="Custom Voice" value="custom" />
            </RadioButton.Group>
          </Dialog.Content>
          <Dialog.Actions>
            <Button onPress={() => setVoiceDialogVisible(false)}>Done</Button>
          </Dialog.Actions>
        </Dialog>
      </Portal>
      
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
  },
  buttonContainer: {
    padding: 16,
    marginBottom: 16,
  },
  resetButton: {
    borderColor: '#F44336',
    borderWidth: 1,
  },
});

export default SettingsScreen;
