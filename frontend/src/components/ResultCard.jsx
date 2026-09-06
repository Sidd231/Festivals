import { forwardRef } from "react";

const ResultCard = forwardRef(function ResultCard({ visible, value }, ref) {
  return (
    <div
      ref={ref}
      className={`rounded border border-hairline bg-surface p-6 shadow-panel transition-opacity duration-500 ${
        visible ? "opacity-100" : "opacity-0"
      }`}
    >
      <p className="text-xs font-semibold uppercase tracking-wide text-muted">
        Predicted Demand
      </p>
      <p className="mt-2 font-display text-5xl font-semibold text-ink">
        {value !== null ? value.toFixed(2) : "—"}
        <span className="ml-2 text-lg font-sans font-normal text-muted">
          units
        </span>
      </p>
      <p className="mt-3 max-w-sm text-sm leading-relaxed text-muted">
        Estimated demand based on the provided store, product, date and
        festival conditions.
      </p>
    </div>
  );
});

export default ResultCard;
