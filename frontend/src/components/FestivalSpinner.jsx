import { useEffect, useState } from "react";

const FESTIVAL_ICONS = ["🪔", "🎆", "🎇", "🎊", "🪁", "🎉"];

export default function FestivalSpinner({ size = "md", className = "" }) {
  const [index, setIndex] = useState(0);

  useEffect(() => {
    const id = setInterval(() => {
      setIndex((prev) => (prev + 1) % FESTIVAL_ICONS.length);
    }, 500);
    return () => clearInterval(id);
  }, []);

  const dims = size === "sm" ? "h-5 w-5" : size === "lg" ? "h-20 w-20" : "h-14 w-14";
  const iconSize = size === "sm" ? "text-[11px]" : size === "lg" ? "text-4xl" : "text-2xl";

  return (
    <span className={`relative inline-block shrink-0 ${dims} ${className}`}>
      {/* Spinning ring — a separate layer so it rotates without spinning the icon inside it */}
      <span
        className="absolute inset-0 animate-spin rounded-full border-2 border-hairline border-t-marigold"
        aria-hidden="true"
      />
      {/* Cycling festival icon — stays upright */}
      <span
        className={`absolute inset-0 flex items-center justify-center ${iconSize}`}
        aria-hidden="true"
      >
        {FESTIVAL_ICONS[index]}
      </span>
      <span className="sr-only">Loading</span>
    </span>
  );
}
