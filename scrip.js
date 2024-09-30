document.getElementById('mineBlockButton').addEventListener('click', function() {
    const data = prompt("Nhập dữ liệu cho khối mới:", "New transaction data");
    const token = prompt("Nhập token cho khối mới:", "NEW_TOKEN");

    fetch('/mine_block', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ data: data, token: token }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        document.getElementById('resultMessage').innerText = 
            `Khối đã được khai thác! Index: ${data.index}, Hash: ${data.hash}`;
    })
    .catch((error) => {
        document.getElementById('resultMessage').innerText = 'Có lỗi xảy ra: ' + error.message;
    });
});
