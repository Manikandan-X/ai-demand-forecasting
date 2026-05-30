import { useState } from "react";
import API from "../api/axios";

import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import Loader from "../components/Loader";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
  BarChart,
  Bar,
  Legend,
} from "recharts";

import { motion } from "framer-motion";

export default function Forecast() {
  const [datasetId, setDatasetId] = useState("");
  const [forecastData, setForecastData] = useState([]);
  const [accuracy, setAccuracy] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // NEW STATES
  const [bestModel, setBestModel] = useState("");
  const [modelComparison, setModelComparison] = useState([]);

  const handleForecast = async () => {
    if (!datasetId) {
      alert("Please enter dataset ID");
      return;
    }

    setLoading(true);
    setError("");
    setForecastData([]);
    setAccuracy(null);
    setBestModel("");
    setModelComparison([]);

    try {
      // NORMAL FORECAST
      const response = await API.get(`/forecast/${datasetId}`);
      const forecast = response?.data?.forecast;

      if (!forecast) {
        throw new Error("Invalid response from server");
      }

      setForecastData(forecast?.future_predictions || []);
      setAccuracy(forecast?.forecast_accuracy_mae ?? "N/A");

      // ADVANCED FORECAST
      const advancedResponse = await API.get(`/forecast/advanced/${datasetId}`);
      const comparison = advancedResponse?.data?.model_comparison;

      if (comparison) {
        setBestModel(comparison.best_model?.model);

        setModelComparison([
          {
            model: "Linear Regression",
            accuracy: comparison.linear_regression?.accuracy || 0,
          },
          {
            model: "Prophet",
            accuracy: comparison.prophet?.accuracy || 0,
          },
        ]);
      }
    } catch (err) {
      console.error(err);
      setError("Forecast generation failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      className="
        flex
        min-h-screen
        bg-slate-100
        dark:bg-slate-950
        transition-colors
      "
    >
      <Sidebar />

      <div className="flex-1">
        <Navbar />

        <div className="p-6">

          {/* INPUT */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            className="
              bg-white
              dark:bg-slate-900
              p-6
              rounded-3xl
              shadow-xl
              mb-6
            "
          >
            <div className="flex flex-col md:flex-row gap-4">

              <input
                type="number"
                placeholder="Enter Dataset ID"
                className="
                  flex-1
                  border
                  border-gray-300
                  dark:border-slate-700
                  bg-white
                  dark:bg-slate-800
                  text-gray-900
                  dark:text-white
                  rounded-2xl
                  p-4
                  outline-none
                  focus:ring-2
                  focus:ring-blue-400
                "
                value={datasetId}
                onChange={(e) =>
                  setDatasetId(e.target.value)
                }
              />

              <button
                onClick={handleForecast}
                className="
                  bg-gradient-to-r
                  from-blue-600
                  to-purple-700
                  text-white
                  px-8
                  py-4
                  rounded-2xl
                  shadow-lg
                  hover:scale-105
                  transition
                "
              >
                Generate Forecast
              </button>

            </div>
          </motion.div>

          {/* ERROR */}
          {error && (
            <div
              className="
                bg-red-100
                dark:bg-red-900/30
                text-red-700
                dark:text-red-300
                p-4
                rounded-2xl
                mb-6
              "
            >
              {error}
            </div>
          )}

          {/* LOADING */}
          {loading && <Loader />}

          {/* EMPTY STATE */}
          {!loading &&
            forecastData.length === 0 &&
            !error && (
              <div
                className="
                  text-center
                  text-gray-500
                  dark:text-slate-400
                  mt-10
                "
              >
                No forecast generated yet
              </div>
            )}

          {/* RESULTS */}
          {!loading &&
            forecastData.length > 0 && (
              <>

                {/* MODEL COMPARISON */}
                {modelComparison.length > 0 && (

                  <div
                    className="
                      grid
                      grid-cols-1
                      md:grid-cols-3
                      gap-6
                      mb-10
                    "
                  >

                    {/* BEST MODEL */}
                    <div
                      className="
                        bg-white
                        dark:bg-slate-900
                        rounded-3xl
                        shadow-xl
                        p-6
                      "
                    >
                      <h2
                        className="
                          text-gray-500
                          dark:text-slate-400
                          font-semibold
                          mb-2
                        "
                      >
                        Best Model
                      </h2>

                      <p
                        className="
                          text-3xl
                          font-black
                          text-cyan-700
                          dark:text-cyan-400
                        "
                      >
                        {bestModel}
                      </p>
                    </div>

                    {/* LINEAR */}
                    <div
                      className="
                        bg-white
                        dark:bg-slate-900
                        rounded-3xl
                        shadow-xl
                        p-6
                      "
                    >
                      <h2
                        className="
                          text-gray-500
                          dark:text-slate-400
                          font-semibold
                          mb-2
                        "
                      >
                        Linear Regression
                      </h2>

                      <p
                        className="
                          text-3xl
                          font-black
                          text-blue-700
                          dark:text-blue-400
                        "
                      >
                        {modelComparison[0]?.accuracy}%
                      </p>
                    </div>

                    {/* PROPHET */}
                    <div
                      className="
                        bg-white
                        dark:bg-slate-900
                        rounded-3xl
                        shadow-xl
                        p-6
                      "
                    >
                      <h2
                        className="
                          text-gray-500
                          dark:text-slate-400
                          font-semibold
                          mb-2
                        "
                      >
                        Prophet
                      </h2>

                      <p
                        className="
                          text-3xl
                          font-black
                          text-purple-700
                          dark:text-purple-400
                        "
                      >
                        {modelComparison[1]?.accuracy}%
                      </p>
                    </div>

                  </div>
                )}

                {/* KPI */}
                <motion.div
                  whileHover={{ scale: 1.02 }}
                  className="
                    bg-white
                    dark:bg-slate-900
                    rounded-3xl
                    p-8
                    shadow-xl
                    mb-10
                  "
                >
                  <h2
                    className="
                      text-xl
                      text-gray-500
                      dark:text-slate-400
                      font-semibold
                    "
                  >
                    Forecast Accuracy (MAE)
                  </h2>

                  <p
                    className="
                      text-5xl
                      font-black
                      text-blue-700
                      dark:text-blue-400
                      mt-4
                    "
                  >
                    {accuracy}
                  </p>
                </motion.div>

                {/* CHARTS */}
                <div
                  className="
                    grid
                    grid-cols-1
                    xl:grid-cols-2
                    gap-8
                    mb-10
                  "
                >

                  {/* LINE CHART */}
                  <div
                    className="
                      bg-white
                      dark:bg-slate-900
                      rounded-3xl
                      shadow-xl
                      p-6
                    "
                  >
                    <h2
                      className="
                        text-2xl
                        font-bold
                        mb-6
                        text-gray-900
                        dark:text-white
                      "
                    >
                      Future Sales Trend
                    </h2>

                    <div className="h-96">
                      <ResponsiveContainer
                        width="100%"
                        height="100%"
                      >
                        <LineChart data={forecastData}>
                          <CartesianGrid strokeDasharray="3 3" />
                          <XAxis dataKey="day" />
                          <YAxis />
                          <Tooltip />
                          <Legend />

                          <Line
                            type="monotone"
                            dataKey="predicted_sales"
                            stroke="#2563eb"
                            strokeWidth={4}
                          />
                        </LineChart>
                      </ResponsiveContainer>
                    </div>
                  </div>

                  {/* BAR */}
                  <div
                    className="
                      bg-white
                      dark:bg-slate-900
                      rounded-3xl
                      shadow-xl
                      p-6
                    "
                  >
                    <h2
                      className="
                        text-2xl
                        font-bold
                        mb-6
                        text-gray-900
                        dark:text-white
                      "
                    >
                      Forecast Comparison
                    </h2>

                    <div className="h-96">
                      <ResponsiveContainer
                        width="100%"
                        height="100%"
                      >
                        <BarChart data={forecastData}>
                          <CartesianGrid strokeDasharray="3 3" />
                          <XAxis dataKey="day" />
                          <YAxis />
                          <Tooltip />
                          <Legend />

                          <Bar
                            dataKey="predicted_sales"
                            fill="#8B5CF6"
                            radius={[8, 8, 0, 0]}
                          />
                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                  </div>

                </div>

                {/* MODEL COMPARISON CHART */}
                {modelComparison.length > 0 && (

                  <div
                    className="
                      bg-white
                      dark:bg-slate-900
                      rounded-3xl
                      shadow-xl
                      p-6
                      mb-10
                    "
                  >
                    <h2
                      className="
                        text-2xl
                        font-bold
                        mb-6
                        text-gray-900
                        dark:text-white
                      "
                    >
                      Model Comparison
                    </h2>

                    <div className="h-96">
                      <ResponsiveContainer
                        width="100%"
                        height="100%"
                      >
                        <BarChart data={modelComparison}>
                          <CartesianGrid strokeDasharray="3 3" />
                          <XAxis dataKey="model" />
                          <YAxis />
                          <Tooltip />
                          <Legend />

                          <Bar
                            dataKey="accuracy"
                            fill="#06B6D4"
                            radius={[8, 8, 0, 0]}
                          />
                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                  </div>
                )}

                {/* SUMMARY */}
                <div
                  className="
                    bg-white
                    dark:bg-slate-900
                    rounded-3xl
                    shadow-xl
                    p-6
                  "
                >
                  <h2
                    className="
                      text-2xl
                      font-bold
                      mb-5
                      text-gray-900
                      dark:text-white
                    "
                  >
                    Forecast Summary
                  </h2>

                  <div className="space-y-4">

                    <div
                      className="
                        p-4
                        rounded-2xl
                        bg-blue-100
                        dark:bg-blue-900/30
                        text-gray-900
                        dark:text-white
                      "
                    >
                      Forecast generated successfully
                    </div>

                    <div
                      className="
                        p-4
                        rounded-2xl
                        bg-green-100
                        dark:bg-green-900/30
                        text-gray-900
                        dark:text-white
                      "
                    >
                      Total Predictions:
                      {" "}
                      {forecastData.length}
                    </div>

                    <div
                      className="
                        p-4
                        rounded-2xl
                        bg-purple-100
                        dark:bg-purple-900/30
                        text-gray-900
                        dark:text-white
                      "
                    >
                      Model Accuracy:
                      {" "}
                      {accuracy}
                    </div>

                  </div>
                </div>

              </>
            )}

        </div>
      </div>
    </div>
  )};