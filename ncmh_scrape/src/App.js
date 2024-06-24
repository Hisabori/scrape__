import React, { useEffect, useState } from 'react';
import axios from 'axios';
import {CardBody, CardText, CardTitle} from "reactstrap";

function App() {
    const [doctors, setDoctors] = useState([]);

    useEffect(() => {
        axios.get('http://localhost:3001/doctors')
            .then(response => {
                setDoctors(response.data);
            })
            .catch(error => console.error('Error fetching data: ', error));
    }, []);

    return (
        <Container>
            <Row>
                {doctors.map(doctor => (
                    <Col sm="12" md="6" lg="4" xl="3" key={doctor._id} style={{ marginBottom: '20px' }}>
                        <Card>
                            <CardBody>
                                <CardTitle tag="h5">{doctor.name}</CardTitle>
                                <CardText>진료 분야: {doctor.areas}</CardText>
                                <CardText>주요 경력: {doctor.career}</CardText>
                                <CardText>학회 활동: {doctor.activities}</CardText>
                            </CardBody>
                        </Card>
                    </Col>
                ))}
            </Row>
        </Container>
    );
}

export default App;
