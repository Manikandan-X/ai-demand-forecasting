import { Link, useLocation } from "react-router-dom";
import { useState } from "react";
import {
  FaChartLine,
  FaUpload,
  FaFileAlt,
  FaChartBar,
  FaHistory,
  FaUserShield,
  FaPlug,
  FaBrain,
  FaTimes,
  FaBars,
} from "react-icons/fa";
import { motion, AnimatePresence } from "framer-motion";
import { FaMicroscope } from "react-icons/fa";

const menuItems = [
  { name: "Dashboard",        path: "/dashboard",        icon: <FaChartBar /> },
  { name: "Upload Dataset",   path: "/upload",            icon: <FaUpload /> },
  { name: "Forecast",         path: "/forecast",          icon: <FaChartLine /> },
  { name: "Forecast History", path: "/forecast-history",  icon: <FaHistory /> },
  { name: "Reports",          path: "/reports",           icon: <FaFileAlt /> },
  { name: "AI Insights",      path: "/ai-insights",       icon: <FaBrain /> },
  { name: "Integrations",     path: "/enterprise-integrations", icon: <FaPlug /> },
  { name: "Forecast Intel", path: "/forecast-intelligence", icon: <FaMicroscope /> },
];

const adminMenu = [
  { name: "Admin Panel", path: "/admin", icon: <FaUserShield /> },
];

function NavItem({ item, active, onClick }) {
  return (
    <Link
      to={item.path}
      onClick={onClick}
      className={`
        flex items-center gap-4 px-5 py-3 rounded-2xl
        transition duration-200
        ${active
          ? "bg-cyan-500/10 text-cyan-600 dark:text-cyan-400 font-semibold"
          : "text-gray-600 dark:text-slate-400 hover:bg-gray-100 dark:hover:bg-slate-800 hover:text-cyan-600 dark:hover:text-cyan-400"
        }
      `}
    >
      <span className={`text-lg ${active ? "text-cyan-500" : ""}`}>
        {item.icon}
      </span>
      <span className="text-sm">{item.name}</span>
      {active && (
        <span className="ml-auto w-1.5 h-1.5 rounded-full bg-cyan-500" />
      )}
    </Link>
  );
}

function SidebarContent({ onClose }) {
  const location = useLocation();
  const user = JSON.parse(sessionStorage.getItem("user") || "{}");
  const isAdmin = user?.role === "super_admin";

  return (
    <div className="flex flex-col h-full">
      {/* Logo */}
      <div className="flex items-center justify-between mb-8 px-1">
        <div>
          <h2 className="text-2xl font-extrabold text-gray-900 dark:text-white tracking-tight">
            AI Forecast
          </h2>
          <p className="text-gray-400 dark:text-slate-500 text-xs mt-1">
            Smart Analytics
          </p>
        </div>
        {/* Close button — mobile only */}
        {onClose && (
          <button
            onClick={onClose}
            className="md:hidden text-gray-400 hover:text-gray-700 dark:hover:text-white text-xl"
          >
            <FaTimes />
          </button>
        )}
      </div>

      {/* User chip */}
      {user?.name && (
        <div className="
          flex items-center gap-3 mb-6
          bg-gray-100 dark:bg-slate-800
          rounded-2xl px-4 py-3
        ">
          <div className="
            w-9 h-9 rounded-full
            bg-cyan-500 text-white
            flex items-center justify-center
            font-bold text-sm flex-shrink-0
          ">
            {user.name.charAt(0).toUpperCase()}
          </div>
          <div className="min-w-0">
            <p className="text-sm font-semibold text-gray-800 dark:text-white truncate">
              {user.name}
            </p>
            <p className="text-xs text-gray-400 dark:text-slate-500 capitalize">
              {user.role}
            </p>
          </div>
        </div>
      )}

      {/* Main menu */}
      <nav className="flex flex-col gap-1 flex-1">
        <p className="text-gray-400 dark:text-slate-600 text-[10px] uppercase tracking-widest mb-2 px-1">
          Main
        </p>
        {menuItems.map((item) => (
          <NavItem
            key={item.path}
            item={item}
            active={location.pathname === item.path}
            onClick={onClose}
          />
        ))}
      </nav>

      {/* Admin section */}
      {isAdmin && (
        <div className="mt-6 flex flex-col gap-1">
          <p className="text-gray-400 dark:text-slate-600 text-[10px] uppercase tracking-widest mb-2 px-1">
            Admin
          </p>
          {adminMenu.map((item) => (
            <Link
              key={item.path}
              to={item.path}
              onClick={onClose}
              className={`
                flex items-center gap-4 px-5 py-3 rounded-2xl
                transition duration-200
                ${location.pathname === item.path
                  ? "bg-red-500/10 text-red-600 dark:text-red-400 font-semibold"
                  : "text-gray-600 dark:text-slate-400 hover:bg-red-50 dark:hover:bg-red-900/20 hover:text-red-600 dark:hover:text-red-400"
                }
              `}
            >
              <span className="text-lg">{item.icon}</span>
              <span className="text-sm">{item.name}</span>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}

export default function Sidebar() {
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <>
      {/* ── Desktop sidebar ────────────────── */}
      <motion.aside
        initial={{ x: -50, opacity: 0 }}
        animate={{ x: 0, opacity: 1 }}
        transition={{ duration: 0.4 }}
        className="
          hidden md:flex flex-col
          w-64 min-h-screen flex-shrink-0
          bg-white dark:bg-slate-950
          border-r border-gray-200 dark:border-slate-800
          p-5 shadow-sm
          transition-colors duration-300
        "
      >
        <SidebarContent />
      </motion.aside>

      {/* ── Mobile hamburger button ─────────── */}
      <button
        onClick={() => setMobileOpen(true)}
        className="
          md:hidden fixed top-4 left-4 z-[700]
          bg-white dark:bg-slate-900
          border border-gray-200 dark:border-slate-700
          rounded-xl p-2.5 shadow-lg
          text-gray-700 dark:text-white
        "
        aria-label="Open menu"
      >
        <FaBars className="text-lg" />
      </button>

      {/* ── Mobile drawer ───────────────────── */}
      <AnimatePresence>
        {mobileOpen && (
          <>
            {/* Backdrop */}
            <motion.div
              key="overlay"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setMobileOpen(false)}
              className="md:hidden fixed inset-0 z-[700] bg-black/50 backdrop-blur-sm"
            />
            {/* Drawer */}
            <motion.div
              key="drawer"
              initial={{ x: "-100%" }}
              animate={{ x: 0 }}
              exit={{ x: "-100%" }}
              transition={{ type: "tween", duration: 0.25 }}
              className="
                md:hidden fixed top-0 left-0 z-[800]
                w-72 h-full
                bg-white dark:bg-slate-950
                border-r border-gray-200 dark:border-slate-800
                p-5 shadow-2xl overflow-y-auto
              "
            >
              <SidebarContent onClose={() => setMobileOpen(false)} />
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </>
  );
}
