import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Container, Card, CardContent, Typography, Box, Tabs, Tab, TextField } from '@mui/material';

function App() {
    const [doctors, setDoctors] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [tabValue, setTabValue] = useState(0);
    const [uniqueAreas, setUniqueAreas] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');

    useEffect(() => {
        setTimeout(() => {
            axios.get('http://localhost:3001/doctors')
                .then(response => {
                    const cleanedData = response.data.filter(doctor => doctor.name.toLowerCase() !== 'unknown' && doctor.areas.toLowerCase() !== 'unknown')
                        .map(doctor => ({
                            ...doctor,
                            areas: doctor.areas,
                            career: doctor.career.toLowerCase() !== 'unknown' ? doctor.career : '',
                            activities: doctor.activities.toLowerCase() !== 'unknown' ? doctor.activities : ''
                        }));
                    setDoctors(cleanedData);
                    setUniqueAreas([...new Set(cleanedData.map(doctor => doctor.areas))]); // Extract unique areas
                    setIsLoading(false);
                })
                .catch(error => {
                    console.error('Error fetching data: ', error);
                    setIsLoading(false);
                });
        }, 3000);
    }, []);

    const handleChangeTab = (event, newValue) => {
        setTabValue(newValue);
    };

    const handleSearchChange = (event) => {
        setSearchTerm(event.target.value);
    };

    if (isLoading) {
        return <Typography variant="h6" component="div" sx={{ textAlign: 'center', mt: 5 }}>Loading...</Typography>;
    }

    const filteredDoctors = searchTerm.startsWith('#') ?
        doctors.filter(doctor => doctor.areas.toLowerCase().includes(searchTerm.slice(1).toLowerCase())) :
        doctors.filter(doctor => doctor.name.toLowerCase().includes(searchTerm.toLowerCase()));

    return (
        <Container maxWidth="md">
            <TextField
                fullWidth
                label="Search by doctor's name or #area..."
                value={searchTerm}
                onChange={handleSearchChange}
                margin="normal"
                variant="outlined"
                sx={{ mb: 2 }}
            />
            <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
                <Tabs value={tabValue} onChange={handleChangeTab} aria-label="medical areas tabs" variant="scrollable" scrollButtons="auto">
                    {uniqueAreas.map((area, index) => (
                        <Tab key={area} label={area} />
                    ))}
                </Tabs>
            </Box>
            <Box sx={{ pt: 3 }}>
                {filteredDoctors.map(doctor => (
                    <Card key={doctor._id} sx={{ mb: 2 }}>
                        <CardContent>
                            <Typography variant="h5" component="div">{doctor.name}</Typography>
                            <Typography variant="subtitle1" sx={{ mt: 1 }}>진료 분야: {doctor.areas}</Typography>
                            <Typography variant="subtitle1" sx={{ mt: 1 }}>주요 경력: {doctor.career}</Typography>
                            <Typography variant="subtitle1" sx={{ mt: 1 }}>학회 활동: {doctor.activities}</Typography>
                        </CardContent>
                    </Card>
                ))}
            </Box>
        </Container>
    );
}

export default App;
