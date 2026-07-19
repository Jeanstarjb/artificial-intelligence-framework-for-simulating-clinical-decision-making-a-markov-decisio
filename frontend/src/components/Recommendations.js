import React, { useEffect, useState } from 'react';
import { Box, Heading, Text, VStack, Spinner } from '@chakra-ui/react';

const Recommendations = () => {
  const [recommendations, setRecommendations] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchRecommendations = async () => {
      try {
        const response = await fetch('/api/simulate/recommendations');
        const data = await response.json();
        setRecommendations(data);
      } catch (error) {
        console.error('Error fetching recommendations:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchRecommendations();
  }, []);

  if (loading) {
    return (
      <Box textAlign="center" mt={10}>
        <Spinner size="xl" />
      </Box>
    );
  }

  return (
    <Box maxW="4xl" mx="auto" mt={10} p={6} boxShadow="lg" borderRadius="md" bg="white">
      <Heading size="lg" mb={4} color="blue.600">Treatment Recommendations</Heading>
      <VStack spacing={4} align="stretch">
        {recommendations?.map((rec, index) => (
          <Box key={index} p={4} borderWidth="1px" borderRadius="md" bg="gray.100">
            <Text fontWeight="bold">{rec.action}</Text>
            <Text>{rec.description}</Text>
          </Box>
        ))}
      </VStack>
    </Box>
  );
};

export default Recommendations;
