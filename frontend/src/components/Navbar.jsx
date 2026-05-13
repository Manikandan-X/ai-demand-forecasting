import { Link, useNavigate }
from "react-router-dom";

export default function Navbar() {

  const navigate = useNavigate();

  const handleLogout = () => {

    localStorage.removeItem("token");

    navigate("/");
  };

  return (

    <nav className="bg-white shadow p-4 mb-8">

      <div className="max-w-7xl mx-auto flex justify-between items-center">

        <h1 className="text-2xl font-bold text-blue-600">
          AI Forecasting
        </h1>

        <div className="flex gap-4">

          <Link
            to="/dashboard"
            className="text-gray-700"
          >
            Dashboard
          </Link>

          <Link
            to="/upload"
            className="text-gray-700"
          >
            Upload
          </Link>

          <Link
            to="/forecast"
            className="text-gray-700"
          >
            Forecast
          </Link>

          <Link
            to="/reports"
            className="text-gray-700"
          >
            Reports
          </Link>

          <button
            onClick={handleLogout}
            className="bg-red-600 text-white px-4 py-2 rounded"
          >
            Logout
          </button>

        </div>

      </div>

    </nav>
  );
}