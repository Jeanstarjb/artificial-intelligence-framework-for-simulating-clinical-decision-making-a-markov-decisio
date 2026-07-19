import React, { useState } from 'react';
import { Box, Button, FormControl, FormLabel, Input, VStack, useToast } from '@chakra-ui/react';
import { useNavigate } from 'react-router-dom';

const PatientInput = () => {
  const [patientData, setPatientData] = useState({
    firstName: '',
    lastName: '',
    dob: '',
    gender: '',
    medicalRecordNumber: ''
  });
  const toast = useToast();
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setPatientData({ ...patientData, [name]: value });
  };

  const handleSubmit = async () => {
    try {
      const response = await fetch('/api/ingest/ehr', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(patientData),
      });

      if (response.ok) {
        toast({
          title: 'Patient data submitted successfully!',
          status: 'success',
          duration: 3000,
          isClosable: true,
        });
        navigate('/recommendations');
      } else {
        toast({
          title: 'Error submitting patient data.',
          status: 'error',
          duration: 3000,
          isClosable: true,
        });
      }
    } catch (error) {
      console.error(error);
      toast({
        title: 'An unexpected error occurred.',
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
    }
  };

  return (
    <Box maxW="md" mx="auto" mt={10} p={6} boxShadow="lg" borderRadius="md" bg="white">
      <VStack spacing={4} align="stretch">
        <FormControl id="firstName">
          <FormLabel>First Name</FormLabel>
          <Input
            type="text"
            name="firstName"
            value={patientData.firstName}
            onChange={handleChange}
            placeholder="Enter first name"
          />
        </FormControl>
        <FormControl id="lastName">
          <FormLabel>Last Name</FormLabel>
          <Input
            type="text"
            name="lastName"
            value={patientData.lastName}
            onChange={handleChange}
            placeholder="Enter last name"
          />
        </FormControl>
        <FormControl id="dob">
          <FormLabel>Date of Birth</FormLabel>
          <Input
            type="date"
            name="dob"
            value={patientData.dob}
            onChange={handleChange}
          />
        </FormControl>
        <FormControl id="gender">
          <FormLabel>Gender</FormLabel>
          <Input
            type="text"
            name="gender"
            value={patientData.gender}
            onChange={handleChange}
            placeholder="Enter gender"
          />
        </FormControl>
        <FormControl id="medicalRecordNumber">
          <FormLabel>Medical Record Number</FormLabel>
          <Input
            type="text"
            name="medicalRecordNumber"
            value={patientData.medicalRecordNumber}
            onChange={handleChange}
            placeholder="Enter medical record number"
          />
        </FormControl>
        <Button colorScheme="blue" onClick={handleSubmit} width="full">
          Submit
        </Button>
      </VStack>
    </Box>
  );
};

export default PatientInput;
