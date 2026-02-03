import React from "react";
import "../App.css";

export default function DataTable({ summary }) {
  // ✅ Default view before upload
  if (!summary || !summary.data_preview) {
    return (
      <div className="table-card">
        <h2 className="section-title">Dataset Table Preview</h2>
        <p className="table-placeholder">
          Upload a dataset to view the table preview here.
        </p>
      </div>
    );
  }

  const columns = summary.preview_columns || [];
  const rows = summary.data_preview || [];

  return (
    <div className="table-card">
      <h2 className="section-title">Dataset Table Preview (First 10 Rows)</h2>

      <div className="table-wrapper">
        <table className="dataset-table">
          <thead>
            <tr>
              {columns.map((col, index) => (
                <th key={index}>{col}</th>
              ))}
            </tr>
          </thead>

          <tbody>
            {rows.map((row, rowIndex) => (
              <tr key={rowIndex}>
                {columns.map((col, colIndex) => (
                  <td key={colIndex}>{row[col]}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}