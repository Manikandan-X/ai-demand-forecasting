import { Link } from "react-router-dom";

import {
  FaChartLine,
  FaUpload,
  FaFileAlt,
  FaChartBar,
  FaHistory,
  FaUserShield
} from "react-icons/fa";

import { motion } from "framer-motion";

export default function Sidebar() {
  const user = JSON.parse(localStorage.getItem("user"));

  const isAdmin = user?.role === "admin";

  const menuItems = [
    {
      name: "Dashboard",
      path: "/dashboard",
      icon: <FaChartBar />
    },
    {
      name: "Upload Dataset",
      path: "/upload",
      icon: <FaUpload />
    },
    {
      name: "Forecast",
      path: "/forecast",
      icon: <FaChartLine />
    },
    {
      name: "Forecast History",
      path: "/forecast-history",
      icon: <FaHistory />
    },
    {
      name: "Reports",
      path: "/reports",
      icon: <FaFileAlt />
    }
  ];

  const adminMenu = [
    {
      name: "Admin Panel",
      path: "/admin",
      icon: <FaUserShield />
    }
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
        bg-gradient-to-b
        from-slate-950
        via-blue-950
        to-slate-900
        text-white
        p-6
        shadow-2xl
      "
    >
      {/* LOGO */}
      <div className="mb-10">
        <h2 className="text-3xl font-extrabold tracking-wide">
          AI Forecast
        </h2>
        <p className="text-gray-400 text-sm mt-2">
          Smart Analytics Dashboard
        </p>
      </div>

      {/* MAIN MENU */}
      <div className="flex flex-col gap-3">
        <p className="text-gray-400 text-xs uppercase tracking-widest mb-2">
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
              hover:bg-blue-700/40
              transition
              duration-300
              hover:translate-x-1
              text-lg
              font-medium
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
          <p className="text-gray-400 text-xs uppercase tracking-widest mb-2">
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
                hover:bg-red-700/40
                transition
                duration-300
                hover:translate-x-1
                text-lg
                font-medium
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