const ctx = document.getElementById('resultsChart').getContext('2d');
new Chart(ctx, {
    type: 'pie',
    data: {
        labels: labels,
        datasets: [{
            label: 'Vote Count',
            data: data,
            backgroundColor: [
                '#007bff', '#28a745', '#ffc107', '#dc3545',
                '#6610f2', '#20c997', '#fd7e14', '#6f42c1'
            ],
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'bottom',
                labels: {
                    color: '#fff',
                    font: {
                        size: 14
                    }
                }
            }
        }
    }
});
