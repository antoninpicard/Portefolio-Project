import React, { useState, useEffect } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { StatusBar } from 'expo-status-bar';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Provider as PaperProvider, DefaultTheme } from 'react-native-paper';

// Import screens
import HomeScreen from './screens/HomeScreen';
import SettingsScreen from './screens/SettingsScreen';
import ConnectionScreen from './screens/ConnectionScreen';

// Import contexts
import { AssistantProvider } from './contexts/AssistantContext';

// Create navigation stack
const Stack = createNativeStackNavigator();

// Custom theme
const theme = {
  ...DefaultTheme,
  colors: {
    ...DefaultTheme.colors,
    primary: '#6200ee',
    accent: '#03dac4',
    background: '#f6f6f6',
  },
};

export default function App() {
  const [isFirstLaunch, setIsFirstLaunch] = useState<boolean | null>(null);

  useEffect(() => {
    // Check if this is the first launch
    const checkFirstLaunch = async () => {
      try {
        const value = await AsyncStorage.getItem('@first_launch');
        if (value === null) {
          // First launch
          await AsyncStorage.setItem('@first_launch', 'false');
          setIsFirstLaunch(true);
        } else {
          setIsFirstLaunch(false);
        }
      } catch (error) {
        console.error('Error checking first launch:', error);
        setIsFirstLaunch(false);
      }
    };

    checkFirstLaunch();
  }, []);

  // Wait until we know if this is the first launch
  if (isFirstLaunch === null) {
    return null;
  }

  return (
    <SafeAreaProvider>
      <PaperProvider theme={theme}>
        <AssistantProvider>
          <NavigationContainer>
            <Stack.Navigator initialRouteName={isFirstLaunch ? 'Connection' : 'Home'}>
              <Stack.Screen 
                name="Home" 
                component={HomeScreen} 
                options={{ title: 'NLP Assistant' }}
              />
              <Stack.Screen 
                name="Settings" 
                component={SettingsScreen} 
                options={{ title: 'Settings' }}
              />
              <Stack.Screen 
                name="Connection" 
                component={ConnectionScreen} 
                options={{ 
                  title: 'Connect to Assistant',
                  headerBackVisible: false
                }}
              />
            </Stack.Navigator>
          </NavigationContainer>
          <StatusBar style="auto" />
        </AssistantProvider>
      </PaperProvider>
    </SafeAreaProvider>
  );
}
