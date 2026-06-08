import { useState } from "react";
import {
  LineChart, Line, BarChart, Bar,
  XAxis, YAxis, Tooltip, Legend,
  ResponsiveContainer, Cell, RadialBarChart,
  RadialBar,
} from "recharts";

import API from "../api/axios";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import { useToast } from "../components/ui/Toast";
import { CardSkeleton } from "../components/ui/LoadingSpinner";
import Table from "../components/ui/Table";

// ── Shared UI ──────────────────────────────

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

function StatChip({ label, value, color = "cyan" }) {
  const colors = {
    cyan:   "bg-cyan-50 dark:bg-cyan-900/20 text-cyan-700 dark:text-cyan-300",
    green:  "bg-green-50 dark:bg-green-900/20 text-green-700 dark:text-green-300",
    purple: "bg-purple-50 dark:bg-purple-900/20 text-purple-700 dark:text-purple-300",
    red:    "bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-300",
    yellow: "bg-yellow-50 dark:bg-yellow-900/20 text-yellow-700 dark:text-yellow-300",
  };
  return (
    <div className={`rounded-xl px-5 py-3 ${colors[color]}`}>
      <p className="text-2xl font-bold">{value}</p>
      <p className="text-xs mt-0.5 opacity-75">{label}</p>
    </div>
  );
}

const PRIORITY_STYLE = {
  HIGH:   "bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-300",
  MEDIUM: "bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-300",
  LOW:    "bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300",
};

function Badge({ label, styleMap }) {
  const cls = styleMap?.[label?.toUpperCase()] ||
    "bg-gray-100 dark:bg-slate-700 text-gray-600 dark:text-slate-300";
  return (
    <span className={`px-2.5 py-0.5 rounded-lg text-xs font-semibold ${cls}`}>
      {label}
    </span>
  );
}

const CHART_COLORS = ["#22d3ee", "#818cf8", "#34d399", "#fb923c", "#f472b6"];

const tooltipStyle = {
  contentStyle: {
    background: "#1e293b",
    border: "1px solid #334155",
    borderRadius: 10,
    color: "#f1f5f9",
    fontSize: 12,
  },
};

