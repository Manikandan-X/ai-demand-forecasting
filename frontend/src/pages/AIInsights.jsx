import { useState } from "react";
import {
  BarChart, Bar, XAxis, YAxis, Tooltip,
  ResponsiveContainer, Cell,
} from "recharts";

import API from "../api/axios";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import { useToast } from "../components/ui/Toast";
import { CardSkeleton } from "../components/ui/LoadingSpinner";
import Table from "../components/ui/Table";

// ── Shared helpers ─────────────────────────

function Section({ title, icon, children }) {
  return (
    <div className="bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-700 rounded-2xl overflow-hidden">
      <div className="flex items-center gap-3 px-6 py-4 border-b border-gray-100 dark:border-slate-800">
        <span className="text-xl">{icon}</span>
        <h2 className="font-bold text-gray-800 dark:text-white text-base">{title}</h2>
      </div>
      <div className="p-6">{children}</div>
    </div>
  );
}

const PRIORITY_STYLE = {
  HIGH:   "bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-300",
  MEDIUM: "bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-300",
  LOW:    "bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300",
};

const SEGMENT_STYLE = {
  HIGH_VALUE: "bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300",
  MID_VALUE:  "bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300",
  LOW_VALUE:  "bg-gray-100 dark:bg-slate-700 text-gray-600 dark:text-slate-300",
};

function Badge({ label, styleMap, fallback = "bg-gray-100 text-gray-600" }) {
  const cls = styleMap?.[label?.toUpperCase()] || fallback;
  return (
    <span className={`px-2.5 py-0.5 rounded-lg text-xs font-semibold ${cls}`}>
      {label}
    </span>
  );
}

