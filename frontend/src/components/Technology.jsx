const STACK = [
  { group: "Frontend", items: ["React", "Tailwind CSS", "Vite"] },
  { group: "Backend", items: ["Python", "Flask", "Flask-CORS"] },
  { group: "Machine learning", items: ["XGBoost"] },
  { group: "Data processing", items: ["Pandas", "NumPy", "Scikit-learn"] },
];

export default function Technology() {
  return (
    <section id="technology" className="border-b border-hairline bg-surface">
      <div className="mx-auto max-w-content px-6 py-20">
        <h2 className="font-display text-3xl font-semibold text-ink">
          Technology
        </h2>
        <p className="mt-3 max-w-2xl text-muted">
          The stack actually used to build and serve this project.
        </p>

        <div className="mt-10 divide-y divide-hairline rounded border border-hairline">
          {STACK.map((row) => (
            <div
              key={row.group}
              className="flex flex-col gap-2 px-5 py-4 sm:flex-row sm:items-center sm:justify-between"
            >
              <span className="text-sm font-semibold text-ink">
                {row.group}
              </span>
              <span className="text-sm text-muted">
                {row.items.join(" · ")}
              </span>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
