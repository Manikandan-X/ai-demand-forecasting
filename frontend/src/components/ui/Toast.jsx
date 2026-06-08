import { createContext, useContext, useState, useCallback } from "react";
import { AnimatePresence, motion } from "framer-motion";

// ── Context ────────────────────────────────
const ToastContext = createContext(null);

// ── Provider (wrap in App.jsx) ─────────────
export function ToastProvider({ children }) {
  const [toasts, setToasts] = useState([]);

  const show = useCallback((message, type = "success", duration = 3500) => {
    const id = Date.now() + Math.random();
    setToasts((t) => [...t, { id, message, type }]);
    setTimeout(() => {
      setToasts((t) => t.filter((x) => x.id !== id));
    }, duration);
  }, []);

  const dismiss = (id) =>
    setToasts((t) => t.filter((x) => x.id !== id));

  return (
    <ToastContext.Provider value={show}>
      {children}
      <ToastContainer toasts={toasts} dismiss={dismiss} />
    </ToastContext.Provider>
  );
}

// ── Hook ───────────────────────────────────
export function useToast() {
  const ctx = useContext(ToastContext);
  if (!ctx) throw new Error("useToast must be inside ToastProvider");
  return ctx;
}

// ── Styles per type ────────────────────────
const TYPE_STYLES = {
  success: {
    bar: "bg-green-500",
    icon: "✅",
    text: "text-green-700 dark:text-green-300",
    bg: "bg-green-50 dark:bg-green-900/30 border-green-200 dark:border-green-800",
  },
  error: {
    bar: "bg-red-500",
    icon: "❌",
    text: "text-red-700 dark:text-red-300",
    bg: "bg-red-50 dark:bg-red-900/30 border-red-200 dark:border-red-800",
  },
  warning: {
    bar: "bg-yellow-400",
    icon: "⚠️",
    text: "text-yellow-700 dark:text-yellow-300",
    bg: "bg-yellow-50 dark:bg-yellow-900/30 border-yellow-200 dark:border-yellow-800",
  },
  info: {
    bar: "bg-blue-500",
    icon: "ℹ️",
    text: "text-blue-700 dark:text-blue-300",
    bg: "bg-blue-50 dark:bg-blue-900/30 border-blue-200 dark:border-blue-800",
  },
};

// ── Container ──────────────────────────────
function ToastContainer({ toasts, dismiss }) {
  return (
    <div className="fixed bottom-6 right-6 z-[9999] flex flex-col gap-3 pointer-events-none">
      <AnimatePresence>
        {toasts.map((t) => {
          const s = TYPE_STYLES[t.type] || TYPE_STYLES.info;
          return (
            <motion.div
              key={t.id}
              initial={{ opacity: 0, x: 60, scale: 0.95 }}
              animate={{ opacity: 1, x: 0, scale: 1 }}
              exit={{ opacity: 0, x: 60, scale: 0.95 }}
              transition={{ duration: 0.22 }}
              className={`
                pointer-events-auto
                relative overflow-hidden
                min-w-[260px] max-w-[360px]
                rounded-2xl border shadow-xl
                px-4 py-3
                ${s.bg}
              `}
            >
              {/* Accent bar */}
              <div className={`absolute left-0 top-0 bottom-0 w-1 ${s.bar}`} />

              <div className="flex items-start gap-3 pl-2">
                <span className="text-lg flex-shrink-0">{s.icon}</span>
                <p className={`text-sm font-medium flex-1 ${s.text}`}>
                  {t.message}
                </p>
                <button
                  onClick={() => dismiss(t.id)}
                  className="text-gray-400 hover:text-gray-600 dark:hover:text-white text-lg leading-none flex-shrink-0"
                >
                  ✕
                </button>
              </div>
            </motion.div>
          );
        })}
      </AnimatePresence>
    </div>
  );
}
