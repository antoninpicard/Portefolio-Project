import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';

// Pages
import HomePage from './pages/HomePage';
import CircuitBuilderPage from './pages/CircuitBuilderPage';
import AlgorithmLibraryPage from './pages/AlgorithmLibraryPage';
import TutorialPage from './pages/TutorialPage';
import AboutPage from './pages/AboutPage';

// Components
import MainLayout from './components/layout/MainLayout';

// Context providers
import { CircuitProvider } from './contexts/CircuitContext';
import { SimulationProvider } from './contexts/SimulationContext';

// Create theme
const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#3f51b5',
    },
    secondary: {
      main: '#f50057',
    },
    background: {
      default: '#f5f5f5',
      paper: '#ffffff',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    h1: {
      fontSize: '2.5rem',
      fontWeight: 500,
    },
    h2: {
      fontSize: '2rem',
      fontWeight: 500,
    },
    h3: {
      fontSize: '1.75rem',
      fontWeight: 500,
    },
    h4: {
      fontSize: '1.5rem',
      fontWeight: 500,
    },
    h5: {
      fontSize: '1.25rem',
      fontWeight: 500,
    },
    h6: {
      fontSize: '1rem',
      fontWeight: 500,
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
        },
      },
    },
  },
});

const App: React.FC = () => {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <CircuitProvider>
        <SimulationProvider>
          <Router>
            <MainLayout>
              <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/circuit-builder" element={<CircuitBuilderPage />} />
                <Route path="/algorithm-library" element={<AlgorithmLibraryPage />} />
                <Route path="/tutorials" element={<TutorialPage />} />
                <Route path="/about" element={<AboutPage />} />
              </Routes>
            </MainLayout>
          </Router>
        </SimulationProvider>
      </CircuitProvider>
    </ThemeProvider>
  );
};

export default App;
