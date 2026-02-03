import { useRef, useState } from "react";
import API from "../api";

export default function UploadForm({ onUploadSuccess }) {
  const fileInputRef = useRef(null);
  const [status, setStatus] = useState({ message: "", type: "" }); // types: 'success', 'error', 'loading'

  const handleButtonClick = () => {
    fileInputRef.current.click();
  };

  const showNotification = (msg, type) => {
    setStatus({ message: msg, type: type });
    
    // Auto-hide after 3 seconds
    setTimeout(() => {
      setStatus({ message: "", type: "" });
    }, 3000);
  };

  const handleFileChange = async (e) => {
    const selectedFile = e.target.files[0];
    if (!selectedFile) return;

    if (!selectedFile.name.endsWith(".csv")) {
      showNotification("Only CSV files allowed!", "error");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      setStatus({ message: "Uploading...", type: "loading" });
      
      const res = await API.post("upload/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      showNotification("Upload successful ✅", "success");
      
      // Trigger dashboard update
      onUploadSuccess(res.data);
    } catch (err) {
      console.error("UPLOAD ERROR:", err.response?.data);
      showNotification("Upload failed ❌", "error");
    } finally {
      e.target.value = "";
    }
  };

  return (
    <div className="upload-container" style={{ position: "relative" }}>
      {/* Hidden File Input */}
      <input
        type="file"
        ref={fileInputRef}
        onChange={handleFileChange}
        accept=".csv"
        style={{ display: "none" }}
      />

      {/* Main Upload Button */}
      <button 
        className="btn-upload" 
        onClick={handleButtonClick}
        disabled={status.type === "loading"}
      >
        <span className="icon">{status.type === "loading" ? "⏳" : "📂"}</span> 
        {status.type === "loading" ? "Processing..." : "Upload Dataset"}
      </button>

      {/* Floating 3-Second Notification Box */}
      {status.message && (
        <div className={`upload-toast ${status.type}`}>
          {status.message}
        </div>
      )}
    </div>
  );
}