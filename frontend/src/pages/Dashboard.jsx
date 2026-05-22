import { useState } from "react";
import { Link } from "react-router-dom";

import API from "../api/axios";

import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import SkeletonCard from "../components/SkeletonCard";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  AreaChart,
  Area,
  Legend,
} from "recharts";

import { motion } from "framer-motion";

export default function Dashboard() {
  // =========================
  // STATE
  // =========================
  const [datasetId, setDatasetId] = useState("");

  const [analytics, setAnalytics] = useState(null);
  const [chartData, setChartData] = useState([]);
  const [productData, setProductData] = useState([]);

  const [loading, setLoading] = useState(false);

  // FILTERS
  const [selectedRegion, setSelectedRegion] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");

  // DROPDOWN DATA
  const [regions, setRegions] = useState([]);
  const [categories, setCategories] = useState([]);

  // =========================
  // LOAD DASHBOARD (FIXED)
  // =========================
  const handleLoadDashboard = async () => {
    if (!datasetId) {
      alert("Please enter dataset ID");
      return;
    }

    try {
      setLoading(true);

      // ✅ SAFE PARAMS OBJECT (FIXED)
      const params = {
        id: datasetId,
      };

      if (selectedRegion) {
        params.region = selectedRegion;
      }

      if (selectedCategory) {
        params.category = selectedCategory;
      }

      if (startDate) {
        params.start_date = startDate;
      }

      if (endDate) {
        params.end_date = endDate;
      }

      const response = await API.get(`/dashboard/${datasetId}`, {
        params,
      });

      const analyticsData = response.data.analytics;

      setAnalytics(analyticsData);

      // dropdown options
      setRegions(analyticsData.regions || []);
      setCategories(analyticsData.categories || []);

      // monthly chart
      setChartData(
        Object.entries(analyticsData.monthly_sales || {}).map(
          ([month, sales]) => ({
            month,
            sales,
          })
        )
      );

      // product chart
      setProductData(
        Object.entries(analyticsData.top_products || {}).map(
          ([name, value]) => ({
            name,
            value,
          })
        )
      );

        } catch (error) {
    console.error(error);
    alert("Failed to load dashboard");
  } finally {
    setLoading(false);
  }
};

const pieColors = [
  "#3B82F6",
  "#8B5CF6",
  "#10B981",
  "#F59E0B",
  "#EF4444",
];

return (
  <div className="flex min-h-screen bg-gradient-to-br from-slate-100 via-blue-50 to-purple-100">
    <Sidebar />

    <div className="flex-1">
      <Navbar />

      <div className="p-6 md:p-10">

        {/* HEADER */}
        <div className="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-6 mb-8">
          <div>
            <h1 className="text-4xl font-black text-gray-800">
              AI Forecast Dashboard
            </h1>
            <p className="text-gray-500 mt-2">
              Filters: ID + Region + Category + Date Range
            </p>
          </div>

          <div className="flex gap-3 flex-wrap">
            <Link to="/upload" className="bg-blue-600 text-white px-5 py-3 rounded-2xl">
              Upload
            </Link>
            <Link to="/forecast" className="bg-green-600 text-white px-5 py-3 rounded-2xl">
              Forecast
            </Link>
            <Link to="/reports" className="bg-red-500 text-white px-5 py-3 rounded-2xl">
              Reports
            </Link>
          </div>
        </div>
      </div>
      
        {/* FILTER PANEL */}
        <div className="bg-white/70 backdrop-blur-lg p-6 rounded-3xl shadow mb-8">
          <div className="grid grid-cols-1 md:grid-cols-5 gap-4">

            <input
              type="number"
              placeholder="Dataset ID"
              value={datasetId}
              onChange={(e) => setDatasetId(e.target.value)}
              className="border p-3 rounded-xl"
            />

            
              <select
                value={selectedRegion}
                onChange={(e) => setSelectedRegion(e.target.value)}
                className="border p-3 rounded-xl"
              >
                <option value="">All Regions</option>

                {regions.length > 0 ? (
                  regions.map((r, i) => (
                    <option key={i} value={r}>
                      {r}
                    </option>
                  ))
                ) : (
                  <option value="" disabled>
                    No regions available
                  </option>
                )}
              </select>
              

            
              <select
                value={selectedCategory}
                onChange={(e) => setSelectedCategory(e.target.value)}
                className="border p-3 rounded-xl"
              >
                <option value="">All Categories</option>

                {categories.length > 0 ? (
                  categories.map((c, i) => (
                    <option key={i} value={c}>
                      {c}
                    </option>
                  ))
                ) : (
                  <option value="" disabled>
                    No categories available
                  </option>
                )}
              </select>
            

        {/* START DATE */}
        <div className="flex flex-col">
          <label className="text-sm font-semibold text-gray-600 mb-1">
            Start Date
          </label>

          <input
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
            className="border p-3 rounded-xl"
          />
        </div>

        {/* END DATE */}
        <div className="flex flex-col">
          <label className="text-sm font-semibold text-gray-600 mb-1">
            End Date
          </label>

          <input
            type="date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
            className="border p-3 rounded-xl"
          />
        </div>

          <div className="mt-4">
            <button
              onClick={handleLoadDashboard}
              className="bg-purple-600 text-white px-8 py-3 rounded-2xl"
            >
              Load Analytics
            </button>
          </div>
        </div>

        {/* LOADING */}
        {loading && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <SkeletonCard />
            <SkeletonCard />
            <SkeletonCard />
            <SkeletonCard />
          </div>
        )}

        {/* ANALYTICS */}
        {!loading && analytics && (
          <>
            {/* KPI */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-10">
              <div className="bg-white p-6 rounded-3xl shadow">
                <h2>Total Sales</h2>
                <p className="text-2xl font-bold">₹{analytics.total_sales}</p>
              </div>

              <div className="bg-white p-6 rounded-3xl shadow">
                <h2>Total Orders</h2>
                <p className="text-2xl font-bold">{analytics.total_orders}</p>
              </div>

              <div className="bg-white p-6 rounded-3xl shadow">
                <h2>Top Product</h2>
                <p className="text-2xl font-bold">
                  {Object.keys(analytics.top_products || {})[0]}
                </p>
              </div>

              <div className="bg-white p-6 rounded-3xl shadow">
                <h2>Products</h2>
                <p className="text-2xl font-bold">
                  {Object.keys(analytics.top_products || {}).length}
                </p>
              </div>
            </div>

            {/* BAR + PIE */}
            <div className="grid grid-cols-1 xl:grid-cols-2 gap-8 mb-10">
              <div className="bg-white p-6 rounded-3xl shadow">
                <h2 className="text-xl font-bold mb-4">Monthly Sales</h2>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="month" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="sales" fill="#7c3aed" />
                  </BarChart>
                </ResponsiveContainer>
              </div>

              <div className="bg-white p-6 rounded-3xl shadow">
                <h2 className="text-xl font-bold mb-4">Product Distribution</h2>
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={productData}
                      dataKey="value"
                      nameKey="name"
                      outerRadius={100}
                      label
                    >
                      {productData.map((_, i) => (
                        <Cell key={i} fill={pieColors[i % pieColors.length]} />
                      ))}
                    </Pie>
                    <Tooltip />
                    <Legend />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            </div>
          </>
        )}

      </div>
    </div>
  </div>
);
}
