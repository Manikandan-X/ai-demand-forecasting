import { useState } from "react";

import API from "../api/axios";

import Navbar from "../components/Navbar";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
} from "recharts";

export default function Forecast() {

  const [datasetId, setDatasetId] =
    useState("");

  const [forecastData, setForecastData] =
    useState([]);

  const [accuracy, setAccuracy] =
    useState(null);

  const [loading, setLoading] =
    useState(false);

  const handleForecast = async () => {

    try {

      setLoading(true);

      const response = await API.get(
        `/forecast/${datasetId}`
      );

      setForecastData(
        response.data.forecast
          .future_predictions
      );

      setAccuracy(
        response.data.forecast
          .forecast_accuracy_mae
      );

      setLoading(false);

    } catch (error) {

      console.error(error);

      setLoading(false);

      alert("Forecast Failed");
    }
  };

  return (
    <>
      <Navbar />

      <div className="min-h-screen bg-gray-100 p-8">

        <div className="max-w-6xl mx-auto bg-white p-8 rounded-2xl shadow">

          <h1 className="text-3xl font-bold mb-8">
            AI Forecast Predictions
          </h1>

          <div className="flex flex-col md:flex-row gap-4 mb-8">

            <input
              type="number"
              placeholder="Enter Dataset ID"
              className="border p-3 rounded-lg w-full md:w-72"
              value={datasetId}
              onChange={(e) =>
                setDatasetId(e.target.value)
              }
            />

            <button
              onClick={handleForecast}
              className="bg-blue-600 text-white px-6 py-3 rounded-lg"
            >
              {
                loading
                  ? "Generating..."
                  : "Generate Forecast"
              }
            </button>

          </div>

          {accuracy !== null && (

            <div className="bg-blue-50 p-4 rounded-xl mb-8">

              <h2 className="text-xl font-semibold">

                Forecast Accuracy (MAE):

                <span className="ml-2 text-blue-700">
                  {accuracy}
                </span>

              </h2>

            </div>
          )}

          {forecastData.length > 0 && (

            <div className="bg-gray-50 p-6 rounded-xl">

              <h2 className="text-2xl font-bold mb-6">
                Future Sales Predictions
              </h2>

              <div className="h-96">

                <ResponsiveContainer
                  width="100%"
                  height="100%"
                >

                  <LineChart data={forecastData}>

                    <CartesianGrid
                      strokeDasharray="3 3"
                    />

                    <XAxis dataKey="day" />

                    <YAxis />

                    <Tooltip />

                    <Line
                      type="monotone"
                      dataKey="predicted_sales"
                      stroke="#2563eb"
                      strokeWidth={3}
                    />

                  </LineChart>

                </ResponsiveContainer>

              </div>

            </div>
          )}

        </div>

      </div>
    </>
  );
}