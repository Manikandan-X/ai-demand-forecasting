import { Link } from "react-router-dom";

import {
  FaChartLine,
  FaUpload,
  FaFileAlt,
  FaChartBar,
  FaHistory,
  FaUserShield,
} from "react-icons/fa";

import { motion } from "framer-motion";

export default function Sidebar() {
  const user = JSON.parse(sessionStorage.getItem("user"));

  const isAdmin = user?.role === "super_admin";

  const menuItems = [
    {
      name: "Dashboard",
      path: "/dashboard",
      icon: <FaChartBar />,
    },
    {
      name: "Upload Dataset",
      path: "/upload",
      icon: <FaUpload />,
    },
    {
      name: "Forecast",
      path: "/forecast",
      icon: <FaChartLine />,
    },
    {
      name: "Forecast History",
      path: "/forecast-history",
      icon: <FaHistory />,
    },
    {
      name: "Reports",
      path: "/reports",
      icon: <FaFileAlt />,
    },
  ];

  const adminMenu = [
    {
      name: "Admin Panel",
      path: "/admin",
      icon: <FaUserShield />,
    },
  ];

  return (
    <motion.div
      initial={{ x: -50, opacity: 0 }}
      animate={{ x: 0, opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="
        hidden
        md:flex
        flex-col
        w-72
        min-h-screen

        bg-white
        text-gray-900

        dark:bg-slate-950
        dark:text-white

        border-r
        border-gray-200
        dark:border-slate-800

        p-6
        shadow-2xl
        transition-colors
        duration-300
      "
    >
      {/* LOGO */}
      <div className="mb-10">
        <h2 className="text-3xl font-extrabold tracking-wide">
          AI Forecast
        </h2>

        <p className="text-gray-500 dark:text-gray-400 text-sm mt-2">
          Smart Analytics Dashboard
        </p>
      </div>

      {/* MAIN MENU */}
      <div className="flex flex-col gap-3">
        <p className="text-gray-500 dark:text-gray-400 text-xs uppercase tracking-widest mb-2">
          Main
        </p>

        {menuItems.map((item) => (
          <Link
            key={item.name}
            to={item.path}
            className="
              flex
              items-center
              gap-4
              px-5
              py-4
              rounded-2xl

              text-gray-700
              dark:text-slate-300

              hover:bg-gray-100
              dark:hover:bg-slate-800

              hover:text-cyan-600
              dark:hover:text-cyan-400

              transition
              duration-300
              hover:translate-x-1
            "
          >
            <span className="text-xl">{item.icon}</span>
            {item.name}
          </Link>
        ))}
      </div>

      {/* ADMIN SECTION */}
      {isAdmin && (
        <div className="flex flex-col gap-3 mt-10">
          <p className="text-gray-500 dark:text-gray-400 text-xs uppercase tracking-widest mb-2">
            Admin
          </p>

          {adminMenu.map((item) => (
            <Link
              key={item.name}
              to={item.path}
              className="
                flex
                items-center
                gap-4
                px-5
                py-4
                rounded-2xl

                text-gray-700
                dark:text-slate-300

                hover:bg-red-100
                dark:hover:bg-red-900/30

                hover:text-red-600
                dark:hover:text-red-400

                transition
                duration-300
                hover:translate-x-1
              "
            >
              <span className="text-xl">{item.icon}</span>
              {item.name}
            </Link>
          ))}
        </div>
      )}
    </motion.div>
  );
}