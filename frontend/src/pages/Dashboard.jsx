import { useState } from "react";

import { Link } from "react-router-dom";

import API from "../api/axios";

import Navbar from "../components/Navbar";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
} from "recharts";

export default function Dashboard() {

  const [datasetId, setDatasetId] =
    useState("");

  const [analytics, setAnalytics] =
    useState(null);

  const [chartData, setChartData] =
    useState([]);

  const handleLoadDashboard =
    async () => {

      try {

        const response = await API.get(
          `/dashboard/${datasetId}`
        );

        setAnalytics(
          response.data.analytics
        );

        const monthlyData =
          Object.entries(
            response.data.analytics
              .monthly_sales
          ).map(
            ([month, sales]) => ({
              month,
              sales,
            })
          );

        setChartData(monthlyData);

      } catch (error) {

        console.error(error);

        alert("Failed to load dashboard");
      }
    };

  return (
    <>
    <Navbar />

    <div className="min-h-screen bg-gray-100 p-8">

      <h1 className="text-3xl font-bold mb-8">
        AI Demand Forecasting Dashboard
      </h1>

      <div className="flex gap-4 mb-8">

        <Link
          to="/upload"
          className="bg-blue-600 text-white px-5 py-3 rounded-lg"
        >
          Upload Dataset
        </Link>

        <Link
          to="/forecast"
          className="bg-green-600 text-white px-5 py-3 rounded-lg"
        >
          Forecast
        </Link>

        <Link
          to="/reports"
          className="bg-red-600 text-white px-5 py-3 rounded-lg"
        >
          Reports
        </Link>

      </div>

      <div className="flex gap-4 mb-8">

        <input
          type="number"
          placeholder="Enter Dataset ID"
          className="border p-3 rounded w-64"
          value={datasetId}
          onChange={(e) =>
            setDatasetId(e.target.value)
          }
        />

        <button
          onClick={handleLoadDashboard}
          className="bg-purple-600 text-white px-6 rounded"
        >
          Load Analytics
        </button>

      </div>

      {analytics && (

        <>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">

            <div className="bg-white p-6 rounded-xl shadow">

              <h2 className="text-lg font-semibold">
                Total Sales
              </h2>

              <p className="text-2xl mt-4">
                ₹{analytics.total_sales}
              </p>

            </div>

            <div className="bg-white p-6 rounded-xl shadow">

              <h2 className="text-lg font-semibold">
                Total Orders
              </h2>

              <p className="text-2xl mt-4">
                {analytics.total_orders}
              </p>

            </div>

            <div className="bg-white p-6 rounded-xl shadow">

              <h2 className="text-lg font-semibold">
                Top Product
              </h2>

              <p className="text-2xl mt-4">

                {
                  Object.keys(
                    analytics.top_products
                  )[0]
                }

              </p>

            </div>

            <div className="bg-white p-6 rounded-xl shadow">

              <h2 className="text-lg font-semibold">
                Product Count
              </h2>

              <p className="text-2xl mt-4">

                {
                  Object.keys(
                    analytics.top_products
                  ).length
                }

              </p>

            </div>

          </div>

          <div className="bg-white p-6 rounded-xl shadow">

            <h2 className="text-2xl font-bold mb-6">
              Monthly Sales Trends
            </h2>

            <div className="h-96">

              <ResponsiveContainer
                width="100%"
                height="100%"
              >

                <BarChart data={chartData}>

                  <CartesianGrid
                    strokeDasharray="3 3"
                  />

                  <XAxis dataKey="month" />

                  <YAxis />

                  <Tooltip />

                  <Bar
                    dataKey="sales"
                    fill="#7c3aed"
                  />

                </BarChart>

              </ResponsiveContainer>

            </div>

          </div>

        </>
      )}

    </div>
  </>
  );
}