const SIGNALS = [
  "Store and item identifiers",
  "Calendar date, month and weekday",
  "Festival name and festival type",
  "Region",
  "Impact scale of the festival",
  "Regional-event, festival-day and pre-festival-week flags",
  "Days remaining to the next festival",
];

export default function About() {
  return (
    <section id="about" className="border-b border-hairline bg-surface">
      <div className="mx-auto grid max-w-content gap-12 px-6 py-20 lg:grid-cols-2">
        <div>
          <h2 className="font-display text-3xl font-semibold text-ink">
            Why festival-aware, hyperlocal forecasting
          </h2>
          <p className="mt-4 leading-relaxed text-muted">
            Retail demand in India moves sharply around festivals — a
            Raksha Bandhan weekend or the run-up to Diwali can shift demand
            far more than an ordinary calendar date would suggest. Generic
            forecasting models that only look at historical sales trends
            miss this, because the effect of a festival differs by region,
            by how significant the festival is locally, and by how close a
            given date sits to it.
          </p>
          <p className="mt-4 leading-relaxed text-muted">
            Hyperlocal AI is built around that gap. Instead of forecasting
            demand from date and sales history alone, it treats the
            festival calendar as a first-class input — so a store manager
            or planner can ask "what will demand look like on this date, in
            this region, given this festival" and get a store-level answer
            they can act on for stocking, staffing and local promotions.
          </p>
        </div>

        <div>
          <h3 className="font-display text-xl font-semibold text-ink">
            Signals the model reads
          </h3>
          <ul className="mt-4 divide-y divide-hairline rounded border border-hairline">
            {SIGNALS.map((signal) => (
              <li key={signal} className="px-4 py-3 text-sm text-ink">
                {signal}
              </li>
            ))}
          </ul>
          <p className="mt-3 text-xs text-muted">
            These map directly to the 14 input fields the prediction model
            was trained on — see the prediction workspace below.
          </p>
        </div>
      </div>
    </section>
  );
}
