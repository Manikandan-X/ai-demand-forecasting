import { useState } from "react";

import API from "../api/axios";

import Navbar from "../components/Navbar";

import Loader from "../components/Loader";

export default function Reports() {

  const [datasetId, setDatasetId] =
    useState("");

  const [loading, setLoading] =
    useState(false);

  const handleExcelDownload =
    async () => {

      if (!datasetId) {

        alert("Enter Dataset ID");

        return;
      }

      try {

        setLoading(true);

        const response =
          await API.get(
            `/reports/excel/${datasetId}`,
            {
              responseType: "blob",
            }
          );

        const url =
          window.URL.createObjectURL(
            new Blob([response.data])
          );

        const link =
          document.createElement("a");

        link.href = url;

        link.setAttribute(
          "download",
          `dataset_${datasetId}.xlsx`
        );

        document.body.appendChild(link);

        link.click();

      } catch (error) {

        console.error(error);

        alert(
          "Excel Download Failed"
        );

      } finally {

        setLoading(false);
      }
    };

  const handlePDFDownload =
    async () => {

      if (!datasetId) {

        alert("Enter Dataset ID");

        return;
      }

      try {

        setLoading(true);

        const response =
          await API.get(
            `/reports/pdf/${datasetId}`,
            {
              responseType: "blob",
            }
          );

        const url =
          window.URL.createObjectURL(
            new Blob([response.data])
          );

        const link =
          document.createElement("a");

        link.href = url;

        link.setAttribute(
          "download",
          `dataset_${datasetId}.pdf`
        );

        document.body.appendChild(link);

        link.click();

      } catch (error) {

        console.error(error);

        alert(
          "PDF Download Failed"
        );

      } finally {

        setLoading(false);
      }
    };

  return (

    <>
      <Navbar />

      <div
        className="
        min-h-screen
        bg-gradient-to-br
        from-slate-100
        via-blue-50
        to-purple-100
        p-6
        md:p-10
        "
      >

        <div
          className="
          max-w-6xl
          mx-auto
          "
        >

          {/* TITLE */}
          <div className="mb-10">

            <h1
              className="
              text-4xl
              font-extrabold
              text-slate-800
              mb-3
              "
            >
              Reports Center
            </h1>

            <p
              className="
              text-gray-600
              text-lg
              "
            >
              Download forecasting
              reports in Excel
              and PDF format.
            </p>

          </div>

          {/* INPUT CARD */}
          <div
            className="
            bg-white/70
            backdrop-blur-lg
            shadow-xl
            rounded-3xl
            p-8
            mb-10
            border
            border-white
            "
          >

            <h2
              className="
              text-2xl
              font-bold
              mb-6
              text-slate-800
              "
            >
              Generate Report
            </h2>

            <input
              type="number"
              placeholder="Enter Dataset ID"
              className="
              w-full
              border
              border-gray-300
              rounded-2xl
              p-4
              text-lg
              outline-none
              focus:ring-4
              focus:ring-blue-300
              transition
              "
              value={datasetId}
              onChange={(e) =>
                setDatasetId(
                  e.target.value
                )
              }
            />

          </div>

          {/* REPORT CARDS */}
          <div
            className="
            grid
            grid-cols-1
            md:grid-cols-2
            gap-8
            mb-10
            "
          >

            {/* EXCEL */}
            <div
              className="
              bg-gradient-to-r
              from-green-500
              to-emerald-600
              text-white
              rounded-3xl
              p-8
              shadow-xl
              hover:scale-105
              transition
              duration-300
              "
            >

              <div className="text-5xl mb-4">
                📊
              </div>

              <h2
                className="
                text-3xl
                font-bold
                mb-3
                "
              >
                Excel Report
              </h2>

              <p className="mb-6">
                Download detailed
                spreadsheet analytics
                report.
              </p>

              <button
                onClick={
                  handleExcelDownload
                }
                className="
                bg-white
                text-green-700
                px-6
                py-3
                rounded-xl
                font-bold
                hover:scale-105
                transition
                "
              >
                Download Excel
              </button>

            </div>

            {/* PDF */}
            <div
              className="
              bg-gradient-to-r
              from-red-500
              to-pink-600
              text-white
              rounded-3xl
              p-8
              shadow-xl
              hover:scale-105
              transition
              duration-300
              "
            >

              <div className="text-5xl mb-4">
                📄
              </div>

              <h2
                className="
                text-3xl
                font-bold
                mb-3
                "
              >
                PDF Report
              </h2>

              <p className="mb-6">
                Download clean
                printable forecasting
                report.
              </p>

              <button
                onClick={
                  handlePDFDownload
                }
                className="
                bg-white
                text-red-700
                px-6
                py-3
                rounded-xl
                font-bold
                hover:scale-105
                transition
                "
              >
                Download PDF
              </button>

            </div>

          </div>

          {/* SUMMARY SECTION */}
          <div
            className="
            bg-white
            rounded-3xl
            p-8
            shadow-xl
            "
          >

            <h2
              className="
              text-2xl
              font-bold
              mb-6
              "
            >
              Report Features
            </h2>

            <div
              className="
              grid
              grid-cols-1
              md:grid-cols-3
              gap-6
              "
            >

              <div
                className="
                bg-blue-50
                rounded-2xl
                p-6
                "
              >
                <h3
                  className="
                  font-bold
                  text-xl
                  mb-2
                  "
                >
                  Forecast Summary
                </h3>

                <p>
                  Export demand
                  forecasting
                  analytics.
                </p>
              </div>

              <div
                className="
                bg-green-50
                rounded-2xl
                p-6
                "
              >
                <h3
                  className="
                  font-bold
                  text-xl
                  mb-2
                  "
                >
                  Business Reports
                </h3>

                <p>
                  Generate detailed
                  Excel analytics.
                </p>
              </div>

              <div
                className="
                bg-red-50
                rounded-2xl
                p-6
                "
              >
                <h3
                  className="
                  font-bold
                  text-xl
                  mb-2
                  "
                >
                  Printable PDF
                </h3>

                <p>
                  Download ready-to-use
                  PDF reports.
                </p>
              </div>

            </div>

          </div>

          {loading && <Loader />}

        </div>

      </div>
    </>
  );
}