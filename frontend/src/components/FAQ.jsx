import { useState } from "react";

const FAQS = [
  {
    q: "What is demand forecasting?",
    a: "Predicting how much of a product a store is likely to need on a given date, so stocking, staffing and promotions can be planned in advance.",
  },
  {
    q: "What does festival-aware forecasting mean?",
    a: "Instead of relying only on historical sales trends, the model takes festival name, festival type, region, how significant the festival is, and how close the date is to a festival as direct inputs.",
  },
  {
    q: "What inputs are required?",
    a: "Store ID, item ID, the date (year, month, day, weekday), festival name, festival type, region, impact scale, days to the next festival, and three yes/no event flags — 14 fields in total.",
  },
  {
    q: "How does the prediction work?",
    a: "The Flask API encodes your form inputs using the same encoders the model was trained with, then passes them to a trained XGBoost regression model, which returns a single predicted demand value.",
  },
  {
    q: "Is the prediction real-time?",
    a: "Yes. Each prediction is computed on demand by the Flask API the moment you submit the form — nothing is precomputed or cached.",
  },
  {
    q: "What model powers the prediction?",
    a: "An XGBoost regression model (XGBRegressor), trained ahead of time and loaded once when the backend starts.",
  },
];

function FaqItem({ q, a }) {
  const [open, setOpen] = useState(false);
  return (
    <div className="border-b border-hairline py-4">
      <button
        type="button"
        onClick={() => setOpen((v) => !v)}
        aria-expanded={open}
        className="flex w-full items-center justify-between text-left"
      >
        <span className="text-sm font-semibold text-ink">{q}</span>
        <span className="ml-4 text-lg text-muted">{open ? "–" : "+"}</span>
      </button>
      {open && <p className="mt-3 text-sm leading-relaxed text-muted">{a}</p>}
    </div>
  );
}

export default function FAQ() {
  return (
    <section id="faq" className="border-b border-hairline bg-paper">
      <div className="mx-auto max-w-content px-6 py-20">
        <h2 className="font-display text-3xl font-semibold text-ink">
          Frequently asked questions
        </h2>

        <div className="mt-8 max-w-2xl">
          {FAQS.map((item) => (
            <FaqItem key={item.q} q={item.q} a={item.a} />
          ))}
        </div>
      </div>
    </section>
  );
}
