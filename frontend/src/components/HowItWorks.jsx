const STEPS = [
  {
    n: "01",
    title: "Enter data",
    body: "Store, item, date and festival details are entered in the prediction workspace.",
  },
  {
    n: "02",
    title: "Process features",
    body: "The Flask API converts the form values into the 14 encoded features the model expects.",
  },
  {
    n: "03",
    title: "Model inference",
    body: "The trained XGBoost regression model scores the encoded feature row.",
  },
  {
    n: "04",
    title: "Demand prediction",
    body: "A single predicted demand figure is returned to the browser.",
  },
  {
    n: "05",
    title: "Better decisions",
    body: "Use the estimate to plan stock, staffing and promotions for that date.",
  },
];

export default function HowItWorks() {
  return (
    <section id="how-it-works" className="border-b border-hairline bg-paper">
      <div className="mx-auto max-w-content px-6 py-20">
        <h2 className="font-display text-3xl font-semibold text-ink">
          How it works
        </h2>
        <p className="mt-3 max-w-2xl text-muted">
          Every prediction follows the same path, end to end, from your
          browser to the trained model and back.
        </p>

        <ol className="mt-10 grid gap-8 sm:grid-cols-2 lg:grid-cols-5 lg:gap-6">
          {STEPS.map((step, i) => (
            <li key={step.n} className="relative">
              <div className="flex items-baseline gap-2">
                <span className="font-display text-2xl font-semibold text-marigold-dark">
                  {step.n}
                </span>
              </div>
              <h3 className="mt-2 font-display text-lg font-semibold text-ink">
                {step.title}
              </h3>
              <p className="mt-2 text-sm leading-relaxed text-muted">
                {step.body}
              </p>
              {i < STEPS.length - 1 && (
                <div className="mt-6 hidden h-px bg-hairline lg:block" />
              )}
            </li>
          ))}
        </ol>
      </div>
    </section>
  );
}
