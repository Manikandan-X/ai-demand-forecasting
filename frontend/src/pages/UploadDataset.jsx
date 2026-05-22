import { useState } from "react";
import API from "../api/axios";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";

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

      const response = await API.post(
        "/dataset/upload",
        formData,
        {
          headers: {
            "Content-Type":
              "multipart/form-data",
          },
        }
      );

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
    <div className="flex min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-gray-950 text-white">

      <Sidebar />

      <div className="flex-1">

        <Navbar />

        <div className="p-6 md:p-10">

          {/* TITLE */}
          <div className="mb-8">

            <h1 className="text-4xl font-bold mb-2">
              Upload Dataset
            </h1>

            <p className="text-slate-400">
              Upload CSV or Excel datasets for AI forecasting
            </p>

          </div>

          {/* MAIN CARD */}
          <div
            className="
            bg-white/10
            backdrop-blur-lg
            border border-white/10
            rounded-3xl
            p-8
            shadow-2xl
            "
          >

            {/* FORM */}
            <form
              onSubmit={handleUpload}
              className="mb-8"
            >

              <div className="flex flex-col lg:flex-row gap-5">

                <input
                  type="file"
                  accept=".csv,.xlsx"
                  onChange={(e) =>
                    setFile(e.target.files[0])
                  }
                  className="
                  flex-1
                  bg-slate-800
                  border
                  border-slate-700
                  text-slate-300
                  rounded-xl
                  px-5
                  py-4
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
                  hover:scale-105
                  transition
                  duration-300
                  shadow-lg
                  "
                >
                  {loading
                    ? "Uploading..."
                    : "Upload Dataset"}
                </button>

              </div>

            </form>

            {/* FILE SELECTED */}
            {file && (

              <div
                className="
                bg-blue-500/10
                border border-blue-500/20
                rounded-2xl
                p-5
                mb-8
                "
              >

                <h3 className="font-semibold text-lg mb-2">
                  Selected File
                </h3>

                <p className="text-slate-300">
                  {file.name}
                </p>

              </div>
            )}

            {/* RESULT */}
            {result && (

              <div className="space-y-8">

                <div>

                  <h2 className="text-3xl font-bold mb-6">
                    Dataset Summary
                  </h2>

                  <div
                    className="
                    grid
                    grid-cols-1
                    md:grid-cols-2
                    xl:grid-cols-4
                    gap-6
                    "
                  >

                    <div className="bg-slate-900 p-6 rounded-2xl border border-slate-800 hover:scale-105 transition">
                      <h3 className="text-slate-400 text-sm mb-2">
                        Filename
                      </h3>

                      <p className="text-xl font-bold">
                        {result.filename}
                      </p>
                    </div>

                    <div className="bg-slate-900 p-6 rounded-2xl border border-slate-800 hover:scale-105 transition">
                      <h3 className="text-slate-400 text-sm mb-2">
                        Original Rows
                      </h3>

                      <p className="text-3xl font-bold text-cyan-400">
                        {
                          result.summary
                            .original_rows
                        }
                      </p>
                    </div>

                    <div className="bg-slate-900 p-6 rounded-2xl border border-slate-800 hover:scale-105 transition">
                      <h3 className="text-slate-400 text-sm mb-2">
                        Cleaned Rows
                      </h3>

                      <p className="text-3xl font-bold text-green-400">
                        {
                          result.summary
                            .cleaned_rows
                        }
                      </p>
                    </div>

                    <div className="bg-slate-900 p-6 rounded-2xl border border-slate-800 hover:scale-105 transition">
                      <h3 className="text-slate-400 text-sm mb-2">
                        Duplicates Removed
                      </h3>

                      <p className="text-3xl font-bold text-red-400">
                        {
                          result.summary
                            .duplicate_rows_removed
                        }
                      </p>
                    </div>

                  </div>

                </div>

                {/* COLUMNS */}
                <div className="bg-slate-900 rounded-3xl p-8">

                  <h3 className="text-2xl font-bold mb-5">
                    Dataset Columns
                  </h3>

                  <div className="flex flex-wrap gap-3">

                    {result.summary.columns.map(
                      (
                        column,
                        index
                      ) => (
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
                      )
                    )}

                  </div>

                </div>

              </div>
            )}

          </div>

        </div>

      </div>

    </div>
  );
}