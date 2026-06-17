document.addEventListener('DOMContentLoaded', () => {
  const el = document.getElementById('dashboard-data');
  if (!el) return;
 
  const datos = JSON.parse(el.textContent);
 
  Chart.defaults.font.family = "'Lato', 'Segoe UI', sans-serif";
  Chart.defaults.color = '#6B6B6B';
 
  // ── Gráfico: Reservas por estado (doughnut) ──────────────────────────────
  new Chart(document.getElementById('cEstados'), {
    type: 'doughnut',
    data: {
      labels: ['Pendientes', 'Confirmadas', 'Finalizadas', 'Vencidas'],
      datasets: [{
        data: [
          datos.reservas_por_estado.pendientes,
          datos.reservas_por_estado.confirmadas,
          datos.reservas_por_estado.finalizadas,
          datos.reservas_por_estado.vencidas,
        ],
        backgroundColor: ['#C8973A', '#2e7d32', '#7B1E1E', '#1565c0', '#6B6B6B'],
        borderWidth: 2,
        borderColor: '#fff',
        hoverOffset: 6,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'bottom',
          labels: { padding: 14, boxWidth: 11, font: { size: 11 } },
        },
        tooltip: {
          callbacks: { label: (c) => ` ${c.label}: ${c.raw}` },
        },
      },
    },
  });
 
  // ── Gráfico: Productos por categoría (bar horizontal) ───────────────────
  const cats = datos.productos_por_categoria;
  new Chart(document.getElementById('cCats'), {
    type: 'bar',
    data: {
      labels: cats.map(
        (c) => c.categoria.charAt(0).toUpperCase() + c.categoria.slice(1)
      ),
      datasets: [{
        label: 'Productos',
        data: cats.map((c) => c.cantidad),
        backgroundColor: ['#7B1E1E', '#2e7d32', '#1565c0', '#C8973A'],
        borderRadius: 5,
        borderSkipped: false,
      }],
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: (c) => ` ${c.raw} producto${c.raw !== 1 ? 's' : ''}`,
          },
        },
      },
      scales: {
        x: {
          beginAtZero: true,
          ticks: { stepSize: 1 },
          grid: { color: 'rgba(0,0,0,0.05)' },
        },
        y: { grid: { display: false } },
      },
    },
  });
 
  // ── Gráfico: Reservas por día (line) ────────────────────────────────────
  const diasEl = document.getElementById('cDias');
  if (diasEl && datos.reservas_por_dia && datos.reservas_por_dia.length) {
    new Chart(diasEl, {
      type: 'line',
      data: {
        labels: datos.reservas_por_dia.map((d) => d.dia),
        datasets: [{
          label: 'Reservas',
          data: datos.reservas_por_dia.map((d) => d.cantidad),
          borderColor: '#7B1E1E',
          backgroundColor: 'rgba(123,30,30,0.08)',
          borderWidth: 2.5,
          pointBackgroundColor: '#7B1E1E',
          pointRadius: 5,
          pointHoverRadius: 7,
          fill: true,
          tension: 0.35,
        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: (c) => ` ${c.raw} reserva${c.raw !== 1 ? 's' : ''}`,
            },
          },
        },
        scales: {
          y: {
            beginAtZero: true,
            ticks: { stepSize: 1 },
            grid: { color: 'rgba(0,0,0,0.05)' },
          },
          x: { grid: { display: false } },
        },
      },
    });
  }
});
 