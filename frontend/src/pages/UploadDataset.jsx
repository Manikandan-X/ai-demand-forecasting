import { useState } from "react";
import API from "../api/axios";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import Loader from "../components/Loader";

export default function UploadDataset() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async (e) => {
    e.preventDefault();

    if (!file) {
      alert("Please select a file");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoading(true);

      const response = await API.post("/dataset/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      setResult(response.data);
      alert("Dataset Uploaded");
    } catch (error) {
      console.error(error);
      alert("Upload Failed");
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
      dark:bg-gradient-to-br
      dark:from-slate-950
      dark:via-slate-900
      dark:to-blue-950
      transition-colors
      duration-300
      "
    >
      <Sidebar />

      <div className="flex-1">
        <Navbar />

        <div className="p-6 md:p-10">
          <div className="max-w-6xl mx-auto">

            {/* TITLE */}
            <div className="mb-10">
              <h1 className="text-4xl font-extrabold text-slate-800 dark:text-white mb-3">
                Upload Dataset
              </h1>

              <p className="text-gray-600 dark:text-gray-300 text-lg">
                Upload CSV or Excel datasets for AI forecasting.
              </p>
            </div>

            {/* MAIN CARD */}
            <div
              className="
              bg-white
              dark:bg-slate-900/70
              backdrop-blur-lg
              shadow-xl
              rounded-3xl
              p-8
              border
              border-gray-200
              dark:border-slate-700
              mb-10
              "
            >
              {/* FORM */}
              <form onSubmit={handleUpload} className="mb-8">
                <div className="flex flex-col lg:flex-row gap-5">

                  <input
                    type="file"
                    accept=".csv,.xlsx"
                    onChange={(e) => setFile(e.target.files[0])}
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
                    px-5
                    py-4
                    outline-none
                    focus:ring-4
                    focus:ring-blue-300
                    transition
                    "
                  />

                  <button
                    type="submit"
                    className="
                    px-8
                    py-4
                    rounded-2xl
                    font-semibold
                    bg-gradient-to-r
                    from-blue-600
                    to-purple-600
                    text-white
                    hover:scale-105
                    transition
                    duration-300
                    shadow-lg
                    "
                  >
                    {loading ? "Uploading..." : "Upload Dataset"}
                  </button>

                </div>
              </form>

              {/* FILE SELECTED */}
              {file && (
                <div
                  className="
                  bg-blue-50
                  dark:bg-slate-800
                  border
                  border-blue-200
                  dark:border-slate-700
                  rounded-2xl
                  p-5
                  mb-8
                  "
                >
                  <h3 className="font-bold text-lg mb-2 text-slate-800 dark:text-white">
                    Selected File
                  </h3>

                  <p className="text-gray-600 dark:text-gray-300">
                    {file.name}
                  </p>
                </div>
              )}

              {/* RESULT */}
              {result && (
                <div className="space-y-8">

                  <div>
                    <h2 className="text-3xl font-bold mb-6 text-slate-800 dark:text-white">
                      Dataset Summary
                    </h2>

                    <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">

                      <div className="bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-700 p-6 rounded-2xl shadow hover:scale-105 transition">
                        <h3 className="text-gray-500 dark:text-gray-400 text-sm mb-2">
                          Filename
                        </h3>
                        <p className="text-xl font-bold text-slate-800 dark:text-white">
                          {result.filename}
                        </p>
                      </div>

                      <div className="bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-700 p-6 rounded-2xl shadow hover:scale-105 transition">
                        <h3 className="text-gray-500 dark:text-gray-400 text-sm mb-2">
                          Original Rows
                        </h3>
                        <p className="text-3xl font-bold text-cyan-500">
                          {result.summary.original_rows}
                        </p>
                      </div>

                      <div className="bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-700 p-6 rounded-2xl shadow hover:scale-105 transition">
                        <h3 className="text-gray-500 dark:text-gray-400 text-sm mb-2">
                          Cleaned Rows
                        </h3>
                        <p className="text-3xl font-bold text-green-500">
                          {result.summary.cleaned_rows}
                        </p>
                      </div>

                      <div className="bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-700 p-6 rounded-2xl shadow hover:scale-105 transition">
                        <h3 className="text-gray-500 dark:text-gray-400 text-sm mb-2">
                          Duplicates Removed
                        </h3>
                        <p className="text-3xl font-bold text-red-500">
                          {result.summary.duplicate_rows_removed}
                        </p>
                      </div>

                    </div>
                  </div>

                  {/* COLUMNS */}
                  <div
                    className="
                    bg-white
                    dark:bg-slate-900/70
                    border
                    border-gray-200
                    dark:border-slate-700
                    rounded-3xl
                    p-8
                    shadow-xl
                    "
                  >
                    <h3 className="text-2xl font-bold mb-5 text-slate-800 dark:text-white">
                      Dataset Columns
                    </h3>

                    <div className="flex flex-wrap gap-3">
                      {result.summary.columns.map((column, index) => (
                        <span
                          key={index}
                          className="
                          px-5
                          py-2
                          rounded-full
                          bg-gradient-to-r
                          from-purple-600
                          to-blue-600
                          text-white
                          text-sm
                          shadow-lg
                          "
                        >
                          {column}
                        </span>
                      ))}
                    </div>
                  </div>

                </div>
              )}
            </div>

            {loading && <Loader />}

          </div>
        </div>
      </div>
    </div>
  );
}