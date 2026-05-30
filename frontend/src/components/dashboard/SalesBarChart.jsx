import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid
} from "recharts";

export default function MonthlySalesChart({
  chartData
}) {

  const formatCurrency =
    (value) => {

      return new Intl.NumberFormat(
        "en-IN",
        {
          style: "currency",
          currency: "INR",
          maximumFractionDigits: 0
        }
      ).format(
        value || 0
      );
    };

  if (
    !chartData ||
    chartData.length === 0
  ) {

    return (
      <div
        className="
          bg-white
          rounded-3xl
          shadow-md
          p-8
          text-center
        "
      >
        <h2
          className="
            text-xl
            font-bold
            text-gray-700
          "
        >
          No Sales Data
        </h2>

        <p
          className="
            text-gray-500
            mt-2
          "
        >
          Monthly sales chart
          will appear here
        </p>
      </div>
    );
  }

  return (
    <div
      className="
        bg-white
        rounded-3xl
        shadow-md
        p-6
      "
    >

      <h2
        className="
          text-xl
          font-bold
          mb-5
        "
      >
        Monthly Sales
      </h2>

      <ResponsiveContainer
        width="100%"
        height={320}
      >

        <BarChart
          data={chartData}
        >

          <CartesianGrid
            strokeDasharray="3 3"
          />

          <XAxis
            dataKey="month"
          />

          <YAxis
            tickFormatter={
              (value) =>
                `₹${Math.round(
                  value
                )}`
            }
          />

          <Tooltip
            formatter={
              (value) =>
                [
                  formatCurrency(
                    value
                  ),
                  "Sales"
                ]
            }
          />

          <Bar
            dataKey="sales"
            fill="#7c3aed"
            radius={[
              8,
              8,
              0,
              0
            ]}
            animationDuration={
              1000
            }
          />

        </BarChart>

      </ResponsiveContainer>

    </div>
  );
}