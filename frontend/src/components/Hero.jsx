export default function Hero({ onScrollTo }) {
  return (
    <section id="home" className="border-b border-hairline bg-paper">
      <div className="mx-auto grid max-w-content gap-12 px-6 py-16 sm:py-20 lg:grid-cols-2 lg:items-center lg:py-28">
        <div>
          <p className="text-sm font-medium text-marigold-dark">
            Built for festive-season retail planning in India
          </p>

          <h1 className="mt-4 font-display text-4xl font-semibold leading-tight text-ink md:text-5xl">
            Know what a festival will do to your demand — before it happens.
          </h1>

          <p className="mt-5 max-w-lg text-base leading-relaxed text-muted">
            Hyperlocal AI predicts store-level product demand around Indian
            festivals, using store, product, date and regional festival
            signals. Feed it the details of an upcoming day and it returns an
            estimated demand figure to plan stock, staffing and promotions
            around.
          </p>

          <div className="mt-8 flex flex-wrap gap-4">
            <button
              onClick={() => onScrollTo("#predict")}
              className="rounded bg-ink px-6 py-3 text-sm font-semibold text-white transition-opacity hover:opacity-90"
            >
              Predict Demand
            </button>
            <button
              onClick={() => onScrollTo("#how-it-works")}
              className="rounded border border-hairline px-6 py-3 text-sm font-semibold text-ink transition-colors hover:border-ink"
            >
              Explore Platform
            </button>
          </div>

          <div className="mt-10 flex flex-wrap gap-x-8 gap-y-2 text-xs text-muted">
            <span>React + Tailwind CSS</span>
            <span>Python + Flask API</span>
            <span>XGBoost regression model</span>
          </div>
        </div>

        {/* Example prediction panel — illustrative, not a live/real result */}
        <div className="rounded border border-hairline bg-surface p-6 shadow-panel">
          <p className="text-xs font-medium uppercase tracking-wide text-muted">
            Example input
          </p>
          <dl className="mt-3 grid grid-cols-2 gap-y-2 text-sm">
            <dt className="text-muted">Store / Item</dt>
            <dd className="text-right text-ink">12 / 048</dd>
            <dt className="text-muted">Date</dt>
            <dd className="text-right text-ink">28 Aug 2026 (Fri)</dd>
            <dt className="text-muted">Festival</dt>
            <dd className="text-right text-ink">Raksha Bandhan</dd>
            <dt className="text-muted">Region</dt>
            <dd className="text-right text-ink">North</dd>
            <dt className="text-muted">Pre-festival week</dt>
            <dd className="text-right text-ink">Yes</dd>
          </dl>

          <div className="my-5 h-px bg-hairline" />

          <p className="text-xs font-medium uppercase tracking-wide text-muted">
            Example output
          </p>
          <p className="mt-2 font-display text-4xl font-semibold text-ink">
            428<span className="text-lg text-muted"> units</span>
          </p>
          <p className="mt-1 text-xs text-muted">
            Illustrative only — run the live predictor below for a real
            estimate.
          </p>
        </div>
      </div>
    </section>
  );
}
