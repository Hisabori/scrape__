// html2canvas 라이브러리를 로드합니다
const script = document.createElement('script');
script.src = chrome.runtime.getURL('html2canvas.min.js');
script.onload = function() {
    function createOverlay(data) {
        const overlay = document.createElement('div');
        overlay.id = 'my-extension-overlay';
        overlay.innerHTML = `
            <div class="overlay-content">
                <h1>Trading Information</h1>
                <p>Pattern: ${data.pattern}</p>
                <p>Result: ${data.result}</p>
                <p>Entry Price: ${data.entry_price}</p>
                <p>Stop Loss: ${data.stop_loss}</p>
                <p>Take Profit: ${data.take_profit}</p>
            </div>
        `;
        document.body.appendChild(overlay);
    }

    function fetchData(imageBase64) {
        fetch('http://127.0.0.1:5000/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ image_url: imageBase64 })
        })
            .then(response => response.json())
            .then(data => {
                createOverlay(data);
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }

    function captureChart() {
        const chart = document.querySelector('.your-chart-selector'); // 차트 요소 선택자
        if (!chart) {
            console.error('Chart element not found.');
            return;
        }
        html2canvas(chart).then(canvas => {
            const imageBase64 = canvas.toDataURL('image/png');
            fetchData(imageBase64);
        });
    }

    (function() {
        captureChart();
    })();
};
document.head.appendChild(script);
