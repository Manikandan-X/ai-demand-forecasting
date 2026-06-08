import { useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";

/**
 * Reusable Modal
 *
 * Props:
 *   open       boolean  — show/hide
 *   onClose    fn       — called on backdrop click or X
 *   title      string
 *   children   ReactNode
 *   size       "sm" | "md" | "lg" | "xl"   default "md"
 *   hideClose  boolean  — hide X button
 */
export default function Modal({
  open,
  onClose,
  title,
  children,
  size = "md",
  hideClose = false,
}) {
  // Lock body scroll when open
  useEffect(() => {
    if (open) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "";
    }
    return () => { document.body.style.overflow = ""; };
  }, [open]);

  // Close on Escape
  useEffect(() => {
    const handler = (e) => {
      if (e.key === "Escape" && open) onClose?.();
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [open, onClose]);

  const maxWidths = {
    sm: "max-w-sm",
    md: "max-w-lg",
    lg: "max-w-2xl",
    xl: "max-w-4xl",
  };

  return (
    <AnimatePresence>
      {open && (
        // Backdrop
        <motion.div
          key="backdrop"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.18 }}
          onClick={onClose}
          className="
            fixed inset-0 z-[900]
            bg-black/60 backdrop-blur-sm
            flex items-center justify-center
            p-4
          "
        >
          {/* Panel */}
          <motion.div
            key="panel"
            initial={{ opacity: 0, scale: 0.95, y: 16 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: 16 }}
            transition={{ duration: 0.2 }}
            onClick={(e) => e.stopPropagation()}
            className={`
              w-full ${maxWidths[size]}
              bg-white dark:bg-slate-900
              border border-gray-200 dark:border-slate-700
              rounded-2xl shadow-2xl
              flex flex-col
              max-h-[90vh]
            `}
          >
            {/* Header */}
            {(title || !hideClose) && (
              <div className="
                flex items-center justify-between
                px-6 py-4
                border-b border-gray-100 dark:border-slate-800
                flex-shrink-0
              ">
                {title && (
                  <h2 className="
                    text-lg font-bold
                    text-gray-800 dark:text-white
                    truncate
                  ">
                    {title}
                  </h2>
                )}
                {!hideClose && (
                  <button
                    onClick={onClose}
                    className="
                      ml-auto text-gray-400 hover:text-gray-700
                      dark:hover:text-white
                      text-2xl leading-none transition
                      hover:rotate-90 duration-200
                      flex-shrink-0
                    "
                    aria-label="Close"
                  >
                    ✕
                  </button>
                )}
              </div>
            )}

            {/* Body — scrollable */}
            <div className="overflow-y-auto flex-1 px-6 py-5">
              {children}
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
