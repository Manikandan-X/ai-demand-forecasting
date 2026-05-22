import { useEffect, useState, useCallback, useRef } from "react";
import {
  getAdminDashboard,
  getUsers,
  getDatasets,
  getForecasts,
  getMonthlyAnalytics
} from "../api/admin";

export default function useAdminDashboard() {

  const [dashboard, setDashboard] = useState(null);
  const [users, setUsers] = useState([]);
  const [datasets, setDatasets] = useState([]);
  const [forecasts, setForecasts] = useState([]);
  const [monthly, setMonthly] = useState([]);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const [userPage, setUserPage] = useState(1);
  const [datasetPage, setDatasetPage] = useState(1);
  const [userSearch, setUserSearch] = useState("");

  const limit = 5;

  // prevent duplicate calls
  const isFetching = useRef(false);

  const loadDashboard = useCallback(async () => {

    if (isFetching.current) return;
    isFetching.current = true;

    try {
      setLoading(true);
      setError("");

      const [
        dashRes,
        userRes,
        datasetRes,
        forecastRes,
        monthlyRes
      ] = await Promise.all([
        getAdminDashboard(),
        getUsers(userPage, limit, userSearch),
        getDatasets(datasetPage, limit, userSearch),
        getForecasts(),
        getMonthlyAnalytics()
      ]);

      setDashboard(dashRes.data || {});
      setUsers(userRes.data || []);
      setDatasets(datasetRes.data || []);
      setForecasts(forecastRes.data || []);
      setMonthly(monthlyRes.data || []);

    } catch (err) {
      console.error("Dashboard error:", err);
      setError(err?.response?.data?.detail || err?.message || "Failed to load dashboard");

    } finally {
      setLoading(false);
      isFetching.current = false;
    }

  }, [userPage, datasetPage, userSearch]);

  // debounce
  useEffect(() => {
    const delay = setTimeout(() => {
      loadDashboard();
    }, 400);

    return () => clearTimeout(delay);
  }, [loadDashboard]);

  // auto refresh (safe)
  useEffect(() => {
    const interval = setInterval(() => {
      loadDashboard();
    }, 30000);

    return () => clearInterval(interval);
  }, [loadDashboard]);

  return {
    dashboard,
    users,
    datasets,
    forecasts,
    monthly,
    loading,
    error,

    userPage,
    setUserPage,

    datasetPage,
    setDatasetPage,

    userSearch,
    setUserSearch,

    reload: loadDashboard
  };
}