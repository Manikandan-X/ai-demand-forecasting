import { Link, useNavigate } from "react-router-dom";
import { useState,useEffect, useRef } from "react";
import { AnimatePresence, motion } from "framer-motion";

import API from "../api/axios";
import useTheme from "../context/useTheme";
import { useToast } from "./ui/Toast";
import { Spinner } from "./ui/LoadingSpinner";

export default function Navbar() {
  const navigate  = useNavigate();
  const toast     = useToast();
  const { darkMode, toggleTheme } = useTheme();

  const user    = JSON.parse(sessionStorage.getItem("user") || "{}");
  const isAdmin = user?.role === "super_admin";

  const [notifOpen, setNotifOpen]   = useState(false);
  const [notifications, setNotifs]  = useState([]);
  const [notifLoading, setNLoading] = useState(false);

  const socketRef  = useRef(null);
  const notifRef   = useRef(null);

  // ── Close bell dropdown on outside click ─
  useEffect(() => {
    const handler = (e) => {
      if (notifRef.current && !notifRef.current.contains(e.target)) {
        setNotifOpen(false);
      }
    };
    document.addEventListener("mousedown", handler);
    return () => document.removeEventListener("mousedown", handler);
  }, []);

  // ── Fetch notifications ───────────────────
  const fetchNotifs = async () => {
    try {
      setNLoading(true);
      const res = await API.get("/notifications/");
      setNotifs(res.data);
    } catch {
      // silent — navbar shouldn't crash on notif failure
    } finally {
      setNLoading(false);
    }
  };

  // ── WebSocket + initial fetch ─────────────
  useEffect(() => {

  const initialize = async () => {

    await fetchNotifs();

    if (!user?.id) return;

    socketRef.current?.close();

    const ws = new WebSocket(
      `ws://localhost:8000/ws/notifications/${user.id}`
    );

    socketRef.current = ws;

    ws.onmessage = async () => {
      await fetchNotifs();
    };
  };

  initialize();

  return () => {
    socketRef.current?.close();
  };

}, [user?.id]);

  const unread = notifications.filter((n) => !n.is_read).length;

  // ── Mark read ─────────────────────────────
  const markRead = async (id) => {
    try {
      await API.put(`/notifications/${id}/read`);
      setNotifs((prev) =>
        prev.map((n) => (n.id === id ? { ...n, is_read: true } : n))
      );
    } catch { /* silent */ }
  };

  const markAllRead = async () => {
    try {
      await API.put("/notifications/mark-all/read");
      setNotifs((prev) => prev.map((n) => ({ ...n, is_read: true })));
    } catch { /* silent */ }
  };

  // ── Logout ───────────────────────────────
  const handleLogout = () => {
    socketRef.current?.close();
    sessionStorage.removeItem("token");
    sessionStorage.removeItem("user");
    navigate("/");
  };

  return (
    <nav className="
      sticky top-0 z-50
      bg-white dark:bg-slate-950
      border-b border-gray-200 dark:border-slate-800
      shadow-sm transition-colors duration-300
    ">
      <div className="
        px-4 sm:px-6 h-16
        flex items-center justify-between gap-4
      ">

        {/* ── Left: title (desktop) ────────── */}
        <h1 className="
          hidden md:block
          text-xl font-bold text-gray-800 dark:text-white
          tracking-tight
        ">
          AI Forecasting
        </h1>

        {/* ── Spacer on mobile (hamburger is fixed) */}
        <div className="w-10 md:hidden" />

        {/* ── Right actions ────────────────── */}
        <div className="flex items-center gap-2 sm:gap-3 ml-auto">

          {/* Admin badge */}
          {isAdmin && (
            <Link
              to="/admin"
              className="
                hidden sm:flex items-center gap-1.5
                bg-red-500/10 text-red-600 dark:text-red-400
                border border-red-200 dark:border-red-800
                px-3 py-1.5 rounded-xl text-xs font-semibold
                hover:bg-red-500/20 transition
              "
            >
              🛡 Admin
            </Link>
          )}

          {/* Theme toggle */}
          <button
            onClick={toggleTheme}
            title={darkMode ? "Switch to light" : "Switch to dark"}
            className="
              p-2 rounded-xl
              bg-gray-100 dark:bg-slate-800
              text-gray-600 dark:text-slate-300
              hover:bg-gray-200 dark:hover:bg-slate-700
              transition text-lg
            "
          >
            {darkMode ? "☀️" : "🌙"}
          </button>

          {/* Notifications bell */}
          <div ref={notifRef} className="relative">
            <button
              onClick={() => setNotifOpen((o) => !o)}
              className="
                relative p-2 rounded-xl
                bg-gray-100 dark:bg-slate-800
                text-gray-600 dark:text-slate-300
                hover:bg-gray-200 dark:hover:bg-slate-700
                transition text-xl
              "
              aria-label="Notifications"
            >
              🔔
              {unread > 0 && (
                <span className="
                  absolute -top-1 -right-1
                  bg-red-500 text-white
                  text-[9px] font-bold
                  w-4 h-4 rounded-full
                  flex items-center justify-center
                ">
                  {unread > 9 ? "9+" : unread}
                </span>
              )}
            </button>

            {/* Dropdown */}
            <AnimatePresence>
              {notifOpen && (
                <motion.div
                  initial={{ opacity: 0, y: 8, scale: 0.97 }}
                  animate={{ opacity: 1, y: 0, scale: 1 }}
                  exit={{ opacity: 0, y: 8, scale: 0.97 }}
                  transition={{ duration: 0.15 }}
                  className="
                    absolute right-0 top-12
                    w-80 max-h-[420px]
                    bg-white dark:bg-slate-900
                    border border-gray-200 dark:border-slate-700
                    rounded-2xl shadow-2xl
                    flex flex-col z-[999]
                    overflow-hidden
                  "
                >
                  {/* Header */}
                  <div className="
                    flex items-center justify-between
                    px-4 py-3
                    border-b border-gray-100 dark:border-slate-800
                    flex-shrink-0
                  ">
                    <span className="font-semibold text-sm text-gray-800 dark:text-white">
                      Notifications
                      {unread > 0 && (
                        <span className="ml-2 bg-red-500 text-white text-[10px] px-1.5 py-0.5 rounded-full">
                          {unread}
                        </span>
                      )}
                    </span>
                    {unread > 0 && (
                      <button
                        onClick={markAllRead}
                        className="text-cyan-500 text-xs hover:underline"
                      >
                        Mark all read
                      </button>
                    )}
                  </div>

                  {/* List */}
                  <div className="overflow-y-auto flex-1">
                    {notifLoading && (
                      <div className="flex justify-center py-8">
                        <Spinner size="sm" />
                      </div>
                    )}

                    {!notifLoading && notifications.length === 0 && (
                      <div className="text-center py-10 text-gray-400 dark:text-slate-500 text-sm">
                        <div className="text-3xl mb-2">🔕</div>
                        No notifications
                      </div>
                    )}

                    {!notifLoading && notifications.map((n) => (
                      <div
                        key={n.id}
                        className={`
                          px-4 py-3 border-b border-gray-50 dark:border-slate-800
                          transition
                          ${!n.is_read
                            ? "bg-cyan-50/50 dark:bg-cyan-900/10"
                            : "bg-white dark:bg-slate-900"
                          }
                        `}
                      >
                        <p className="text-sm text-gray-700 dark:text-slate-300 leading-snug">
                          {n.message}
                        </p>
                        <div className="flex items-center justify-between mt-1.5">
                          <span className="text-[11px] text-gray-400">
                            {new Date(n.created_at).toLocaleString()}
                          </span>
                          {!n.is_read && (
                            <button
                              onClick={() => markRead(n.id)}
                              className="text-[11px] text-cyan-500 hover:underline"
                            >
                              Mark read
                            </button>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          {/* Logout */}
          <button
            onClick={handleLogout}
            className="
              px-3 sm:px-4 py-2 rounded-xl
              bg-red-500 hover:bg-red-600
              text-white text-sm font-medium
              transition
            "
          >
            <span className="hidden sm:inline">Logout</span>
            <span className="sm:hidden">↩</span>
          </button>
        </div>
      </div>
    </nav>
  );
}
