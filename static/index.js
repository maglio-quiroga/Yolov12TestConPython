const ctx = document.getElementById('chart').getContext('2d');

const chart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: [],
    datasets: [
      {
        label: 'Cantidad de Chalecos',
        data: [],
        borderColor: 'blue',
        yAxisID: 'y',
        tension: 0.3,
        fill: false,
        pointRadius: 2
      },
      {
        label: 'Confianza (%)',
        data: [],
        borderColor: 'green',
        yAxisID: 'y1',
        tension: 0.3,
        fill: false,
        pointRadius: 2
      }
    ]
  },
  options: {
    responsive: true,
    interaction: {
      mode: 'index',
      intersect: false,
    },
    stacked: false,
    plugins: {
      title: {
        display: true,
        text: 'Evolución de Detecciones'
      }
    },
    scales: {
      x: {
        title: { display: true, text: 'Hora' }
      },
      y: {
        type: 'linear',
        display: true,
        position: 'left',
        beginAtZero: true,
        title: { display: true, text: 'Cantidad' }
      },
      y1: {
        type: 'linear',
        display: true,
        position: 'right',
        beginAtZero: true,
        max: 100,
        title: { display: true, text: 'Confianza (%)' },
        grid: {
          drawOnChartArea: false
        }
      }
    }
  }
});

function fetchStats() {
  fetch('/stats')
    .then(res => res.json())
    .then(data => {
      document.getElementById('count').textContent = "Objetos detectados: " + data.count;
      const labels = data.history.map(d => d.timestamp);
      const detections = data.history.map(d => d.detecciones);
      const confidence = data.history.map(d => d.confianza);

      chart.data.labels = labels;
      chart.data.datasets[0].data = detections;
      chart.data.datasets[1].data = confidence;
      chart.update();
    });
}

setInterval(fetchStats, 1000);
