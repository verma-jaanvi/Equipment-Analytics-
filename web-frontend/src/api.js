import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000/api/",
});

// ✅ Load token from localStorage on startup
let token = localStorage.getItem("token");

// ✅ Attach token automatically to every request
API.interceptors.request.use((req) => {
  if (token) {
    req.headers.Authorization = `Token ${token}`;
  }
  return req;
});

// =====================================================
// ✅ TOKEN HELPERS (UNCHANGED)
// =====================================================

// ✅ Save token (Login)
export const setToken = (newToken) => {
  token = newToken;
  localStorage.setItem("token", newToken);
};

// ✅ Remove token (Logout)
export const clearToken = () => {
  token = null;
  localStorage.removeItem("token");
};

// =====================================================
// ✅ AUTH APIs (NEW - Added Safely)
// =====================================================

// ✅ Signup API
export const signupUser = async (username, email, password) => {
  const res = await API.post("signup/", {
    username,
    email,
    password,
  });
  return res.data;
};

// ✅ Login API (returns token)
export const loginUser = async (username, password) => {
  const res = await API.post("token/", {
    username,
    password,
  });

  // ✅ Save token automatically after login
  setToken(res.data.token);

  return res.data;
};

// =====================================================
// ✅ EXISTING FUNCTIONALITIES (UPLOAD/HISTORY/REPORT)
// =====================================================

// ✅ Upload CSV
export const uploadCSV = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  const res = await API.post("upload/", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });

  return res.data;
};

// ✅ Fetch User History (last 5 uploads)
export const fetchHistory = async () => {
  const res = await API.get("history/");
  return res.data;
};

// ✅ Download PDF Report
export const downloadReport = async (datasetId) => {
  const res = await API.get(`report/${datasetId}/`, {
    responseType: "blob",
  });

  // ✅ Convert blob into downloadable file
  const url = window.URL.createObjectURL(new Blob([res.data]));

  const link = document.createElement("a");
  link.href = url;
  link.setAttribute("download", `report_${datasetId}.pdf`);

  document.body.appendChild(link);
  link.click();
  link.remove();
};

export default API;