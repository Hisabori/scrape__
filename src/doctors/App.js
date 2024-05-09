import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Container, Card, CardBody, CardTitle, CardText } from 'reactstrap';

function App() {
    const [doctors, setDoctors] = useState([]);

    useEffect(() => {
        axios.get('http://localhost:3001/doctors')  // 서버 API URL 수정
            .then(response => {
                setDoctors(response.data);
            })
            .catch(error => console.error('Error fetching data: ', error));
    }, []);

    return (
        <Container>
            {doctors.map(doctor => (
                <Card key={doctor._id} style={{ margin: '20px 0' }}>  // 고유 key로 _id 사용
                    <CardBody>
                        <CardTitle tag="h5">{doctor.name}</CardTitle>
                        <CardText>진료 분야: {doctor.areas}</CardText>
                        <CardText>주요 경력: {doctor.career}</CardText>
                        <CardText>학회 활동: {doctor.activities}</CardText>
                    </CardBody>
                </Card>
            ))}
        </Container>
    );
}

export default App;