// ─────────────────────────────────────────────
export default function ForecastIntelligence() {
  const toast = useToast();

  const [datasetId, setDatasetId] = useState("");
  const [loading,   setLoading]   = useState({});

  const [dashboard,   setDashboard]   = useState(null);  // /dashboard (all-in-one)
  const [history,     setHistory]     = useState(null);  // /historical-comparison

  const isLoading = Object.values(loading).some(Boolean);

  // ── Fetch helpers ──────────────────────────
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
      fetchSection(
        "dash",
        `/forecast-intelligence/dashboard/${datasetId}`,
        setDashboard
      ),
      fetchSection(
        "hist",
        `/forecast-intelligence/historical-comparison/${datasetId}`,
        setHistory
      ),
    ]);
  };

  // ── Derived data ───────────────────────────

  // Model comparison bar chart
  const comparisonData = (dashboard?.model_comparison || []).map((m) => ({
    name:     m.model_name || m.model || "Model",
    accuracy: parseFloat(m.accuracy || 0).toFixed(2),
  }));

  // Accuracy trends line chart
  const trendsData = (dashboard?.accuracy_trends || []).map((t, i) => ({
    name:     t.model_name || t.label || `Run ${i + 1}`,
    accuracy: parseFloat(t.accuracy || 0).toFixed(2),
  }));

  // Confidence gauge value (0–100)
  const confidenceScore = parseFloat(
    dashboard?.confidence?.confidence_score ||
    dashboard?.confidence?.score ||
    0
  );

  const confidenceColor =
    confidenceScore >= 75 ? "#4ade80" :
    confidenceScore >= 50 ? "#facc15" : "#f87171";

  // Recommendations table
  const recColumns = [
    { key: "title",       label: "Title",      sortable: true },
    { key: "description", label: "Recommendation" },
    {
      key: "priority", label: "Priority", sortable: true,
      render: (v) => <Badge label={v} styleMap={PRIORITY_STYLE} />,
    },
  ];

  // Historical comparison table
  const histColumns = [
    { key: "model",      label: "Model",    sortable: true },
    { key: "dataset_id", label: "Dataset",  sortable: true },
    {
      key: "accuracy", label: "Accuracy", sortable: true,
      render: (v) => (
        <span className="font-semibold text-cyan-600 dark:text-cyan-400">
          {parseFloat(v || 0).toFixed(2)}%
        </span>
      ),
    },
    {
      key: "created_at", label: "Date",
      render: (v) => v ? new Date(v).toLocaleDateString() : "—",
    },
  ];

  const hasData = dashboard || history;

  return (
    <div className="flex min-h-screen bg-gray-50 dark:bg-slate-950">
      <Sidebar />

      <div className="flex-1 min-w-0">
        <Navbar />

        <main className="p-4 sm:p-6 lg:p-8 space-y-6">

          {/* ── Header ──────────────────────── */}
          <div>
            <h1 className="text-2xl sm:text-3xl font-bold text-gray-800 dark:text-white">
              Forecast Intelligence
            </h1>
            <p className="text-sm text-gray-500 dark:text-slate-400 mt-1">
              Model comparison, accuracy trends, confidence scores & business recommendations
            </p>
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
                {isLoading ? "Loading…" : "Load Intelligence"}
              </button>
            </div>
          </div>

          {/* ── Empty state ──────────────────── */}
          {!isLoading && !hasData && (
            <div className="
              bg-white dark:bg-slate-900
              border border-dashed border-gray-300 dark:border-slate-700
              rounded-2xl p-16 text-center
            ">
              <div className="text-5xl mb-4">🔬</div>
              <h3 className="text-lg font-semibold text-gray-700 dark:text-white mb-1">
                No Intelligence Loaded
              </h3>
              <p className="text-sm text-gray-400 dark:text-slate-500">
                Enter a Dataset ID and click Load Intelligence
              </p>
            </div>
          )}

          {/* ────────────────────────────────────
              CONFIDENCE SCORE + SUMMARY CHIPS
          ──────────────────────────────────── */}
          {(loading.dash || dashboard) && (
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">

              {/* Confidence gauge */}
              <Section title="Forecast Confidence" icon="🎯">
                {loading.dash ? (
                  <CardSkeleton count={1} />
                ) : (
                  <div className="flex flex-col items-center">
                    <div className="h-40 w-full">
                      <ResponsiveContainer width="100%" height="100%">
                        <RadialBarChart
                          innerRadius="60%"
                          outerRadius="100%"
                          data={[{ value: confidenceScore, fill: confidenceColor }]}
                          startAngle={180}
                          endAngle={0}
                        >
                          <RadialBar dataKey="value" background={{ fill: "#1e293b" }} />
                        </RadialBarChart>
                      </ResponsiveContainer>
                    </div>
                    <p className="text-4xl font-bold mt-1"
                      style={{ color: confidenceColor }}>
                      {confidenceScore.toFixed(1)}%
                    </p>
                    <p className="text-sm text-gray-500 dark:text-slate-400 mt-1">
                      {confidenceScore >= 75 ? "High confidence" :
                       confidenceScore >= 50 ? "Moderate confidence" : "Low confidence"}
                    </p>
                    {dashboard?.confidence && (
                      <div className="mt-4 w-full space-y-2 text-sm">
                        {Object.entries(dashboard.confidence)
                          .filter(([k]) => k !== "confidence_score" && k !== "score")
                          .map(([k, v]) => (
                            <div key={k} className="flex justify-between
                              text-gray-600 dark:text-slate-400">
                              <span className="capitalize">
                                {k.replace(/_/g, " ")}
                              </span>
                              <span className="font-medium text-gray-800 dark:text-white">
                                {typeof v === "number" ? v.toFixed(2) : String(v)}
                              </span>
                            </div>
                          ))}
                      </div>
                    )}
                  </div>
                )}
              </Section>

              {/* Model summary chips */}
              <div className="lg:col-span-2">
                <Section title="Model Summary" icon="📊">
                  {loading.dash ? (
                    <div className="grid grid-cols-2 gap-4">
                      <CardSkeleton count={4} />
                    </div>
                  ) : (
                    <>
                      <div className="flex flex-wrap gap-3 mb-5">
                        <StatChip
                          label="Models Compared"
                          value={dashboard?.model_comparison?.length || 0}
                          color="cyan"
                        />
                        <StatChip
                          label="Best Accuracy"
                          value={
                            comparisonData.length
                              ? `${Math.max(...comparisonData.map((m) => parseFloat(m.accuracy))).toFixed(1)}%`
                              : "—"
                          }
                          color="green"
                        />
                        <StatChip
                          label="Trend Points"
                          value={trendsData.length}
                          color="purple"
                        />
                        <StatChip
                          label="Recommendations"
                          value={dashboard?.recommendations?.length || 0}
                          color="yellow"
                        />
                      </div>

                      {/* Best model highlight */}
                      {comparisonData.length > 0 && (() => {
                        const best = comparisonData.reduce((a, b) =>
                          parseFloat(a.accuracy) > parseFloat(b.accuracy) ? a : b
                        );
                        return (
                          <div className="
                            flex items-center gap-3
                            bg-cyan-50 dark:bg-cyan-900/20
                            border border-cyan-200 dark:border-cyan-800
                            rounded-xl px-4 py-3
                          ">
                            <span className="text-2xl">🏆</span>
                            <div>
                              <p className="font-semibold text-cyan-700 dark:text-cyan-300 text-sm">
                                Best Model: {best.name}
                              </p>
                              <p className="text-xs text-cyan-600 dark:text-cyan-400 mt-0.5">
                                {best.accuracy}% accuracy
                              </p>
                            </div>
                          </div>
                        );
                      })()}
                    </>
                  )}
                </Section>
              </div>
            </div>
          )}

          {/* ────────────────────────────────────
              MODEL COMPARISON CHART
          ──────────────────────────────────── */}
          {(loading.dash || dashboard) && (
            <Section title="Model Comparison" icon="🤖">
              {loading.dash ? (
                <CardSkeleton count={1} />
              ) : comparisonData.length === 0 ? (
                <p className="text-gray-400 dark:text-slate-500 text-sm text-center py-8">
                  No comparison data available
                </p>
              ) : (
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={comparisonData} barSize={36}>
                      <XAxis
                        dataKey="name"
                        tick={{ fontSize: 12, fill: "#9ca3af" }}
                        axisLine={false} tickLine={false}
                      />
                      <YAxis
                        domain={[0, 100]}
                        tick={{ fontSize: 11, fill: "#9ca3af" }}
                        axisLine={false} tickLine={false}
                        unit="%"
                      />
                      <Tooltip {...tooltipStyle} formatter={(v) => [`${v}%`, "Accuracy"]} />
                      <Bar dataKey="accuracy" name="Accuracy" radius={[6, 6, 0, 0]}>
                        {comparisonData.map((_, i) => (
                          <Cell key={i} fill={CHART_COLORS[i % CHART_COLORS.length]} />
                        ))}
                      </Bar>
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              )}
            </Section>
          )}

          {/* ────────────────────────────────────
              ACCURACY TRENDS CHART
          ──────────────────────────────────── */}
          {(loading.dash || dashboard) && (
            <Section title="Accuracy Trends" icon="📈">
              {loading.dash ? (
                <CardSkeleton count={1} />
              ) : trendsData.length === 0 ? (
                <p className="text-gray-400 dark:text-slate-500 text-sm text-center py-8">
                  No trend data available
                </p>
              ) : (
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={trendsData}>
                      <XAxis
                        dataKey="name"
                        tick={{ fontSize: 11, fill: "#9ca3af" }}
                        axisLine={false} tickLine={false}
                      />
                      <YAxis
                        domain={[0, 100]}
                        tick={{ fontSize: 11, fill: "#9ca3af" }}
                        axisLine={false} tickLine={false}
                        unit="%"
                      />
                      <Tooltip {...tooltipStyle} formatter={(v) => [`${v}%`, "Accuracy"]} />
                      <Line
                        type="monotone"
                        dataKey="accuracy"
                        stroke="#22d3ee"
                        strokeWidth={2.5}
                        dot={{ fill: "#22d3ee", r: 4 }}
                        activeDot={{ r: 6 }}
                      />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              )}
            </Section>
          )}

          {/* ────────────────────────────────────
              BUSINESS RECOMMENDATIONS
          ──────────────────────────────────── */}
          {(loading.dash || dashboard) && (
            <Section title="Business Recommendations" icon="💡">
              {loading.dash ? (
                <CardSkeleton count={1} />
              ) : (
                <Table
                  columns={recColumns}
                  data={dashboard?.recommendations || []}
                  emptyText="No recommendations available"
                  rowKey={(row) => row.title + row.priority}
                />
              )}
            </Section>
          )}

          {/* ────────────────────────────────────
              HISTORICAL COMPARISON
          ──────────────────────────────────── */}
          {(loading.hist || history) && (
            <Section title="Historical Forecast Comparison" icon="🕐">
              {loading.hist ? (
                <CardSkeleton count={1} />
              ) : (
                <>
                  {/* Accuracy distribution mini chart */}
                  {(history?.history || []).length > 0 && (
                    <div className="h-48 mb-6">
                      <ResponsiveContainer width="100%" height="100%">
                        <LineChart
                          data={(history.history || []).map((h, i) => ({
                            name: h.model || `#${i + 1}`,
                            accuracy: parseFloat(h.accuracy || 0).toFixed(2),
                          }))}
                        >
                          <XAxis
                            dataKey="name"
                            tick={{ fontSize: 10, fill: "#9ca3af" }}
                            axisLine={false} tickLine={false}
                          />
                          <YAxis
                            domain={[0, 100]}
                            tick={{ fontSize: 10, fill: "#9ca3af" }}
                            axisLine={false} tickLine={false}
                            unit="%"
                          />
                          <Tooltip
                            {...tooltipStyle}
                            formatter={(v) => [`${v}%`, "Accuracy"]}
                          />
                          <Line
                            type="monotone"
                            dataKey="accuracy"
                            stroke="#818cf8"
                            strokeWidth={2}
                            dot={{ fill: "#818cf8", r: 3 }}
                          />
                        </LineChart>
                      </ResponsiveContainer>
                    </div>
                  )}

                  <Table
                    columns={histColumns}
                    data={history?.history || []}
                    emptyText="No historical forecasts found"
                    rowKey={(row, i) => `${row.model}-${i}`}
                  />
                </>
              )}
            </Section>
          )}

        </main>
      </div>
    </div>
  );
}
