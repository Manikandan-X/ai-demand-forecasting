import {
  FaArrowUp,
  FaArrowDown,
  FaBox,
  FaChartLine,
  FaShoppingCart,
  FaExclamationTriangle
} from "react-icons/fa";

export default function DashboardStats({
  analytics
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

  const topProduct =
    Object.keys(
      analytics?.top_products || {}
    )[0] || "N/A";

  const trendIcon =
    analytics?.trend === "up"
      ? <FaArrowUp />
      : analytics?.trend === "down"
      ? <FaArrowDown />
      : <FaChartLine />;

  const trendText =
    analytics?.trend === "up"
      ? "Sales Increasing"
      : analytics?.trend === "down"
      ? "Sales Decreasing"
      : "Sales Stable";

  const cards = [
    {
      title:
        "Total Sales",

      value:
        formatCurrency(
          analytics?.total_sales
        ),

      icon:
        <FaChartLine />
    },

    {
      title:
        "Total Orders",

      value:
        analytics?.total_orders || 0,

      icon:
        <FaShoppingCart />
    },

    {
      title:
        "Top Product",

      value:
        topProduct,

      icon:
        <FaBox />
    },

    {
      title:
        "Products",

      value:
        Object.keys(
          analytics?.top_products || {}
        ).length,

      icon:
        <FaBox />
    },

    {
      title:
        "Trend",

      value:
        trendText,

      icon:
        trendIcon
    },

    {
      title:
        "Next Forecast",

      value:
        formatCurrency(
          analytics?.forecast_next_month
        ),

      icon:
        <FaChartLine />
    },

    {
      title:
        "Anomalies",

      value:
        analytics?.anomalies?.length || 0,

      icon:
        <FaExclamationTriangle />
    }
  ];

  return (
    <div
      className="
        grid
        grid-cols-1
        sm:grid-cols-2
        md:grid-cols-3
        xl:grid-cols-4
        2xl:grid-cols-7
        gap-6
        mb-10
      "
    >

      {cards.map(
        (
          card,
          index
        ) => (

          <div
            key={index}
            className="
              bg-white
              dark:bg-slate-900
              rounded-3xl
              shadow-md
              hover:shadow-xl
              transition-all
              duration-300
              hover:-translate-y-1
              p-6
            "
          >

            <div
              className="
                flex
                justify-between
                items-start
                mb-4
              "
            >

              <h3
                className="
                  text-gray-500
                  text-sm
                  font-medium
                "
              >
                {card.title}
              </h3>

              <span
                className="
                  text-purple-600
                  text-xl
                "
              >
                {card.icon}
              </span>

            </div>

            <h2
              className="
                text-xl
                md:text-2xl
                font-bold
                text-gray-800
                break-words
              "
            >
              {card.value}
            </h2>

          </div>
        )
      )}

    </div>
  );
}