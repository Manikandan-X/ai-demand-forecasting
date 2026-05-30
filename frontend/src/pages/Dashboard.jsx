import {
  useState,
  useEffect,
  useRef,
  useCallback,
} from "react";

import { Link } from "react-router-dom";
import API from "../api/axios";

import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import SkeletonCard from "../components/SkeletonCard";

import DashboardStats from "../components/dashboard/DashboardStats";
import SalesBarChart from "../components/dashboard/SalesBarChart";
import ProductPieChart from "../components/dashboard/ProductPieChart";
import AIInsights from "../components/dashboard/AIInsights";

export default function Dashboard() {

  const [datasetId, setDatasetId] = useState("");
  const [analytics, setAnalytics] = useState(null);
  const [chartData, setChartData] = useState([]);
  const [productData, setProductData] = useState([]);
  const [loading, setLoading] = useState(false);

  const [globalSearch, setGlobalSearch] = useState("");
  const [debouncedSearch, setDebouncedSearch] = useState("");

  const [selectedType, setSelectedType] = useState("");
  const [searchResults, setSearchResults] = useState([]);

  const [selectedRegion, setSelectedRegion] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");

  const [regions, setRegions] = useState([]);
  const [categories, setCategories] = useState([]);

  const socketRef = useRef(null);

  const latestRef = useRef({
    datasetId: "",
    selectedRegion: "",
    selectedCategory: "",
    startDate: "",
    endDate: "",
  });

  useEffect(() => {
    const t = setTimeout(() => {
      setDebouncedSearch(globalSearch);
    }, 400);

    return () => clearTimeout(t);
  }, [globalSearch]);

  useEffect(() => {
    latestRef.current = {
      datasetId,
      selectedRegion,
      selectedCategory,
      startDate,
      endDate,
      selectedType,
    };
  }, [
    datasetId,
    selectedRegion,
    selectedCategory,
    startDate,
    endDate,
    selectedType,
  ]);
    const handleLoadDashboard = useCallback(async (overrideId) => {

    const id = overrideId || latestRef.current.datasetId;
    if (!id) return;

    try {
      setLoading(true);

      const params = {
        id,
        search: debouncedSearch,
        type: selectedType,
      };

      if (latestRef.current.selectedRegion)
        params.region = latestRef.current.selectedRegion;

      if (latestRef.current.selectedCategory)
        params.category = latestRef.current.selectedCategory;

      if (latestRef.current.startDate)
        params.start_date = latestRef.current.startDate;

      if (latestRef.current.endDate)
        params.end_date = latestRef.current.endDate;

      const res = await API.get(`/dashboard/${id}`, { params });

      const data = res.data.analytics;

      setAnalytics(data);
      setRegions(data.regions || []);
      setCategories(data.categories || []);

      setChartData(
        Object.entries(data.monthly_sales || {}).map(([m, s]) => ({
          month: m,
          sales: s,
        }))
      );

      setProductData(
        Object.entries(data.top_products || {}).map(([n, v]) => ({
          name: n,
          value: v,
        }))
      );

    } catch (err) {
      console.error(err);
      alert("Failed to load dashboard");
    } finally {
      setLoading(false);
    }

  }, [debouncedSearch, selectedType]);

  const handleGlobalSearch = async () => {
    try {
      const res = await API.get("/dashboard/search", {
        params: {
          search: globalSearch.trim(),
          type: selectedType,
        },
      });

      setSearchResults(res.data || []);

    } catch (err) {
      console.error(err);
      alert("Search failed");
    }
  };

  const handleClearFilters = () => {
    setDatasetId("");
    setSelectedRegion("");
    setSelectedCategory("");
    setStartDate("");
    setEndDate("");
    setAnalytics(null);
    setChartData([]);
    setProductData([]);
  };
    return (
    <div className="flex min-h-screen bg-gray-100 dark:bg-slate-950">

      <Sidebar />

      <div className="flex-1">
        <Navbar />

        <div className="p-6 md:p-10">

          {/* HEADER */}
          <div className="flex justify-between flex-wrap gap-4 mb-8">
            <div>
              <h1 className="text-3xl font-bold text-gray-800 dark:text-white">
                AI Forecast Dashboard
              </h1>
              <p className="text-gray-500 dark:text-gray-400">
                Smart analytics dashboard
              </p>
            </div>

            <div className="flex gap-3">
              <Link to="/upload" className="bg-blue-600 text-white px-4 py-2 rounded-xl">
                Upload
              </Link>
              <Link to="/forecast" className="bg-green-600 text-white px-4 py-2 rounded-xl">
                Forecast
              </Link>
              <Link to="/reports" className="bg-red-500 text-white px-4 py-2 rounded-xl">
                Reports
              </Link>
            </div>
          </div>

          {/* GLOBAL SEARCH (FIXED BUTTON) */}
          <div className="mb-6">

            <div className="grid md:grid-cols-2 gap-4">
              <input
                className="p-3 border rounded-xl dark:bg-slate-900 dark:text-white"
                placeholder="Search..."
                value={globalSearch}
                onChange={(e) => setGlobalSearch(e.target.value)}
              />

              <select
                className="p-3 border rounded-xl dark:bg-slate-900 dark:text-white"
                value={selectedType}
                onChange={(e) => setSelectedType(e.target.value)}
              >
                <option value="">All</option>
                <option value="dataset">Dataset</option>
                <option value="forecast">Forecast</option>
                <option value="report">Report</option>
                <option value="user">User</option>
              </select>
            </div>

            {/* ✅ THIS IS YOUR MISSING BUTTON FIX */}
            <button
              onClick={handleGlobalSearch}
              className="mt-4 bg-blue-600 text-white px-6 py-2 rounded-xl hover:bg-blue-700"
            >
              Search
            </button>

          </div>

          {/* SEARCH RESULTS */}
          {searchResults.length > 0 && (
            <div className="bg-white dark:bg-slate-900 p-5 rounded-2xl mb-6">
              <h2 className="font-bold mb-3">Search Results</h2>

              {searchResults.map((item) => (
                <div key={item.id} className="border p-3 rounded-xl mb-2">
                  <p><b>{item.name}</b></p>
                  <p className="text-sm text-gray-500">{item.type}</p>
                </div>
              ))}
            </div>
          )}

          {/* FILTERS */}
          <div className="bg-white dark:bg-slate-900 p-6 rounded-2xl mb-6">

            <div className="grid md:grid-cols-2 xl:grid-cols-5 gap-4">

              <input
                className="p-2 border rounded-xl dark:bg-slate-800 dark:text-white"
                placeholder="Dataset ID"
                value={datasetId}
                onChange={(e) => setDatasetId(e.target.value)}
              />

              <select
                className="p-2 border rounded-xl dark:bg-slate-800 dark:text-white"
                value={selectedRegion}
                onChange={(e) => setSelectedRegion(e.target.value)}
              >
                <option value="">Region</option>
                {regions.map((r, i) => (
                  <option key={i}>{r}</option>
                ))}
              </select>

              <select
                className="p-2 border rounded-xl dark:bg-slate-800 dark:text-white"
                value={selectedCategory}
                onChange={(e) => setSelectedCategory(e.target.value)}
              >
                <option value="">Category</option>
                {categories.map((c, i) => (
                  <option key={i}>{c}</option>
                ))}
              </select>

              <input type="date" className="p-2 border rounded-xl dark:bg-slate-800 dark:text-white"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
              />

              <input type="date" className="p-2 border rounded-xl dark:bg-slate-800 dark:text-white"
                value={endDate}
                onChange={(e) => setEndDate(e.target.value)}
              />

            </div>

            <div className="flex gap-4 mt-4">
              <button
                onClick={() => handleLoadDashboard(datasetId)}
                className="bg-purple-600 text-white px-6 py-2 rounded-xl"
              >
                Load Analytics
              </button>

              <button
                onClick={handleClearFilters}
                className="bg-gray-300 px-4 py-2 rounded-xl"
              >
                Clear
              </button>
            </div>

          </div>

          {/* LOADING */}
          {loading && (
            <div className="grid md:grid-cols-4 gap-6">
              <SkeletonCard />
              <SkeletonCard />
              <SkeletonCard />
              <SkeletonCard />
            </div>
          )}

          {/* EMPTY */}
          {!loading && !analytics && (
            <div className="bg-white dark:bg-slate-900 p-10 rounded-2xl text-center">
              No analytics loaded
            </div>
          )}

          {/* DASHBOARD */}
          {!loading && analytics && (
            <>
              <DashboardStats analytics={analytics} />

              <div className="grid xl:grid-cols-2 gap-6 mt-6">
                <SalesBarChart chartData={chartData} />
                <ProductPieChart productData={productData} />
              </div>

              <div className="mt-6">
                <AIInsights analytics={analytics} />
              </div>
            </>
          )}

        </div>
      </div>
    </div>
  );
}
