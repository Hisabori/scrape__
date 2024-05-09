const express = require('express');
const { MongoClient } = require('mongodb');
const cors = require('cors');

const app = express();
app.use(cors()); // CORS 미들웨어 추가 (클라이언트에서 서버의 다른 포트로 요청 가능하게 설정)
const PORT = 3001;
const uri = "mongodb://localhost:27017"; // MongoDB 연결 URI
const client = new MongoClient(uri, { useNewUrlParser: true, useUnifiedTopology: true });

app.get('/doctors', async (req, res) => {
    try {
        await client.connect();  // MongoDB에 연결
        const database = client.db('hospital'); // 사용할 데이터베이스 선택
        const doctors = database.collection('doctors'); // 데이터베이스에서 'doctors' 컬렉션 사용
        const doctorList = await doctors.find({}).toArray(); // 모든 의사 정보를 배열로 반환
        res.json(doctorList);
    } catch (error) {
        console.error('Error accessing MongoDB', error);
        res.status(500).send('Error accessing MongoDB');
    } finally {
        await client.close(); // 요청 처리 후 연결 닫기
    }
});

app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
