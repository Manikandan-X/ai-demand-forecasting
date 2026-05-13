import { useState } from "react";

import API from "../api/axios";

import Navbar from "../components/Navbar";

export default function Reports() {

  const [datasetId, setDatasetId] =
    useState("");

  const handleExcelDownload =
    async () => {

      try {

        const response = await API.get(
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

        alert("Excel Download Failed");
      }
    };

  const handlePDFDownload =
    async () => {

      try {

        const response = await API.get(
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

        alert("PDF Download Failed");
      }
    };

  return (
    <>

    <Navbar />

    <div className="min-h-screen bg-gray-100 p-8">

      <div className="max-w-2xl mx-auto bg-white p-8 rounded-xl shadow">

        <h1 className="text-3xl font-bold mb-8">
          Reports Download
        </h1>

        <input
          type="number"
          placeholder="Enter Dataset ID"
          className="border p-3 rounded w-full mb-6"
          value={datasetId}
          onChange={(e) =>
            setDatasetId(e.target.value)
          }
        />

        <div className="flex gap-4">

          <button
            onClick={handleExcelDownload}
            className="bg-green-600 text-white px-6 py-3 rounded"
          >
            Download Excel
          </button>

          <button
            onClick={handlePDFDownload}
            className="bg-red-600 text-white px-6 py-3 rounded"
          >
            Download PDF
          </button>

        </div>

      </div>

    </div>
    </>
  );
}