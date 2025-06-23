const ctx = document.getElementById('chart').getContext('2d');
const data = {
  labels: [],
  datasets: [{
    label: 'Detecciones',
    data: [],
    borderColor: 'rgb(75, 192, 192)',
    tension: 0.1
  }]
};

const chart = new Chart(ctx, {
  type: 'line',
  data: data,
  options: {
    scales: {
      x: { title: { display: true, text: 'Tiempo' } },
      y: { beginAtZero: true }
    }
  }
});

function fetchStats() {
  fetch('/stats')
    .then(res => res.json())
    .then(data => {
      document.getElementById('count').textContent = "Objetos detectados: " + data.count;
      chart.data.labels = data.history.map(d => d.timestamp);
      chart.data.datasets[0].data = data.history.map(d => d.detecciones);
      chart.update();
    });
}

setInterval(fetchStats, 1000);
