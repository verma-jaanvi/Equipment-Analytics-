// components/SummaryCards.jsx
import React from 'react';
import '../App.css';

export default function SummaryCards({ summary }) {
  if (!summary) return null; // Or return your skeleton loader

  const stats = [
    { label: "Total Equipment", value: summary.total_count || 0 },
    { label: "Average Flowrate", value: summary.avg_flowrate?.toFixed(1) || "0.0" },
    { label: "Average Pressure", value: summary.avg_pressure?.toFixed(2) || "0.00" },
    { label: "Average Temperature", value: summary.avg_temperature?.toFixed(2) || "0.00" },
  ];

  // Logic: check for equipment_distribution OR type_distribution
  const distributionData = summary.equipment_distribution || summary.type_distribution;

  return (
    <div className="main-summary-container">
      <h2 className="summary-title">Summary Statistics</h2>
      
      <div className="stats-grid">
        {stats.map((item, index) => (
          <div key={index} className="stat-card-outer">
            <div className="stat-label-box">{item.label}</div>
            <div className="stat-value-box">{item.value}</div>
          </div>
        ))}
      </div>

      {/* The List Section */}
      {distributionData && (
        <div className="distribution-panel-left">
          <p className="distribution-header">Equipment Distribution:</p>
          <ul className="distribution-list">
            {Object.entries(distributionData).map(([key, val]) => (
              <li key={key}>• {key}: {val}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}