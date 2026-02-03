import { useState } from "react";
import API, { setToken } from "../api";

export default function Login({ onLogin, onSwitchToSignup }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  // ✅ Message states
  const [message, setMessage] = useState("");
  const [msgType, setMsgType] = useState(""); // success | error
  const [loading, setLoading] = useState(false);

  const showMessage = (text, type = "success") => {
    setMessage(text);
    setMsgType(type);

    // ✅ Auto hide after 3 sec
    setTimeout(() => {
      setMessage("");
      setMsgType("");
    }, 3000);
  };

  const handleLogin = async (e) => {
    e.preventDefault();

    if (!username || !password) {
      showMessage("⚠️ Please enter both fields", "error");
      return;
    }

    setLoading(true);

    try {
      const res = await API.post("token/", { username, password });

      setToken(res.data.token);

      // ✅ Show success message
      showMessage("✅ Login Successful! Redirecting...", "success");

      // ✅ Redirect after 3 sec
      setTimeout(() => {
        onLogin(username);
      }, 3000);

    } catch {
      showMessage("❌ Invalid username or password", "error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-card">
      {/* Icon */}
      <div className="user-icon-circle">
        <span style={{ fontSize: "28px" }}>👤</span>
      </div>

      {/* ✅ Message Display */}
      {message && (
        <div className={`form-message ${msgType}`}>
          {message}
        </div>
      )}

      <form onSubmit={handleLogin} style={{ marginTop: "30px" }}>
        <div className="input-field-wrapper">
          <span className="input-icon">👤</span>
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>

        <div className="input-field-wrapper">
          <span className="input-icon">🔒</span>
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>

        <button type="submit" className="btn-login" disabled={loading}>
          {loading ? "LOADING..." : "LOGIN"}
        </button>
      </form>

      <button className="register-link" onClick={onSwitchToSignup}>
        Register
      </button>
    </div>
  );
}