import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8000",
  timeout: 30000,
});

// ── Request: attach token ──────────────────
API.interceptors.request.use(
  (config) => {
    const token = sessionStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// ── Response: normalize errors, auto-logout ─
API.interceptors.response.use(
  (response) => response,
  (error) => {
    // Auto-logout on 401
    if (error.response?.status === 401) {
      sessionStorage.removeItem("token");
      sessionStorage.removeItem("user");
      window.location.href = "/";
      return Promise.reject(error);
    }

    // Normalize error message so every caller
    // can do:  catch(e) => e.message
    const message =
      error.response?.data?.detail ||
      error.response?.data?.message ||
      error.message ||
      "Something went wrong";

    error.message = message;
    return Promise.reject(error);
  }
);

export default API;