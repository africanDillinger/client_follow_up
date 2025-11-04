// app/static/chart-init.js
function initFollowupChart(weekly, monthly, total) {
  const ctx = document.getElementById('followupChart').getContext('2d');
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Weekly','Monthly','Total'],
      datasets: [{
        label: 'Number of follow-ups',
        data: [weekly, monthly, total],
      }]
    },
    options: { responsive: true }
  });
}
