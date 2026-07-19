import React, { useEffect, useState } from 'react';
import { Box, Heading, Table, Thead, Tbody, Tr, Th, Td, Spinner } from '@chakra-ui/react';

const SimulationResults = () => {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchResults = async () => {
      try {
        const response = await fetch('/api/simulate/results');
        const data = await response.json();
        setResults(data);
      } catch (error) {
        console.error('Error fetching simulation results:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchResults();
  }, []);

  if (loading) {
    return (
      <Box textAlign="center" mt={10}>
        <Spinner size="xl" />
      </Box>
    );
  }

  return (
    <Box maxW="6xl" mx="auto" mt={10} p={6} boxShadow="lg" borderRadius="md" bg="white">
      <Heading size="lg" mb={4} color="blue.600">Simulation Results</Heading>
      <Table variant="simple">
        <Thead>
          <Tr>
            <Th>State</Th>
            <Th>Action</Th>
            <Th>Reward</Th>
            <Th>QALY</Th>
            <Th>Confidence Interval</Th>
          </Tr>
        </Thead>
        <Tbody>
          {results?.state_history.map((state, index) => (
            <Tr key={index}>
              <Td>{state.state}</Td>
              <Td>{state.action}</Td>
              <Td>{state.reward}</Td>
              <Td>{state.qaly}</Td>
              <Td>{state.confidence_interval.join(' - ')}</Td>
            </Tr>
          ))}
        </Tbody>
      </Table>
    </Box>
  );
};

export default SimulationResults;
