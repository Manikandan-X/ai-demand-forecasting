export default function AIInsights({ analytics }) {
  if (!analytics) {
    return (
      <div className="bg-white p-6 rounded-3xl shadow mt-8 text-center">
        <h2 className="text-xl font-bold text-gray-700">
          No Insights Available
        </h2>
        <p className="text-gray-500 mt-2">
          Load analytics to generate AI insights
        </p>
      </div>
    );
  }

  const trend = analytics?.trend;

  const trendText =
    trend === "up"
      ? "📈 Sales trend increasing"
      : trend === "down"
      ? "📉 Sales trend decreasing"
      : "➡ Sales trend stable";

  const forecast = analytics?.forecast_next_month
    ? Math.round(analytics.forecast_next_month)
    : 0;

  const anomalyCount = analytics?.anomalies?.length || 0;

  return (
    <div className="bg-white p-6 rounded-3xl shadow mt-8">
      
      <h2 className="text-2xl font-bold mb-4">
        AI Insights
      </h2>

      <div className="space-y-4 text-gray-700">

        {/* TREND */}
        <p>
          Trend:{" "}
          <span className="font-semibold">
            {trendText}
          </span>
        </p>

        {/* FORECAST */}
        <p>
          Forecast:{" "}
          <span className="font-semibold">
            Expected next sales: ₹{forecast}
          </span>
        </p>

        {/* ANOMALY SUMMARY */}
        <p>
          Anomaly Detection:{" "}
          <span className="font-semibold">
            {anomalyCount} unusual month(s) detected
          </span>
        </p>

        {/* ANOMALY DETAILS */}
        {anomalyCount > 0 && (
          <div className="mt-4">
            
            <h3 className="font-semibold mb-2">
              Unusual Months
            </h3>

            <div className="space-y-2">
              {analytics.anomalies.map((item, index) => (
                <div
                  key={index}
                  className="bg-red-50 border border-red-200 rounded-xl p-3"
                >
                  <p>
                    <strong>Month:</strong> {item.month}
                  </p>

                  <p>
                    <strong>Sales:</strong> ₹
                    {Math.round(item.sales)}
                  </p>
                </div>
              ))}
            </div>

          </div>
        )}

      </div>
    </div>
  );
}