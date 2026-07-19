import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ChakraProvider, extendTheme } from '@chakra-ui/react';
import PatientInput from './components/PatientInput';
import Recommendations from './components/Recommendations';
import SimulationResults from './components/SimulationResults';
import Navbar from './components/Navbar';

const theme = extendTheme({
  styles: {
    global: {
      body: {
        bg: 'gray.50',
        color: 'gray.800',
      },
    },
  },
});

function App() {
  return (
    <ChakraProvider theme={theme}>
      <Router>
        <Navbar />
        <Routes>
          <Route path="/" element={<PatientInput />} />
          <Route path="/recommendations" element={<Recommendations />} />
          <Route path="/results" element={<SimulationResults />} />
        </Routes>
      </Router>
    </ChakraProvider>
  );
}

export default App;
