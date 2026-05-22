import {
  useEffect,
  useState
} from "react";

import API from "../api/axios";

import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import Loader from "../components/Loader";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line,
  CartesianGrid,
  Legend,
} from "recharts";

export default function AdminDashboard() {

  // =========================
  // STATE
  // =========================
  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState("");

  const [dashboard, setDashboard] =
    useState(null);

  const [analytics, setAnalytics] =
    useState(null);

  const [users, setUsers] =
    useState([]);

  const [datasets, setDatasets] =
    useState([]);

  const [reports, setReports] =
    useState([]);

  const [forecasts, setForecasts] =
    useState([]);

  // =========================
  // LOAD ADMIN DATA
  // =========================
  useEffect(() => {

    const loadAdminData =
      async () => {

        try {

          setLoading(true);

          const [
            dashboardRes,
            analyticsRes,
            usersRes,
            datasetsRes,
            reportsRes,
            forecastsRes,
          ] =
            await Promise.all([
              API.get(
                "/admin/dashboard"
              ),

              API.get(
                "/admin/analytics"
              ),

              API.get(
                "/admin/users"
              ),

              API.get(
                "/admin/datasets"
              ),

              API.get(
                "/admin/reports"
              ),

              API.get(
                "/admin/forecasts"
              ),
            ]);

          setDashboard(
            dashboardRes.data
          );

          setAnalytics(
            analyticsRes.data
          );

          setUsers(
            usersRes.data || []
          );

          setDatasets(
            datasetsRes.data || []
          );

          setReports(
            reportsRes.data || []
          );

          setForecasts(
            forecastsRes.data || []
          );

        } catch (err) {

          console.error(err);

          setError(
            err?.response?.data
              ?.detail ||
              "Failed to load admin dashboard"
          );

        } finally {

          setLoading(false);
        }
      };

    loadAdminData();

  }, []);

  // =========================
  // ACTIONS
  // =========================
  const toggleRole =
    async (user) => {

      try {

        const newRole =
          user.role ===
          "admin"
            ? "user"
            : "admin";

        await API.put(
          `/admin/users/${user.id}/role`,
          {
            role:
              newRole,
          }
        );

        setUsers(
          (prev) =>
            prev.map(
              (u) =>
                u.id ===
                user.id
                  ? {
                      ...u,
                      role:
                        newRole,
                    }
                  : u
            )
        );

      } catch (error) {

        console.error(
          error
        );

        alert(
          "Role update failed"
        );
      }
    };

  const deleteUser =
    async (id) => {

      const confirmDelete =
        window.confirm(
          "Delete this user?"
        );

      if (
        !confirmDelete
      ) return;

      try {

        await API.delete(
          `/admin/users/${id}`
        );

        setUsers(
          (prev) =>
            prev.filter(
              (u) =>
                u.id !==
                id
            )
        );

      } catch (error) {

        console.error(
          error
        );

        alert(
          error
            ?.response
            ?.data
            ?.detail ||
            "Delete failed"
        );
      }
    };

  const deleteDataset =
    async (id) => {

      const confirmDelete =
        window.confirm(
          "Delete this dataset?"
        );

      if (
        !confirmDelete
      ) return;

      try {

        await API.delete(
          `/admin/datasets/${id}`
        );

        setDatasets(
          (prev) =>
            prev.filter(
              (d) =>
                d.id !==
                id
            )
        );

      } catch (error) {

        console.error(
          error
        );

        alert(
          "Delete failed"
        );
      }
    };

  // =========================
  // CHART DATA
  // =========================
  const analyticsData =
    [
      {
        name:
          "Users",
        value:
          analytics?.users ||
          0,
      },

      {
        name:
          "Datasets",
        value:
          analytics?.datasets ||
          0,
      },

      {
        name:
          "Forecasts",
        value:
          analytics?.forecasts ||
          0,
      },
    ];

  const modelCounts =
    forecasts.reduce(
      (
        acc,
        item
      ) => {

        const model =
          item.model_name ||
          "Unknown";

        acc[model] =
          (acc[
            model
          ] || 0) + 1;

        return acc;
      },
      {}
    );

  const forecastChartData =
    Object.entries(
      modelCounts
    ).map(
      ([
        model,
        count,
      ]) => ({
        model,
        count,
      })
    );

  const COLORS =
    [
      "#3b82f6",
      "#10b981",
      "#f59e0b",
      "#ef4444",
    ];

  // =========================
  // LOADING
  // =========================
  if (loading) {

    return (
      <Loader />
    );
  }

  // =========================
  // UI
  // =========================
  return (
        <div className="flex min-h-screen bg-slate-100">

      <Sidebar />

      <div className="flex-1">

        <Navbar />

        <div className="p-8 space-y-8">

          {/* TITLE */}
          <div>
            <h1 className="text-4xl font-bold text-slate-800">
              Admin Dashboard
            </h1>

            <p className="text-slate-500 mt-2">
              Monitor users, datasets,
              forecasting activity,
              reports and analytics
            </p>
          </div>

          {/* ERROR */}
          {error && (
            <div
              className="
              bg-red-100
              text-red-700
              p-4
              rounded-xl
              "
            >
              {error}
            </div>
          )}

          {/* ANALYTICS CARDS */}
          <div
            className="
            grid
            grid-cols-1
            md:grid-cols-4
            gap-6
            "
          >

            <div
              className="
              bg-white
              rounded-3xl
              shadow-lg
              p-6
              "
            >
              <h3 className="text-gray-500">
                Users
              </h3>

              <h2
                className="
                text-4xl
                font-bold
                mt-2
                "
              >
                {analytics?.users}
              </h2>
            </div>

            <div
              className="
              bg-white
              rounded-3xl
              shadow-lg
              p-6
              "
            >
              <h3 className="text-gray-500">
                Datasets
              </h3>

              <h2
                className="
                text-4xl
                font-bold
                mt-2
                "
              >
                {
                  analytics?.datasets
                }
              </h2>
            </div>

            <div
              className="
              bg-white
              rounded-3xl
              shadow-lg
              p-6
              "
            >
              <h3 className="text-gray-500">
                Forecasts
              </h3>

              <h2
                className="
                text-4xl
                font-bold
                mt-2
                "
              >
                {
                  analytics?.forecasts
                }
              </h2>
            </div>

            <div
              className="
              bg-white
              rounded-3xl
              shadow-lg
              p-6
              "
            >
              <h3 className="text-gray-500">
                Avg Accuracy
              </h3>

              <h2
                className="
                text-4xl
                font-bold
                mt-2
                "
              >
                {
                  analytics?.average_accuracy
                }
              </h2>
            </div>

          </div>

          {/* CHARTS */}
          <div
            className="
            grid
            grid-cols-1
            lg:grid-cols-2
            gap-6
            "
          >

            {/* BAR */}
            <div
              className="
              bg-white
              rounded-3xl
              p-6
              shadow-lg
              "
            >

              <h2
                className="
                text-2xl
                font-bold
                mb-6
                "
              >
                System Analytics
              </h2>

              <ResponsiveContainer
                width="100%"
                height={300}
              >
                <BarChart
                  data={
                    analyticsData
                  }
                >
                  <XAxis
                    dataKey="name"
                  />

                  <YAxis />

                  <Tooltip />

                  <Legend />

                  <Bar
                    dataKey="value"
                    fill="#3b82f6"
                  />
                </BarChart>
              </ResponsiveContainer>

            </div>

            {/* PIE */}
            <div
              className="
              bg-white
              rounded-3xl
              p-6
              shadow-lg
              "
            >

              <h2
                className="
                text-2xl
                font-bold
                mb-6
                "
              >
                Forecast Models
              </h2>

              <ResponsiveContainer
                width="100%"
                height={300}
              >
                <PieChart>

                  <Pie
                    data={
                      forecastChartData
                    }
                    dataKey="count"
                    nameKey="model"
                    outerRadius={
                      100
                    }
                  >
                    {forecastChartData.map(
                      (
                        _,
                        index
                      ) => (
                        <Cell
                          key={
                            index
                          }
                          fill={
                            COLORS[
                              index %
                                COLORS.length
                            ]
                          }
                        />
                      )
                    )}
                  </Pie>

                  <Tooltip />

                </PieChart>
              </ResponsiveContainer>

            </div>

          </div>

          {/* USERS */}
          <div
            className="
            bg-white
            rounded-3xl
            shadow-lg
            p-6
            overflow-x-auto
            "
          >

            <h2
              className="
              text-2xl
              font-bold
              mb-4
              "
            >
              Manage Users
            </h2>

            <table className="w-full">

              <thead>
                <tr
                  className="
                  border-b
                  text-left
                  "
                >
                  <th className="py-3">
                    ID
                  </th>

                  <th>
                    Name
                  </th>

                  <th>
                    Email
                  </th>

                  <th>
                    Role
                  </th>

                  <th>
                    Actions
                  </th>
                </tr>
              </thead>

              <tbody>

                {users.map(
                  (user) => (
                    <tr
                      key={
                        user.id
                      }
                      className="
                      border-b
                      "
                    >

                      <td className="py-4">
                        {
                          user.id
                        }
                      </td>

                      <td>
                        {
                          user.name
                        }
                      </td>

                      <td>
                        {
                          user.email
                        }
                      </td>

                      <td>
                        {
                          user.role
                        }
                      </td>

                      <td
                        className="
                        flex
                        gap-2
                        py-4
                        "
                      >

                        <button
                          onClick={() =>
                            toggleRole(
                              user
                            )
                          }
                          className="
                          bg-blue-600
                          text-white
                          px-4
                          py-2
                          rounded-lg
                          "
                        >
                          Toggle Role
                        </button>

                        <button
                          onClick={() =>
                            deleteUser(
                              user.id
                            )
                          }
                          className="
                          bg-red-600
                          text-white
                          px-4
                          py-2
                          rounded-lg
                          "
                        >
                          Delete
                        </button>

                      </td>

                    </tr>
                  )
                )}

              </tbody>

            </table>

          </div>

          {/* DATASETS */}
          <div
            className="
            bg-white
            rounded-3xl
            shadow-lg
            p-6
            "
          >

            <h2
              className="
              text-2xl
              font-bold
              mb-5
              "
            >
              Manage Datasets
            </h2>

            <div className="space-y-4">

              {datasets.map(
                (
                  dataset
                ) => (
                  <div
                    key={
                      dataset.id
                    }
                    className="
                    flex
                    justify-between
                    items-center
                    border
                    rounded-xl
                    p-4
                    "
                  >

                    <div>

                      <p
                        className="
                        font-semibold
                        "
                      >
                        {
                          dataset.filename
                        }
                      </p>

                      <p
                        className="
                        text-sm
                        text-gray-500
                        "
                      >
                        Uploaded:
                        {" "}
                        {new Date(
                          dataset.created_at
                        ).toLocaleString()}
                      </p>

                    </div>

                    <button
                      onClick={() =>
                        deleteDataset(
                          dataset.id
                        )
                      }
                      className="
                      bg-red-600
                      text-white
                      px-4
                      py-2
                      rounded-xl
                      "
                    >
                      Delete
                    </button>

                  </div>
                )
              )}

            </div>

          </div>

          {/* REPORTS */}
          <div
            className="
            bg-white
            rounded-3xl
            shadow-lg
            p-6
            overflow-x-auto
            "
          >

            <h2
              className="
              text-2xl
              font-bold
              mb-5
              "
            >
              Uploaded Reports
            </h2>

            <table className="w-full">

              <thead>
                <tr
                  className="
                  border-b
                  text-left
                  "
                >
                  <th>
                    ID
                  </th>

                  <th>
                    Model
                  </th>

                  <th>
                    Dataset ID
                  </th>

                  <th>
                    Accuracy
                  </th>

                  <th>
                    Created
                  </th>
                </tr>
              </thead>

              <tbody>

                {reports.map(
                  (
                    report
                  ) => (
                    <tr
                      key={
                        report.id
                      }
                      className="
                      border-b
                      "
                    >

                      <td className="py-4">
                        {
                          report.id
                        }
                      </td>

                      <td>
                        {
                          report.model_name
                        }
                      </td>

                      <td>
                        {
                          report.dataset_id
                        }
                      </td>

                      <td>
                        {
                          report.accuracy
                        }
                      </td>

                      <td>
                        {new Date(
                          report.created_at
                        ).toLocaleString()}
                      </td>

                    </tr>
                  )
                )}

              </tbody>

            </table>

          </div>

          {/* FORECAST ACTIVITY */}
          <div
            className="
            bg-white
            rounded-3xl
            shadow-lg
            p-6
            "
          >

            <h2
              className="
              text-2xl
              font-bold
              mb-5
              "
            >
              Forecast Activity
            </h2>

            <div className="space-y-4">

              {forecasts.map(
                (
                  item
                ) => (
                  <div
                    key={
                      item.id
                    }
                    className="
                    border
                    rounded-2xl
                    p-4
                    "
                  >

                    <div
                      className="
                      flex
                      justify-between
                      flex-wrap
                      gap-3
                      "
                    >

                      <div>
                        <p>
                          <strong>
                            Model:
                          </strong>{" "}
                          {
                            item.model_name
                          }
                        </p>

                        <p>
                          <strong>
                            Dataset:
                          </strong>{" "}
                          {
                            item.dataset_id
                          }
                        </p>

                        <p>
                          <strong>
                            Accuracy:
                          </strong>{" "}
                          {
                            item.accuracy
                          }
                        </p>
                      </div>

                      <div>
                        {new Date(
                          item.created_at
                        ).toLocaleString()}
                      </div>

                    </div>

                  </div>
                )
              )}

            </div>

          </div>

        </div>

      </div>

    </div>
  );
}