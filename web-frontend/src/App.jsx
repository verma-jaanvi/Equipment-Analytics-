import { useState, useEffect } from "react";
import API, { clearToken } from "./api";

import Login from "./components/Login";
import Signup from "./components/Signup";
import UploadForm from "./components/UploadForm";
import SummaryCards from "./components/SummaryCards";
import DataTable from "./components/DataTable";
import Charts from "./components/Charts";
import History from "./components/History";

import "./App.css";

function App() {
  const [summary, setSummary] = useState({});
  const [datasetId, setDatasetId] = useState(null);

  const [loggedIn, setLoggedIn] = useState(false);
  const [authView, setAuthView] = useState("login");

  // ✅ Download Button Status
  const [downloadStatus, setDownloadStatus] = useState("idle");
  // idle → downloading → downloaded

  // ====================================================
  // ✅ Token Persistence on Reload
  // ====================================================
  useEffect(() => {
    const savedToken = localStorage.getItem("token");

    if (savedToken) {
      setLoggedIn(true);
    }
  }, []);

  // ====================================================
  // ✅ Download Report
  // ====================================================
  const downloadCurrentReport = async () => {
    if (!datasetId) {
      return;
    }

    try {
      setDownloadStatus("downloading");

      const res = await API.get(`report/${datasetId}/`, {
        responseType: "blob",
      });

      const url = window.URL.createObjectURL(new Blob([res.data]));
      const a = document.createElement("a");

      a.href = url;
      a.download = `report_${datasetId}.pdf`;
      a.click();

      setDownloadStatus("downloaded");

      setTimeout(() => {
        setDownloadStatus("idle");
      }, 2000);
    } catch {
      setDownloadStatus("idle");
      alert("PDF download failed ❌");
    }
  };

  // ====================================================
  // ✅ Logout Handler (Reset Everything)
  // ====================================================
  const handleLogout = () => {
    clearToken();

    setLoggedIn(false);
    setAuthView("login");

    setSummary({});
    setDatasetId(null);

    setDownloadStatus("idle");
  };

  return (
    <div className="app-container">
      {/* ====================================================
          ✅ AUTH SCREENS
      ==================================================== */}
      {!loggedIn ? (
        <div className="auth-container">
          {authView === "login" ? (
            <Login
              onLogin={() => setLoggedIn(true)}
              onSwitchToSignup={() => setAuthView("signup")}
            />
          ) : (
            <Signup onSwitchToLogin={() => setAuthView("login")} />
          )}
        </div>
      ) : (
        /* ====================================================
            ✅ DASHBOARD SCREEN
        ==================================================== */
        <div className="dashboard-layout">
          {/* ✅ SIDEBAR */}
          <aside className="sidebar">
            <div className="sidebar-card dashboard-link">
              <div className="dashboard-icon">📊</div>
              <h2 className="sidebar-title">Dashboard</h2>
              <p className="dashboard-subtitle">Analytics & Reports</p>
            </div>

            {/* ✅ Upload + Download */}
            <div className="sidebar-card sidebar-actions">
              <h3 className="action-section-title">Actions</h3>
              <UploadForm
                onUploadSuccess={(data) => {
                  setSummary(data.summary);
                  setDatasetId(data.dataset_id);
                }}
              />

              {/* ✅ Improved Download Button */}
              <button
                className={`btn-download ${downloadStatus === "downloaded" ? "downloaded" : ""}`}
                onClick={downloadCurrentReport}
                disabled={!datasetId || downloadStatus === "downloading"}
              >
                {downloadStatus === "downloading"
                  ? "⏳ Downloading..."
                  : downloadStatus === "downloaded"
                  ? "✅ Downloaded"
                  : "📥 Download Report"}
              </button>
            </div>

            {/* ✅ Recent Upload History */}
            <div className="sidebar-card recent-uploads">
              <h3 className="section-title">
                <span className="title-icon">🕒</span>
                Recent Uploads
              </h3>
              <History loggedIn={loggedIn} />
            </div>

            {/* ✅ Logout */}
            <button className="btn-logout" onClick={handleLogout}>
              <span className="logout-icon">🚪</span>
              Logout
            </button>
          </aside>

          {/* ✅ MAIN CONTENT */}
          <main className="main-content">
            <header className="content-header">
              <div className="header-content">
                <h1 className="page-title">Equipment Analytics Overview</h1>
                <p className="page-subtitle">Comprehensive data analysis and visualization</p>
              </div>
            </header>

            {/* ✅ Scroll Area */}
            <div className="analytics-scroll-area">
              {/* ✅ Summary Section */}
              <section className="summary-section">
                <SummaryCards summary={summary} />
              </section>

              {/* ✅ Data Table Section */}
              <section className="table-section">
                <DataTable summary={summary} />
              </section>

              {/* ✅ Charts Section */}
              <section className="charts-section">
                <Charts summary={summary} />
              </section>
            </div>
          </main>
        </div>
      )}
    </div>
  );
}

export default App;