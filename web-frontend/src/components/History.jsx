import { useEffect, useState } from "react";
import API from "../api";

export default function History({ loggedIn }) {
  const [history, setHistory] = useState([]);

  const fetchHistory = async () => {
    try {
      const res = await API.get("history/");
      // We only want the most recent ones for the sidebar
      setHistory(res.data.slice(0, 5)); 
    } catch (err) {
      console.error("History fetch failed:", err.response?.status);
    }
  };

  useEffect(() => {
    if (loggedIn) {
      fetchHistory();
    }
  }, [loggedIn]);

  // Function to handle clicking a historical dataset 
  // (Optional: You can trigger a download or reload that summary)
  const handleHistoryClick = async (id) => {
    try {
      const response = await API.get(`report/${id}/`, {
        responseType: "blob",
      });
      const fileURL = window.URL.createObjectURL(response.data);
      const link = document.createElement("a");
      link.href = fileURL;
      link.download = `Dataset_${id}_Report.pdf`;
      link.click();
    } catch {
      alert("Could not fetch report for this dataset ❌");
    }
  };

  if (!loggedIn) return null;

  return (
    <div className="recent-uploads-list">
      {history.length === 0 ? (
        <p className="empty-history-text">No dataset reports yet</p>
      ) : (
        <ul className="history-items">
          {history.map((item) => (
            <li 
              key={item.id} 
              className="history-item"
              onClick={() => handleHistoryClick(item.id)}
            >
              Dataset-report {item.id}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}