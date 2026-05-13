import { useState } from "react";

import API from "../api/axios";

import Navbar from "../components/Navbar";

export default function UploadDataset() {

  const [file, setFile] = useState(null);

  const [result, setResult] = useState(null);

  const [loading, setLoading] =
    useState(false);

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

      setLoading(false);

      alert("Dataset Uploaded");

    } catch (error) {

      console.error(error);

      setLoading(false);

      alert("Upload Failed");
    }
  };

  return (
    <>
      <Navbar />

      <div className="min-h-screen bg-gray-100 p-8">

        <div className="max-w-4xl mx-auto bg-white p-8 rounded-2xl shadow">

          <h1 className="text-3xl font-bold mb-8">
            Upload Dataset
          </h1>

          <form
            onSubmit={handleUpload}
            className="mb-8"
          >

            <div className="flex flex-col md:flex-row gap-4 items-center">

              <input
                type="file"
                accept=".csv,.xlsx"
                className="border p-3 rounded-lg w-full"
                onChange={(e) =>
                  setFile(e.target.files[0])
                }
              />

              <button
                type="submit"
                className="bg-blue-600 text-white px-6 py-3 rounded-lg w-full md:w-auto"
              >
                {
                  loading
                    ? "Uploading..."
                    : "Upload Dataset"
                }
              </button>

            </div>

          </form>

          {file && (

            <div className="bg-blue-50 p-4 rounded-xl mb-6">

              <p className="text-lg">

                <strong>Selected File:</strong>

                {" "}
                {file.name}

              </p>

            </div>
          )}

          {result && (

            <div className="bg-gray-50 p-6 rounded-2xl">

              <h2 className="text-2xl font-bold mb-6">
                Dataset Summary
              </h2>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

                <div className="bg-white p-4 rounded-xl shadow-sm">

                  <h3 className="font-semibold mb-2">
                    Filename
                  </h3>

                  <p>{result.filename}</p>

                </div>

                <div className="bg-white p-4 rounded-xl shadow-sm">

                  <h3 className="font-semibold mb-2">
                    Original Rows
                  </h3>

                  <p>
                    {result.summary.original_rows}
                  </p>

                </div>

                <div className="bg-white p-4 rounded-xl shadow-sm">

                  <h3 className="font-semibold mb-2">
                    Cleaned Rows
                  </h3>

                  <p>
                    {result.summary.cleaned_rows}
                  </p>

                </div>

                <div className="bg-white p-4 rounded-xl shadow-sm">

                  <h3 className="font-semibold mb-2">
                    Duplicates Removed
                  </h3>

                  <p>
                    {
                      result.summary
                        .duplicate_rows_removed
                    }
                  </p>

                </div>

              </div>

              <div className="mt-8 bg-white p-6 rounded-xl shadow-sm">

                <h3 className="text-xl font-bold mb-4">
                  Dataset Columns
                </h3>

                <div className="flex flex-wrap gap-3">

                  {result.summary.columns.map(
                    (column, index) => (

                      <span
                        key={index}
                        className="bg-purple-100 text-purple-700 px-4 py-2 rounded-full"
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
    </>
  );
}