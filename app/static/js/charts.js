document.addEventListener('DOMContentLoaded', function() {
    const ctx = document.getElementById('weightChart');
    if (!ctx) return;

    fetch('/api/progress-data')
        .then(response => response.json())
        .then(data => {
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: 'Weight (kg)',
                        data: data.data,
                        borderColor: '#0d6efd',
                        backgroundColor: 'rgba(13, 110, 253, 0.1)',
                        tension: 0.4,
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            labels: { color: '#e0e0e0' }
                        }
                    },
                    scales: {
                        y: {
                            grid: { color: '#333' },
                            ticks: { color: '#e0e0e0' }
                        },
                        x: {
                            grid: { color: '#333' },
                            ticks: { color: '#e0e0e0' }
                        }
                    }
                }
            });
        });
});
