import {
  useState,
  useEffect,
  useRef,
  useCallback,
} from "react";

import jsPDF from "jspdf";
import html2canvas from "html2canvas";
import { Link } from "react-router-dom";

import API from "../api/axios";
import { useToast } from "../components/ui/Toast";
import { CardSkeleton } from "../components/ui/LoadingSpinner";

import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import DashboardStats from "../components/dashboard/DashboardStats";
import SalesBarChart from "../components/dashboard/SalesBarChart";
import ProductPieChart from "../components/dashboard/ProductPieChart";
import AIInsights from "../components/dashboard/AIInsights";

// ── Reusable filter input ──────────────────
function FilterInput({ className = "", ...props }) {
  return (
    <input
      {...props}
      className={`
        w-full px-3 py-2.5 rounded-xl text-sm
        bg-gray-50 dark:bg-slate-800
        border border-gray-200 dark:border-slate-700
        text-gray-800 dark:text-white
        placeholder-gray-400 dark:placeholder-slate-500
        focus:outline-none focus:ring-2 focus:ring-cyan-500/40
        transition
        ${className}
      `}
    />
  );
}

function FilterSelect({ children, className = "", ...props }) {
  return (
    <select
      {...props}
      className={`
        w-full px-3 py-2.5 rounded-xl text-sm
        bg-gray-50 dark:bg-slate-800
        border border-gray-200 dark:border-slate-700
        text-gray-800 dark:text-white
        focus:outline-none focus:ring-2 focus:ring-cyan-500/40
        transition
        ${className}
      `}
    >
      {children}
    </select>
  );
}

// ── Widget toggle checkbox ─────────────────
function WidgetToggle({ label, checked, onChange }) {
  return (
    <label className="flex items-center gap-2.5 cursor-pointer select-none">
      <div
        onClick={onChange}
        className={`
          w-10 h-6 rounded-full transition-colors duration-200
          flex items-center px-1
          ${checked ? "bg-cyan-500" : "bg-gray-300 dark:bg-slate-600"}
        `}
      >
        <div className={`
          w-4 h-4 rounded-full bg-white shadow
          transition-transform duration-200
          ${checked ? "translate-x-4" : "translate-x-0"}
        `} />
      </div>
      <span className="text-sm text-gray-700 dark:text-slate-300">{label}</span>
    </label>
  );
}

