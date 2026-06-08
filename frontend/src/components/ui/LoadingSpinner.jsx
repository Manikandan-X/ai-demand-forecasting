/**
 * Loading components — import what you need:
 *
 *   import { Spinner, PageLoader, CardSkeleton, InlineLoader } from "../components/ui/LoadingSpinner";
 */

// ── Spinner ────────────────────────────────
export function Spinner({ size = "md", color = "cyan" }) {
  const sizes = { sm: "w-4 h-4", md: "w-8 h-8", lg: "w-12 h-12" };
  const colors = {
    cyan:  "border-cyan-500",
    blue:  "border-blue-500",
    white: "border-white",
    gray:  "border-gray-400",
  };
  return (
    <div
      className={`
        ${sizes[size]} ${colors[color]}
        border-4 border-t-transparent
        rounded-full animate-spin
      `}
    />
  );
}

// ── Full page overlay loader ───────────────
export function PageLoader({ message = "Loading…" }) {
  return (
    <div className="
      fixed inset-0 z-[800]
      bg-white/80 dark:bg-slate-950/80
      backdrop-blur-sm
      flex flex-col items-center justify-center gap-4
    ">
      <Spinner size="lg" />
      <p className="text-gray-500 dark:text-slate-400 text-sm font-medium animate-pulse">
        {message}
      </p>
    </div>
  );
}

// ── Card skeleton (replaces SkeletonCard) ──
export function CardSkeleton({ count = 1 }) {
  return (
    <>
      {Array.from({ length: count }).map((_, i) => (
        <div
          key={i}
          className="
            bg-white dark:bg-slate-900
            border border-gray-200 dark:border-slate-700
            rounded-2xl p-6 animate-pulse
          "
        >
          <div className="h-3 bg-gray-200 dark:bg-slate-700 rounded w-1/3 mb-4" />
          <div className="h-8 bg-gray-200 dark:bg-slate-700 rounded w-1/2 mb-2" />
          <div className="h-3 bg-gray-200 dark:bg-slate-700 rounded w-2/3" />
        </div>
      ))}
    </>
  );
}

// ── Inline button loader ───────────────────
export function InlineLoader({ text = "Loading…" }) {
  return (
    <span className="flex items-center gap-2 text-sm text-gray-500 dark:text-slate-400">
      <Spinner size="sm" />
      {text}
    </span>
  );
}

// ── Section skeleton (for tables / lists) ──
export function SectionSkeleton({ rows = 4 }) {
  return (
    <div className="space-y-3 animate-pulse">
      {Array.from({ length: rows }).map((_, i) => (
        <div key={i} className="h-10 bg-gray-200 dark:bg-slate-800 rounded-xl" />
      ))}
    </div>
  );
}

// Default export = Spinner for convenience
export default Spinner;
