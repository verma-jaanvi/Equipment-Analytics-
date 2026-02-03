import React, { useState } from "react";
import "../App.css";
import { signupUser } from "../api";

const Signup = ({ onSwitchToLogin }) => {
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
  });

  // ✅ Message States
  const [message, setMessage] = useState("");
  const [msgType, setMsgType] = useState("");
  const [loading, setLoading] = useState(false);

  const showMessage = (text, type = "success") => {
    setMessage(text);
    setMsgType(type);

    setTimeout(() => {
      setMessage("");
      setMsgType("");
    }, 3000);
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  // ✅ Signup Submit
  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      setLoading(true);

      await signupUser(
        formData.username,
        formData.email,
        formData.password
      );

      // ✅ Success message
      showMessage("✅ Account created! Redirecting to Login...", "success");

      // ✅ Redirect after 3 sec
      setTimeout(() => {
        onSwitchToLogin();
      }, 3000);

    } catch (error) {
      showMessage(
        error.response?.data?.error ||
          "❌ Signup failed. Username may already exist.",
        "error"
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-card">
      {/* Icon */}
      <div className="user-icon-circle">
        <span style={{ fontSize: "28px" }}>➕</span>
      </div>

      {/* ✅ Message Display */}
      {message && (
        <div className={`form-message ${msgType}`}>
          {message}
        </div>
      )}

      <form onSubmit={handleSubmit} style={{ marginTop: "30px" }}>
        <div className="input-field-wrapper">
          <span className="input-icon">👤</span>
          <input
            type="text"
            name="username"
            placeholder="Username"
            value={formData.username}
            onChange={handleChange}
            required
          />
        </div>

        <div className="input-field-wrapper">
          <span className="input-icon">✉️</span>
          <input
            type="email"
            name="email"
            placeholder="Email Address"
            value={formData.email}
            onChange={handleChange}
            required
          />
        </div>

        <div className="input-field-wrapper">
          <span className="input-icon">🔒</span>
          <input
            type="password"
            name="password"
            placeholder="Password"
            value={formData.password}
            onChange={handleChange}
            required
          />
        </div>

        <button type="submit" className="btn-login" disabled={loading}>
          {loading ? "CREATING..." : "REGISTER"}
        </button>
      </form>

      <button className="register-link" onClick={onSwitchToLogin}>
        Back to Login
      </button>
    </div>
  );
};

export default Signup;