// ─────────────────────────────────────────────
export default function AIInsights() {
  const toast = useToast();

  const [datasetId, setDatasetId] = useState("");
  const [loading,   setLoading]   = useState({});

  const [recommendations, setRecommendations] = useState(null);
  const [behavior,        setBehavior]        = useState(null);
  const [spikes,          setSpikes]          = useState(null);
  const [lowStock,        setLowStock]        = useState(null);
  const [inventory,       setInventory]       = useState(null);
  const [generating,      setGenerating]      = useState(false);

  // ── Generic fetch helper ───────────────────
  const fetchSection = async (key, url, setter) => {
    if (!datasetId) { toast("Enter a Dataset ID first", "warning"); return; }
    try {
      setLoading((l) => ({ ...l, [key]: true }));
      const res = await API.get(url);
      setter(res.data);
    } catch (e) {
      toast(e.message || "Failed to load", "error");
    } finally {
      setLoading((l) => ({ ...l, [key]: false }));
    }
  };

  const loadAll = async () => {
    if (!datasetId) { toast("Enter a Dataset ID first", "warning"); return; }
    await Promise.all([
      fetchSection("rec",   `/ai/recommendations/${datasetId}`,      setRecommendations),
      fetchSection("beh",   `/ai/customer-behavior/${datasetId}`,    setBehavior),
      fetchSection("spk",   `/ai/demand-spikes/${datasetId}`,        setSpikes),
      fetchSection("low",   `/ai/low-stock/${datasetId}`,            setLowStock),
      fetchSection("inv",   `/ai/inventory-optimization/${datasetId}`, setInventory),
    ]);
  };

  const generateInsights = async () => {
    if (!datasetId) { toast("Enter a Dataset ID first", "warning"); return; }
    try {
      setGenerating(true);
      const res = await API.post(`/ai/generate/${datasetId}`);
      toast(`${res.data.insights_created} insights generated & saved`, "success");
    } catch (e) {
      toast(e.message || "Generation failed", "error");
    } finally {
      setGenerating(false);
    }
  };

  const isLoading = Object.values(loading).some(Boolean);

  // ── Columns ────────────────────────────────

  const recColumns = [
    { key: "product",        label: "Product",        sortable: true },
    { key: "total_quantity", label: "Total Qty",      sortable: true },
    { key: "recommendation", label: "Recommendation" },
    {
      key: "priority", label: "Priority", sortable: true,
      render: (v) => <Badge label={v} styleMap={PRIORITY_STYLE} />,
    },
  ];

  const behaviorColumns = [
    { key: "customer",       label: "Customer",      sortable: true },
    {
      key: "total_spent", label: "Total Spent", sortable: true,
      render: (v) => `₹${Number(v).toLocaleString()}`,
    },
    { key: "purchase_count", label: "Purchases",     sortable: true },
    {
      key: "segment", label: "Segment",
      render: (v) => <Badge label={v} styleMap={SEGMENT_STYLE} />,
    },
  ];

  const spikeColumns = [
    { key: "product",         label: "Product",        sortable: true },
    {
      key: "average_sales", label: "Avg Sales", sortable: true,
      render: (v) => Number(v).toFixed(2),
    },
    {
      key: "predicted_sales", label: "Predicted", sortable: true,
      render: (v) => Number(v).toFixed(2),
    },
    {
      key: "spike_detected", label: "Spike",
      render: (v) => v
        ? <span className="text-red-500 font-bold">⚠ Yes</span>
        : <span className="text-green-500">✓ No</span>,
    },
  ];

  const lowStockColumns = [
    { key: "product",        label: "Product",    sortable: true },
    { key: "total_quantity", label: "Qty Sold",   sortable: true },
    { key: "recommendation", label: "Recommendation" },
    {
      key: "priority", label: "Risk",
      render: (v) => <Badge label={v} styleMap={PRIORITY_STYLE} />,
    },
  ];

  const inventoryColumns = [
    { key: "product",           label: "Product",             sortable: true },
    {
      key: "recommended_stock", label: "Recommended Stock",   sortable: true,
      render: (v) => <span className="font-semibold text-cyan-600 dark:text-cyan-400">{v}</span>,
    },
  ];

  // ── Spike bar chart data ───────────────────
  const spikeChartData = (spikes?.spikes || []).map((s) => ({
    name:      s.product,
    avg:       parseFloat(s.average_sales)  || 0,
    predicted: parseFloat(s.predicted_sales) || 0,
  }));

  return (
    <div className="flex min-h-screen bg-gray-50 dark:bg-slate-950">
      <Sidebar />

      <div className="flex-1 min-w-0">
        <Navbar />

        <main className="p-4 sm:p-6 lg:p-8 space-y-6">

          {/* ── Header ──────────────────────── */}
          <div className="flex flex-wrap items-start justify-between gap-4">
            <div>
              <h1 className="text-2xl sm:text-3xl font-bold text-gray-800 dark:text-white">
                AI Insights
              </h1>
              <p className="text-sm text-gray-500 dark:text-slate-400 mt-1">
                Demand recommendations, behaviour analysis & inventory optimization
              </p>
            </div>
          </div>

          {/* ── Controls ────────────────────── */}
          <div className="bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-700 rounded-2xl p-5">
            <div className="flex flex-col sm:flex-row gap-3">
              <input
                type="number"
                placeholder="Enter Dataset ID"
                value={datasetId}
                onChange={(e) => setDatasetId(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && loadAll()}
                className="
                  flex-1 px-4 py-2.5 rounded-xl text-sm
                  bg-gray-50 dark:bg-slate-800
                  border border-gray-200 dark:border-slate-700
                  text-gray-800 dark:text-white
                  placeholder-gray-400 dark:placeholder-slate-500
                  focus:outline-none focus:ring-2 focus:ring-cyan-500/40
                "
              />
              <button
                onClick={loadAll}
                disabled={isLoading}
                className="
                  bg-cyan-600 hover:bg-cyan-700
                  text-white px-6 py-2.5 rounded-xl text-sm font-medium
                  transition disabled:opacity-50 whitespace-nowrap
                "
              >
                {isLoading ? "Loading…" : "Load All Insights"}
              </button>
              <button
                onClick={generateInsights}
                disabled={generating}
                className="
                  bg-purple-600 hover:bg-purple-700
                  text-white px-6 py-2.5 rounded-xl text-sm font-medium
                  transition disabled:opacity-50 whitespace-nowrap
                "
              >
                {generating ? "Generating…" : "Generate & Save"}
              </button>
            </div>
          </div>

          {/* ── Empty state ──────────────────── */}
          {!isLoading &&
            !recommendations &&
            !behavior &&
            !spikes &&
            !lowStock &&
            !inventory && (
            <div className="
              bg-white dark:bg-slate-900
              border border-dashed border-gray-300 dark:border-slate-700
              rounded-2xl p-16 text-center
            ">
              <div className="text-5xl mb-4">🧠</div>
              <h3 className="text-lg font-semibold text-gray-700 dark:text-white mb-1">
                No Insights Loaded
              </h3>
              <p className="text-sm text-gray-400 dark:text-slate-500">
                Enter a Dataset ID and click Load All Insights
              </p>
            </div>
          )}

          {/* ────────────────────────────────────
              1. PRODUCT DEMAND RECOMMENDATIONS
          ──────────────────────────────────── */}
          {(loading.rec || recommendations) && (
            <Section title="Product Demand Recommendations" icon="📦">
              {loading.rec ? (
                <div className="grid sm:grid-cols-2 xl:grid-cols-4 gap-4">
                  <CardSkeleton count={4} />
                </div>
              ) : (
                <Table
                  columns={recColumns}
                  data={recommendations?.recommendations || []}
                  emptyText="No recommendations found"
                  rowKey="product"
                />
              )}
            </Section>
          )}

          {/* ────────────────────────────────────
              2. CUSTOMER BUYING BEHAVIOUR
          ──────────────────────────────────── */}
          {(loading.beh || behavior) && (
            <Section title="Customer Buying Behaviour" icon="👥">
              {loading.beh ? (
                <div className="grid sm:grid-cols-2 xl:grid-cols-4 gap-4">
                  <CardSkeleton count={4} />
                </div>
              ) : (
                <>
                  {/* Segment summary chips */}
                  {behavior?.customers?.length > 0 && (
                    <div className="flex flex-wrap gap-3 mb-5">
                      {["HIGH_VALUE", "MID_VALUE", "LOW_VALUE"].map((seg) => {
                        const count = behavior.customers.filter(
                          (c) => c.segment?.toUpperCase() === seg
                        ).length;
                        return (
                          <div key={seg}
                            className="bg-gray-100 dark:bg-slate-800 rounded-xl px-4 py-2 text-sm">
                            <span className="font-semibold text-gray-800 dark:text-white mr-2">
                              {count}
                            </span>
                            <Badge label={seg} styleMap={SEGMENT_STYLE} />
                          </div>
                        );
                      })}
                    </div>
                  )}
                  <Table
                    columns={behaviorColumns}
                    data={behavior?.customers || []}
                    emptyText="No customer data found"
                    rowKey="customer"
                  />
                </>
              )}
            </Section>
          )}

          {/* ────────────────────────────────────
              3. DEMAND SPIKE PREDICTION
          ──────────────────────────────────── */}
          {(loading.spk || spikes) && (
            <Section title="Demand Spike Prediction" icon="📈">
              {loading.spk ? (
                <div className="grid sm:grid-cols-2 xl:grid-cols-4 gap-4">
                  <CardSkeleton count={4} />
                </div>
              ) : (
                <>
                  {/* Spike count summary */}
                  {spikes?.spikes?.length > 0 && (
                    <div className="flex flex-wrap gap-4 mb-5">
                      {[
                        {
                          label: "Spikes Detected",
                          value: spikes.spikes.filter((s) => s.spike_detected).length,
                          color: "text-red-500",
                        },
                        {
                          label: "Products Analysed",
                          value: spikes.spikes.length,
                          color: "text-cyan-500",
                        },
                      ].map((s) => (
                        <div key={s.label}
                          className="bg-gray-100 dark:bg-slate-800 rounded-xl px-5 py-3">
                          <p className={`text-2xl font-bold ${s.color}`}>{s.value}</p>
                          <p className="text-xs text-gray-500 dark:text-slate-400 mt-0.5">{s.label}</p>
                        </div>
                      ))}
                    </div>
                  )}

                  {/* Bar chart */}
                  {spikeChartData.length > 0 && (
                    <div className="mb-6 h-56">
                      <ResponsiveContainer width="100%" height="100%">
                        <BarChart data={spikeChartData} barGap={4}>
                          <XAxis
                            dataKey="name"
                            tick={{ fontSize: 11, fill: "#9ca3af" }}
                            axisLine={false} tickLine={false}
                          />
                          <YAxis
                            tick={{ fontSize: 11, fill: "#9ca3af" }}
                            axisLine={false} tickLine={false}
                          />
                          <Tooltip
                            contentStyle={{
                              background: "#1e293b",
                              border: "1px solid #334155",
                              borderRadius: 10,
                              color: "#f1f5f9",
                              fontSize: 12,
                            }}
                          />
                          <Bar dataKey="avg"       name="Avg Sales"  fill="#60a5fa" radius={[4,4,0,0]} />
                          <Bar dataKey="predicted" name="Predicted"  radius={[4,4,0,0]}>
                            {spikeChartData.map((entry, i) => (
                              <Cell
                                key={i}
                                fill={entry.predicted > entry.avg ? "#f87171" : "#4ade80"}
                              />
                            ))}
                          </Bar>
                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                  )}

                  <Table
                    columns={spikeColumns}
                    data={spikes?.spikes || []}
                    emptyText="No spike data found"
                    rowKey="product"
                  />
                </>
              )}
            </Section>
          )}

          {/* ────────────────────────────────────
              4. LOW-STOCK PREDICTION
          ──────────────────────────────────── */}
          {(loading.low || lowStock) && (
            <Section title="Low-Stock Prediction" icon="⚠️">
              {loading.low ? (
                <div className="grid sm:grid-cols-2 xl:grid-cols-4 gap-4">
                  <CardSkeleton count={4} />
                </div>
              ) : (
                <>
                  {/* High risk count */}
                  {lowStock?.high_risk_products?.length > 0 && (
                    <div className="
                      flex items-center gap-3 mb-5
                      bg-red-50 dark:bg-red-900/20
                      border border-red-200 dark:border-red-800
                      rounded-xl px-5 py-3
                    ">
                      <span className="text-2xl">🚨</span>
                      <div>
                        <p className="font-semibold text-red-700 dark:text-red-300 text-sm">
                          {lowStock.high_risk_products.length} high-risk product(s) need attention
                        </p>
                        <p className="text-xs text-red-500 dark:text-red-400 mt-0.5">
                          These products have HIGH priority — consider restocking soon
                        </p>
                      </div>
                    </div>
                  )}
                  <Table
                    columns={lowStockColumns}
                    data={lowStock?.high_risk_products || []}
                    emptyText="No high-risk products — stock levels look good"
                    rowKey="product"
                  />
                </>
              )}
            </Section>
          )}

          {/* ────────────────────────────────────
              5. INVENTORY OPTIMIZATION
          ──────────────────────────────────── */}
          {(loading.inv || inventory) && (
            <Section title="Inventory Optimization Suggestions" icon="🏭">
              {loading.inv ? (
                <div className="grid sm:grid-cols-2 xl:grid-cols-4 gap-4">
                  <CardSkeleton count={4} />
                </div>
              ) : (
                <Table
                  columns={inventoryColumns}
                  data={inventory?.suggestions || []}
                  emptyText="No optimization suggestions"
                  rowKey="product"
                />
              )}
            </Section>
          )}

        </main>
      </div>
    </div>
  );
}