// ─────────────────────────────────────────────
export default function Dashboard() {
  const toast = useToast();

  const [datasetId,       setDatasetId]       = useState("");
  const [analytics,       setAnalytics]       = useState(null);
  const [chartData,       setChartData]       = useState([]);
  const [productData,     setProductData]     = useState([]);
  const [loading,         setLoading]         = useState(false);
  const [exporting,       setExporting]       = useState(false);

  const [globalSearch,    setGlobalSearch]    = useState("");
  const [debouncedSearch, setDebouncedSearch] = useState("");
  const [selectedType,    setSelectedType]    = useState("");
  const [searchResults,   setSearchResults]   = useState([]);
  const [searching,       setSearching]       = useState(false);

  const [selectedRegion,   setSelectedRegion]   = useState("");
  const [selectedCategory, setSelectedCategory] = useState("");
  const [startDate,        setStartDate]         = useState("");
  const [endDate,          setEndDate]           = useState("");
  const [regions,          setRegions]           = useState([]);
  const [categories,       setCategories]        = useState([]);

  const [widgets, setWidgets] = useState(() => {
    try {
      const saved = localStorage.getItem("dashboard_widgets");
      return saved
        ? JSON.parse(saved)
        : { stats: true, salesChart: true, productChart: true, insights: true };
    } catch {
      return { stats: true, salesChart: true, productChart: true, insights: true };
    }
  });

  const dashboardRef = useRef(null);
  const latestRef    = useRef({});

  // ── Persist widgets ───────────────────────
  useEffect(() => {
    localStorage.setItem("dashboard_widgets", JSON.stringify(widgets));
  }, [widgets]);

  // ── Debounce search ───────────────────────
  useEffect(() => {
    const t = setTimeout(() => setDebouncedSearch(globalSearch), 400);
    return () => clearTimeout(t);
  }, [globalSearch]);

  // ── Keep latest filter values in ref ──────
  useEffect(() => {
    latestRef.current = {
      datasetId, selectedRegion, selectedCategory,
      startDate, endDate, selectedType,
    };
  }, [datasetId, selectedRegion, selectedCategory, startDate, endDate, selectedType]);

  // ── Load dashboard ────────────────────────
  const handleLoadDashboard = useCallback(async (overrideId) => {
    const id = overrideId || latestRef.current.datasetId;
    if (!id) {
      toast("Please enter a Dataset ID", "warning");
      return;
    }

    try {
      setLoading(true);

      const params = { id, search: debouncedSearch, type: selectedType };
      if (latestRef.current.selectedRegion)   params.region     = latestRef.current.selectedRegion;
      if (latestRef.current.selectedCategory) params.category   = latestRef.current.selectedCategory;
      if (latestRef.current.startDate)        params.start_date = latestRef.current.startDate;
      if (latestRef.current.endDate)          params.end_date   = latestRef.current.endDate;

      const res = await API.get(`/dashboard/${id}`, { params });

      const data = {
        ...res.data.analytics,
        forecast_confidence:
          res.data?.forecast_confidence?.confidence_score || 0,
      };

      setAnalytics(data);
      setRegions(data.regions || []);
      setCategories(data.categories || []);

      setChartData(
        Object.entries(data.monthly_sales || {}).map(([m, s]) => ({
          month: m, sales: s,
        }))
      );

      setProductData(
        Object.entries(data.top_products || {}).map(([n, v]) => ({
          name: n, value: v,
        }))
      );

      toast("Dashboard loaded", "success");

    } catch (err) {
      toast(err.message || "Failed to load dashboard", "error");
    } finally {
      setLoading(false);
    }
  }, [debouncedSearch, selectedType, toast]);

  // ── Global search ─────────────────────────
  const handleGlobalSearch = async () => {
    if (!globalSearch.trim()) return;
    try {
      setSearching(true);
      const res = await API.get("/dashboard/search", {
        params: { search: globalSearch.trim(), type: selectedType },
      });
      setSearchResults(res.data || []);
    } catch (err) {
      toast(err.message || "Search failed", "error");
    } finally {
      setSearching(false);
    }
  };

  // ── Clear filters ─────────────────────────
  const handleClearFilters = () => {
    setDatasetId("");
    setSelectedRegion("");
    setSelectedCategory("");
    setStartDate("");
    setEndDate("");
    setGlobalSearch("");
    setSearchResults([]);
    setAnalytics(null);
    setChartData([]);
    setProductData([]);
    toast("Filters cleared", "info");
  };

  // ── Export PDF ────────────────────────────
  const exportDashboardPDF = async () => {
    try {
      setExporting(true);
      const canvas   = await html2canvas(dashboardRef.current, { scale: 1.5 });
      const imgData  = canvas.toDataURL("image/png");
      const pdf      = new jsPDF("p", "mm", "a4");
      const width    = pdf.internal.pageSize.getWidth();
      const height   = (canvas.height * width) / canvas.width;
      pdf.addImage(imgData, "PNG", 0, 0, width, height);
      pdf.save(`dashboard-${datasetId || "export"}.pdf`);
      toast("PDF exported", "success");
    } catch {
      toast("Export failed", "error");
    } finally {
      setExporting(false);
    }
  };

  const toggleWidget = (key) =>
    setWidgets((w) => ({ ...w, [key]: !w[key] }));

  return (
    <div className="flex min-h-screen bg-gray-50 dark:bg-slate-950">
      <Sidebar />

      <div className="flex-1 min-w-0">
        <Navbar />

        <main ref={dashboardRef} className="p-4 sm:p-6 lg:p-8 space-y-6">

          {/* ── Page header ─────────────────── */}
          <div className="flex flex-wrap items-start justify-between gap-4">
            <div>
              <h1 className="text-2xl sm:text-3xl font-bold text-gray-800 dark:text-white">
                AI Forecast Dashboard
              </h1>
              <p className="text-sm text-gray-500 dark:text-slate-400 mt-1">
                Smart analytics dashboard
              </p>
            </div>

            <div className="flex flex-wrap gap-2">
              <Link to="/upload"
                className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-xl text-sm font-medium transition">
                Upload
              </Link>
              <Link to="/forecast"
                className="bg-emerald-600 hover:bg-emerald-700 text-white px-4 py-2 rounded-xl text-sm font-medium transition">
                Forecast
              </Link>
              <Link to="/reports"
                className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-xl text-sm font-medium transition">
                Reports
              </Link>
              <button
                onClick={exportDashboardPDF}
                disabled={!analytics || exporting}
                className="
                  bg-purple-600 hover:bg-purple-700
                  text-white px-4 py-2 rounded-xl text-sm font-medium
                  transition disabled:opacity-40 disabled:cursor-not-allowed
                "
              >
                {exporting ? "Exporting…" : "Export PDF"}
              </button>
            </div>
          </div>

          {/* ── Global search ───────────────── */}
          <div className="bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-700 rounded-2xl p-5">
            <h2 className="text-sm font-semibold text-gray-600 dark:text-slate-400 uppercase tracking-wider mb-3">
              Global Search
            </h2>
            <div className="flex flex-col sm:flex-row gap-3">
              <FilterInput
                placeholder="Search datasets, forecasts, reports…"
                value={globalSearch}
                onChange={(e) => setGlobalSearch(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && handleGlobalSearch()}
                className="flex-1"
              />
              <FilterSelect
                value={selectedType}
                onChange={(e) => setSelectedType(e.target.value)}
                className="sm:w-40"
              >
                <option value="">All types</option>
                <option value="dataset">Dataset</option>
                <option value="forecast">Forecast</option>
                <option value="report">Report</option>
                <option value="user">User</option>
              </FilterSelect>
              <button
                onClick={handleGlobalSearch}
                disabled={searching}
                className="
                  bg-blue-600 hover:bg-blue-700
                  text-white px-5 py-2.5 rounded-xl text-sm font-medium
                  transition disabled:opacity-50 whitespace-nowrap
                "
              >
                {searching ? "Searching…" : "Search"}
              </button>
            </div>

            {/* Search results */}
            {searchResults.length > 0 && (
              <div className="mt-4 space-y-2">
                {searchResults.map((item) => (
                  <div
                    key={item.id}
                    className="
                      flex items-center justify-between
                      bg-gray-50 dark:bg-slate-800
                      border border-gray-200 dark:border-slate-700
                      rounded-xl px-4 py-3
                    "
                  >
                    <span className="font-medium text-sm text-gray-800 dark:text-white">
                      {item.name}
                    </span>
                    <span className="text-xs text-gray-400 dark:text-slate-500 capitalize bg-gray-200 dark:bg-slate-700 px-2 py-0.5 rounded-lg">
                      {item.type}
                    </span>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* ── Widget toggles ───────────────── */}
          <div className="bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-700 rounded-2xl p-5">
            <h2 className="text-sm font-semibold text-gray-600 dark:text-slate-400 uppercase tracking-wider mb-4">
              Visible Widgets
            </h2>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
              <WidgetToggle label="KPI Cards"           checked={widgets.stats}        onChange={() => toggleWidget("stats")} />
              <WidgetToggle label="Sales Chart"         checked={widgets.salesChart}   onChange={() => toggleWidget("salesChart")} />
              <WidgetToggle label="Product Distribution" checked={widgets.productChart} onChange={() => toggleWidget("productChart")} />
              <WidgetToggle label="AI Insights"         checked={widgets.insights}     onChange={() => toggleWidget("insights")} />
            </div>
          </div>

          {/* ── Filters ─────────────────────── */}
          <div className="bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-700 rounded-2xl p-5">
            <h2 className="text-sm font-semibold text-gray-600 dark:text-slate-400 uppercase tracking-wider mb-4">
              Filters
            </h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-5 gap-3">
              <FilterInput
                placeholder="Dataset ID"
                value={datasetId}
                onChange={(e) => setDatasetId(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && handleLoadDashboard(datasetId)}
              />
              <FilterSelect value={selectedRegion} onChange={(e) => setSelectedRegion(e.target.value)}>
                <option value="">All Regions</option>
                {regions.map((r, i) => <option key={i}>{r}</option>)}
              </FilterSelect>
              <FilterSelect value={selectedCategory} onChange={(e) => setSelectedCategory(e.target.value)}>
                <option value="">All Categories</option>
                {categories.map((c, i) => <option key={i}>{c}</option>)}
              </FilterSelect>
              <FilterInput
                type="date"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
              />
              <FilterInput
                type="date"
                value={endDate}
                onChange={(e) => setEndDate(e.target.value)}
              />
            </div>

            <div className="flex gap-3 mt-4">
              <button
                onClick={() => handleLoadDashboard(datasetId)}
                disabled={loading}
                className="
                  bg-purple-600 hover:bg-purple-700
                  text-white px-6 py-2.5 rounded-xl text-sm font-medium
                  transition disabled:opacity-50
                "
              >
                {loading ? "Loading…" : "Load Analytics"}
              </button>
              <button
                onClick={handleClearFilters}
                className="
                  bg-gray-200 dark:bg-slate-700
                  hover:bg-gray-300 dark:hover:bg-slate-600
                  text-gray-700 dark:text-white
                  px-5 py-2.5 rounded-xl text-sm font-medium transition
                "
              >
                Clear
              </button>
            </div>
          </div>

          {/* ── Loading skeletons ────────────── */}
          {loading && (
            <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
              <CardSkeleton count={4} />
            </div>
          )}

          {/* ── Empty state ──────────────────── */}
          {!loading && !analytics && (
            <div className="
              bg-white dark:bg-slate-900
              border border-dashed border-gray-300 dark:border-slate-700
              rounded-2xl p-16 text-center
            ">
              <div className="text-5xl mb-4">📊</div>
              <h3 className="text-lg font-semibold text-gray-700 dark:text-white mb-1">
                No Analytics Loaded
              </h3>
              <p className="text-sm text-gray-400 dark:text-slate-500">
                Enter a Dataset ID above and click Load Analytics
              </p>
            </div>
          )}

          {/* ── Dashboard content ────────────── */}
          {!loading && analytics && (
            <div className="space-y-6">
              {widgets.stats && (
                <DashboardStats analytics={analytics} />
              )}

              <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
                {widgets.salesChart && (
                  <SalesBarChart chartData={chartData} />
                )}
                {widgets.productChart && (
                  <ProductPieChart productData={productData} />
                )}
              </div>

              {widgets.insights && (
                <AIInsights analytics={analytics} />
              )}
            </div>
          )}

        </main>
      </div>
    </div>
  );
}
