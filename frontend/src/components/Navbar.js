import React from 'react';
import { Box, Flex, HStack, Link, Text } from '@chakra-ui/react';
import { Link as RouterLink } from 'react-router-dom';

const Navbar = () => {
  return (
    <Box bg="blue.600" px={4} py={3} boxShadow="md">
      <Flex h={16} alignItems="center" justifyContent="space-between">
        <Text fontSize="lg" fontWeight="bold" color="white">
          CDSS Platform
        </Text>
        <HStack spacing={8} alignItems="center">
          <Link as={RouterLink} to="/" color="white" fontWeight="medium" _hover={{ textDecoration: 'underline' }}>
            Input Patient Data
          </Link>
          <Link as={RouterLink} to="/recommendations" color="white" fontWeight="medium" _hover={{ textDecoration: 'underline' }}>
            Recommendations
          </Link>
          <Link as={RouterLink} to="/results" color="white" fontWeight="medium" _hover={{ textDecoration: 'underline' }}>
            Simulation Results
          </Link>
        </HStack>
      </Flex>
    </Box>
  );
};

export default Navbar;
