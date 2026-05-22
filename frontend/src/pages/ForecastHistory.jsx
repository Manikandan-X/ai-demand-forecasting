import { useEffect, useState } from "react";
import API from "../api/axios";

import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import Loader from "../components/Loader";

export default function ForecastHistory() {
  const [history, setHistory] =
    useState([]);

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState("");

  useEffect(() => {

    const fetchHistory =
      async () => {

        try {

          setLoading(true);

          const response =
            await API.get(
              "/forecast/history"
            );

          setHistory(
            response.data
          );

        } catch (err) {

          console.error(err);

          setError(
            "Failed to load forecast history"
          );

        } finally {

          setLoading(false);
        }
      };

    fetchHistory();

  }, []);

  return (
    <div
      className="
      flex
      min-h-screen
      bg-gradient-to-br
      from-slate-100
      via-blue-50
      to-purple-100
      "
    >
      <Sidebar />

      <div className="flex-1">

        <Navbar />

        <div className="p-6 md:p-10">

          {/* HEADER */}
          <div className="mb-8">

            <h1
              className="
              text-4xl
              font-black
              text-gray-800
              "
            >
              Forecast History
            </h1>

            <p className="text-gray-500 mt-2">
              View all your past
              forecasting activities
            </p>

          </div>

          {/* LOADING */}
          {loading && (
            <Loader />
          )}

          {/* ERROR */}
          {error && (
            <div
              className="
              bg-red-100
              text-red-700
              p-4
              rounded-2xl
              mb-6
              "
            >
              {error}
            </div>
          )}

          {/* EMPTY */}
          {!loading &&
            history.length === 0 && (

            <div
              className="
              bg-white
              rounded-3xl
              shadow-lg
              p-10
              text-center
              text-gray-500
              "
            >
              No forecast history
              available
            </div>
          )}

          {/* HISTORY LIST */}
          {!loading &&
            history.length > 0 && (

            <div
              className="
              grid
              grid-cols-1
              md:grid-cols-2
              xl:grid-cols-3
              gap-6
              "
            >

              {history.map(
                (item) => {

                  const predictions =
                    (() => {

                      try {

                        let result =
                            item.forecast_result;

                        // convert single quotes to double quotes
                        result =
                            result.replace(
                              /'/g,
                              '"'
                            );

                        return JSON.parse(
                          result
                        );

                      } catch (error) {

                        console.error(
                          "Prediction parse error:",
                          error
                        );

                        return [];
                      }

                    })();

                  return (

                    <div
                      key={item.id}

                      className="
                      bg-white/80
                      backdrop-blur-lg
                      rounded-3xl
                      shadow-xl
                      p-6
                      border
                      border-gray-100
                      hover:shadow-2xl
                      transition
                      "
                    >

                      {/* TOP */}
                      <div
                        className="
                        flex
                        justify-between
                        items-start
                        "
                      >

                        <div>

                          <h2
                            className="
                            text-2xl
                            font-bold
                            text-gray-800
                            "
                          >
                            Dataset #
                            {
                              item.dataset_id
                            }
                          </h2>

                          <p
                            className="
                            text-sm
                            text-gray-500
                            mt-1
                            "
                          >
                            {new Date(
                              item.created_at
                            ).toLocaleString()}
                          </p>

                        </div>

                        <span
                          className="
                          bg-blue-100
                          text-blue-700
                          px-4
                          py-2
                          rounded-full
                          text-sm
                          font-semibold
                          "
                        >
                          {item.model}
                        </span>

                      </div>

                      {/* ACCURACY */}
                      <div
                        className="
                        mt-6
                        "
                      >
                        <p
                          className="
                          text-gray-500
                          text-sm
                          "
                        >
                          Accuracy
                        </p>

                        <h3
                          className="
                          text-3xl
                          font-black
                          text-green-600
                          "
                        >
                          {item.accuracy}
                          %
                        </h3>
                      </div>

                      {/* PREDICTIONS */}
                      <div
                        className="
                        mt-6
                        "
                      >

                        <h4
                          className="
                          font-bold
                          text-gray-700
                          mb-3
                          "
                        >
                          Predictions
                        </h4>

                        <div
                          className="
                          max-h-40
                          overflow-y-auto
                          space-y-2
                          "
                        >

                          {predictions
                            .slice(0, 7)
                            .map(
                              (
                                prediction,
                                index
                              ) => (

                                <div
                                  key={
                                    index
                                  }

                                  className="
                                  flex
                                  justify-between
                                  bg-slate-100
                                  p-3
                                  rounded-xl
                                  text-sm
                                  "
                                >

                                  <span>
                                    Day{" "}
                                    {
                                      prediction.day
                                    }
                                  </span>

                                  <span
                                    className="
                                    font-bold
                                    text-blue-700
                                    "
                                  >
                                    ₹
                                    {
                                      prediction.predicted_sales
                                    }
                                  </span>

                                </div>
                              )
                            )}

                        </div>

                      </div>

                    </div>
                  );
                }
              )}

            </div>
          )}

        </div>

      </div>
    </div>
  );
}