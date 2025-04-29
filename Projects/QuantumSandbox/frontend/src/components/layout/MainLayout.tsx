import React from 'react';
import { Box, AppBar, Toolbar, Typography, Container, Button } from '@mui/material';
import { Link, useLocation } from 'react-router-dom';

const navLinks = [
  { label: 'Home', path: '/' },
  { label: 'Circuit Builder', path: '/circuit-builder' },
  { label: 'Algorithm Library', path: '/algorithm-library' },
  { label: 'Tutorials', path: '/tutorials' },
  { label: 'About', path: '/about' },
];

const MainLayout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const location = useLocation();
  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            QuantumSandbox
          </Typography>
          {navLinks.map(link => (
            <Button
              key={link.path}
              color={location.pathname === link.path ? 'secondary' : 'inherit'}
              component={Link}
              to={link.path}
              sx={{ ml: 2 }}
            >
              {link.label}
            </Button>
          ))}
        </Toolbar>
      </AppBar>
      <Container maxWidth="lg" sx={{ mt: 4 }}>
        {children}
      </Container>
    </Box>
  );
};

export default MainLayout;
