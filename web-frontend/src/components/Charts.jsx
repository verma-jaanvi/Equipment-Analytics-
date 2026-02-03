import React from "react";
import {
  Chart as ChartJS,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
  ArcElement,
} from "chart.js";
import { Bar, Doughnut } from "react-chartjs-2";
import ChartDataLabels from "chartjs-plugin-datalabels";

ChartJS.register(
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
  ArcElement,
  ChartDataLabels
);

export default function Charts({ summary }) {
  if (!summary || !summary.type_distribution) return null;

  const typeLabels = Object.keys(summary.type_distribution);
  const typeValues = Object.values(summary.type_distribution);

  const colors = ["#3b82f6", "#22c55e", "#f97316", "#ef4444", "#a855f7", "#14b8a6"];
  const backgroundColors = typeLabels.map((_, i) => colors[i % colors.length]);

  const barOptions = {
    responsive: true,
    maintainAspectRatio: false, // Allows the chart to fill the container height/width
    plugins: {
      legend: { display: false },
      datalabels: {
        anchor: "end",
        align: "top",
        color: "#1e293b",
        font: { weight: "bold", size: 14 },
      },
    },
    scales: {
      x: { grid: { display: false }, ticks: { color: "#64748b" } },
      y: { beginAtZero: true, grid: { color: "#f1f5f9" } },
    },
  };

  const doughnutOptions = {
    responsive: true,
    maintainAspectRatio: false,
    cutout: "60%",
    plugins: {
      legend: {
        position: "right",
        labels: { boxWidth: 12, padding: 15, color: "#1e293b" },
      },
      datalabels: {
        color: "#1e293b",
        font: { weight: "bold", size: 11 },
        formatter: (value, ctx) => {
          let sum = 0;
          ctx.chart.data.datasets[0].data.forEach(d => { sum += d; });
          return ((value * 100) / sum).toFixed(1) + "%";
        },
      },
    },
  };

  return (
    <div className="charts-full-wrapper">
      <div className="charts-header-card">
        <h2 className="charts-title">Charts & Visualizations</h2>
      </div>

      <div className="charts-flex-container">
        <div className="chart-card-half">
          <h3 className="chart-label">Equipment Distribution</h3>
          <div className="chart-canvas-holder">
            <Bar data={{
              labels: typeLabels,
              datasets: [{ data: typeValues, backgroundColor: backgroundColors, borderRadius: 5 }]
            }} options={barOptions} />
          </div>
        </div>

        <div className="chart-card-half">
          <h3 className="chart-label">Type Share (%)</h3>
          <div className="chart-canvas-holder">
            <Doughnut data={{
              labels: typeLabels,
              datasets: [{ data: typeValues, backgroundColor: backgroundColors, borderWidth: 0 }]
            }} options={doughnutOptions} />
          </div>
        </div>
      </div>
    </div>
  );
}