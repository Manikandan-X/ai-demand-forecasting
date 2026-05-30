import {
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend
} from "recharts";

export default function ProductPieChart({
  productData
}) {

  const COLORS = [
    "#3B82F6",
    "#8B5CF6",
    "#10B981",
    "#F59E0B",
    "#EF4444",
  ];

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
    !productData ||
    productData.length === 0
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
          No Product Data
        </h2>

        <p
          className="
            text-gray-500
            mt-2
          "
        >
          Product distribution
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
        Product Distribution
      </h2>

      <ResponsiveContainer
        width="100%"
        height={320}
      >

        <PieChart>

          <Pie
            data={productData}
            dataKey="value"
            nameKey="name"
            outerRadius={100}
            label
            animationDuration={
              1000
            }
          >

            {productData.map(
              (_, i) => (
                <Cell
                  key={i}
                  fill={
                    COLORS[
                      i %
                      COLORS.length
                    ]
                  }
                />
              )
            )}

          </Pie>

          <Tooltip
            formatter={
              (value) =>
                [
                  formatCurrency(
                    value
                  ),
                  "Revenue"
                ]
            }
          />

          <Legend />

        </PieChart>

      </ResponsiveContainer>

    </div>
  );
}