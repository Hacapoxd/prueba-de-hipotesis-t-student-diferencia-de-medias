document.getElementById('test-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const sample1 = document.getElementById('sample1').value.split(',').map(Number);
    const sample2 = document.getElementById('sample2').value.split(',').map(Number);
    const alpha = parseFloat(document.getElementById('alpha').value);
    const hypothesis = document.getElementById('hypothesis').value;

    const response = await fetch('/calculate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sample1, sample2, alpha, hypothesis }),
    });

    const result = await response.json();
    document.getElementById('result').style.display = 'block';
    document.getElementById('result').innerHTML = result.message;

    // Actualiza la gráfica
    drawChart(result.chartData);
});

function drawChart(data) {
    const ctx = document.getElementById('chart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.x,
            datasets: [{
                label: 'Distribución T',
                data: data.y,
                borderColor: 'blue',
                fill: false,
            }],
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false },
            },
        },
    });
}
