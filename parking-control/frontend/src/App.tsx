import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider, CssBaseline } from '@mui/material';
import { theme } from './theme';
import Layout from './components/Layout';
import LoginPage from './pages/LoginPage';
import ParkingMapPage from './pages/ParkingMapPage';
import VehiclesPage from './pages/VehiclesPage';
import { useAuthStore } from './stores/authStore';

function App() {
  const isAuthenticated = useAuthStore(state => state.isAuthenticated);

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Routes>
          <Route path="/login" element={
            !isAuthenticated ? <LoginPage /> : <Navigate to="/parking-map" />
          } />
          
          <Route path="/" element={
            isAuthenticated ? <Layout /> : <Navigate to="/login" />
          }>
            <Route path="parking-map" element={<ParkingMapPage />} />
            <Route path="vehicles" element={<VehiclesPage />} />
            <Route index element={<Navigate to="/parking-map" />} />
          </Route>
        </Routes>
      </Router>
    </ThemeProvider>
  );
}

export default App; 