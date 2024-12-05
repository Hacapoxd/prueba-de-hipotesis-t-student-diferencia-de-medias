document.getElementById('test-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const sample1 = document.getElementById('sample1').value.split(',').map(Number);
    const sample2 = document.getElementById('sample2').value.split(',').map(Number);
    const alpha = parseFloat(document.getElementById('alpha').value);
    const hypothesis = document.getElementById('hypothesis').value;

    try {
        const response = await fetch('/calculate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ sample1, sample2, alpha, hypothesis }),
        });

        const result = await response.json();
        if (result.error) {
            alert(`Error: ${result.error}`);
            return;
        }

        // Mostrar el mensaje del resultado
        document.getElementById('result').style.display = 'block';
        document.getElementById('result').innerHTML = result.message;

        // Actualizar la gráfica
        drawChart(result.chartData);

    } catch (error) {
        alert('Hubo un problema al procesar los datos.');
    }
});

function drawChart(data) {
    const ctx = document.getElementById('chart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.x,
            datasets: [
                {
                    label: 'Distribución T',
                    data: data.y,
                    borderColor: 'blue',
                    fill: false,
                },
                // Regiones de rechazo - Izquierda y Derecha
                ...Object.keys(data.rejectRegions).map(region => {
                    return {
                        label: `Región de rechazo ${region}`,
                        data: data.rejectRegions[region].y,
                        backgroundColor: region === 'izquierda' ? 'rgba(255, 99, 132, 0.2)' : 'rgba(54, 162, 235, 0.2)',
                        borderColor: region === 'izquierda' ? 'rgba(255, 99, 132, 1)' : 'rgba(54, 162, 235, 1)',
                        borderWidth: 1,
                        fill: true, // Esto hace que se sombreen las áreas
                    };
                }),
            ],
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: true },
            },
            scales: {
                x: {
                    ticks: {
                        stepSize: 0.5,
                    },
                    min: -4,  // Límite inferior del eje X
                    max: 4,   // Límite superior del eje X
                },
                y: {
                    beginAtZero: false,
                },
            },
        },
    });
}


