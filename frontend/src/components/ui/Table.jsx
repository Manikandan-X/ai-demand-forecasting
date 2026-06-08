import { useState } from "react";

/**
 * Reusable Table
 *
 * Props:
 *   columns   Array<{ key, label, render?, sortable?, className? }>
 *   data      Array<object>
 *   loading   boolean
 *   emptyText string
 *   rowKey    string | fn(row) → key   default "id"
 *   onRowClick fn(row)
 *   skeletonRows  number  default 5
 */
export default function Table({
  columns = [],
  data = [],
  loading = false,
  emptyText = "No data found",
  rowKey = "id",
  onRowClick,
  skeletonRows = 5,
}) {
  const [sortKey, setSortKey]   = useState(null);
  const [sortDir, setSortDir]   = useState("asc");

  const handleSort = (key) => {
    if (sortKey === key) {
      setSortDir((d) => (d === "asc" ? "desc" : "asc"));
    } else {
      setSortKey(key);
      setSortDir("asc");
    }
  };

  const sorted = [...data].sort((a, b) => {
    if (!sortKey) return 0;
    const av = a[sortKey];
    const bv = b[sortKey];
    if (av == null) return 1;
    if (bv == null) return -1;
    const cmp =
      typeof av === "number"
        ? av - bv
        : String(av).localeCompare(String(bv));
    return sortDir === "asc" ? cmp : -cmp;
  });

  const getKey = (row, i) =>
    typeof rowKey === "function" ? rowKey(row) : (row[rowKey] ?? i);

  return (
    <div className="w-full overflow-x-auto rounded-2xl border border-gray-200 dark:border-slate-700">
      <table className="w-full text-sm text-left">

        {/* Head */}
        <thead className="
          bg-gray-50 dark:bg-slate-800
          text-gray-500 dark:text-slate-400
          text-xs uppercase tracking-wider
        ">
          <tr>
            {columns.map((col) => (
              <th
                key={col.key}
                onClick={col.sortable ? () => handleSort(col.key) : undefined}
                className={`
                  px-5 py-3 font-semibold select-none whitespace-nowrap
                  ${col.sortable ? "cursor-pointer hover:text-cyan-500 transition" : ""}
                  ${col.className || ""}
                `}
              >
                <span className="flex items-center gap-1">
                  {col.label}
                  {col.sortable && (
                    <span className="text-xs opacity-50">
                      {sortKey === col.key
                        ? sortDir === "asc" ? "↑" : "↓"
                        : "↕"}
                    </span>
                  )}
                </span>
              </th>
            ))}
          </tr>
        </thead>

        {/* Body */}
        <tbody className="divide-y divide-gray-100 dark:divide-slate-800">

          {/* Loading skeletons */}
          {loading &&
            Array.from({ length: skeletonRows }).map((_, i) => (
              <tr key={`skel-${i}`} className="animate-pulse">
                {columns.map((col) => (
                  <td key={col.key} className="px-5 py-4">
                    <div className="h-4 bg-gray-200 dark:bg-slate-700 rounded-md w-3/4" />
                  </td>
                ))}
              </tr>
            ))}

          {/* Empty */}
          {!loading && sorted.length === 0 && (
            <tr>
              <td
                colSpan={columns.length}
                className="px-5 py-14 text-center text-gray-400 dark:text-slate-500"
              >
                <div className="flex flex-col items-center gap-2">
                  <span className="text-3xl">📭</span>
                  <span>{emptyText}</span>
                </div>
              </td>
            </tr>
          )}

          {/* Rows */}
          {!loading &&
            sorted.map((row, i) => (
              <tr
                key={getKey(row, i)}
                onClick={() => onRowClick?.(row)}
                className={`
                  bg-white dark:bg-slate-900
                  text-gray-700 dark:text-slate-300
                  transition duration-150
                  ${onRowClick ? "cursor-pointer hover:bg-cyan-50 dark:hover:bg-slate-800" : ""}
                `}
              >
                {columns.map((col) => (
                  <td
                    key={col.key}
                    className={`px-5 py-4 ${col.className || ""}`}
                  >
                    {col.render
                      ? col.render(row[col.key], row)
                      : (row[col.key] ?? "—")}
                  </td>
                ))}
              </tr>
            ))}
        </tbody>
      </table>
    </div>
  );
}
