import { Link, useNavigate } from "react-router-dom";
import { useState, useEffect, useRef } from "react";

import API from "../api/axios";
import useTheme from "../context/useTheme";

export default function Navbar() {
  const navigate = useNavigate();

  const user = JSON.parse(sessionStorage.getItem("user"));

  const isAdmin = user?.role === "admin";

  const [mobileOpen, setMobileOpen] = useState(false);
  const [open, setOpen] = useState(false);
  const [notifications, setNotifications] = useState([]);
  const [loadingNotifications, setLoadingNotifications] = useState(false);

  const socketRef = useRef(null);

  const { darkMode, toggleTheme } = useTheme();

  // =========================
  // FETCH NOTIFICATIONS
  // =========================
  const fetchNotifications = async () => {
    try {
      setLoadingNotifications(true);

      const response = await API.get("/notifications/");
      setNotifications(response.data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoadingNotifications(false);
    }
  };

  // =========================
  // WEBSOCKET
  // =========================
  useEffect(() => {
    const init = async () => {
      await fetchNotifications();
    };

    init();

    if (!user?.id) return;

    if (socketRef.current) {
      socketRef.current.close();
    }

    const ws = new WebSocket(
      `ws://localhost:8000/ws/notifications/${user.id}`
    );

    socketRef.current = ws;

    ws.onmessage = async (event) => {
      console.log("Realtime Notification:", event.data);
      await fetchNotifications();
    };

    return () => ws.close();
  }, [user?.id]);

  // =========================
  // UNREAD COUNT
  // =========================
  const unreadCount = notifications.filter((n) => !n.is_read).length;

  // =========================
  // MARK AS READ
  // =========================
  const markAsRead = async (id) => {
    try {
      await API.put(`/notifications/${id}/read`);

      setNotifications((prev) =>
        prev.map((n) =>
          n.id === id ? { ...n, is_read: true } : n
        )
      );
    } catch (error) {
      console.error(error);
    }
  };

  const markAllAsRead = async () => {
    try {
      await API.put("/notifications/mark-all/read");

      setNotifications((prev) =>
        prev.map((n) => ({ ...n, is_read: true }))
      );
    } catch (error) {
      console.error(error);
    }
  };

  // =========================
  // LOGOUT
  // =========================
  const handleLogout = () => {
    if (socketRef.current) socketRef.current.close();

    sessionStorage.removeItem("token");
    sessionStorage.removeItem("user");

    navigate("/");
  };

  const userMenus = [
    { name: "Dashboard", path: "/dashboard" },
    { name: "Dataset", path: "/upload" },
    { name: "Forecast", path: "/forecast" },
    { name: "Forecast History", path: "/forecast-history" },
    { name: "Reports", path: "/reports" },
  ];

  return (
    <nav className="
      sticky top-0 z-50

      bg-white text-gray-900
      dark:bg-slate-950 dark:text-white

      border-b border-gray-200 dark:border-slate-800
      shadow-lg
      transition-colors duration-300
    ">
      <div className="px-4 sm:px-6 py-4 flex justify-between items-center">

        {/* LEFT */}
        <div className="flex items-center gap-3">
          <button
            onClick={() => setMobileOpen(!mobileOpen)}
            className="md:hidden text-2xl"
          >
            ☰
          </button>

          <h1 className="text-xl md:text-3xl font-bold">
            AI Forecasting
          </h1>
        </div>

        {/* DESKTOP MENU */}
        <div className="hidden md:flex items-center gap-6">

          {!isAdmin &&
            userMenus.map((item) => (
              <Link
                key={item.name}
                to={item.path}
                className="
                  text-gray-700 dark:text-slate-300
                  hover:text-cyan-500 dark:hover:text-cyan-400
                  transition
                "
              >
                {item.name}
              </Link>
            ))}

          {isAdmin && (
            <Link
              to="/admin"
              className="text-cyan-400 font-semibold"
            >
              Admin Dashboard
            </Link>
          )}

          {/* BELL */}
          <div className="relative">
            <button onClick={() => setOpen(!open)} className="text-3xl relative">
              🔔

              {unreadCount > 0 && (
                <span className="absolute -top-1 -right-1 bg-red-600 text-white text-[10px] rounded-full w-5 h-5 flex items-center justify-center">
                  {unreadCount}
                </span>
              )}
            </button>

            {open && (
              <div className="
                absolute right-0 top-14 w-[320px]
                bg-white dark:bg-slate-900
                border border-gray-200 dark:border-slate-700
                rounded-3xl shadow-xl p-5 z-[999]
              ">
                <div className="flex justify-between items-center mb-4">
                  <h2 className="font-bold">Notifications</h2>

                  {unreadCount > 0 && (
                    <button
                      onClick={markAllAsRead}
                      className="text-cyan-500 text-sm"
                    >
                      Mark All
                    </button>
                  )}
                </div>

                <div className="max-h-72 overflow-y-auto space-y-3">
                  {loadingNotifications && (
                    <p className="text-gray-500">Loading...</p>
                  )}

                  {!loadingNotifications && notifications.length === 0 && (
                    <p className="text-gray-500">No notifications</p>
                  )}

                  {notifications.map((n) => (
                    <div
                      key={n.id}
                      className="
                        bg-gray-100 dark:bg-slate-800
                        rounded-xl p-3
                      "
                    >
                      <p className="text-sm">{n.message}</p>

                      <div className="flex justify-between mt-2">
                        <span className="text-xs text-gray-500">
                          {new Date(n.created_at).toLocaleString()}
                        </span>

                        {!n.is_read && (
                          <button
                            onClick={() => markAsRead(n.id)}
                            className="text-green-500 text-xs"
                          >
                            Read
                          </button>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* THEME TOGGLE */}
          <button
            onClick={toggleTheme}
            className="
              px-4 py-2 rounded-xl
              bg-slate-700 hover:bg-slate-600
              text-white
              transition
            "
          >
            {darkMode ? "☀ Light" : "🌙 Dark"}
          </button>

          {/* LOGOUT */}
          <button
            onClick={handleLogout}
            className="
              px-4 py-2 rounded-xl
              bg-red-600 hover:bg-red-700
              text-white
              transition
            "
          >
            Logout
          </button>
        </div>
      </div>
    </nav>
  );
}