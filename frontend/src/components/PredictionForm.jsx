import FestivalSpinner from "./FestivalSpinner";

const MONTHS = [
  { value: "1", label: "January" },
  { value: "2", label: "February" },
  { value: "3", label: "March" },
  { value: "4", label: "April" },
  { value: "5", label: "May" },
  { value: "6", label: "June" },
  { value: "7", label: "July" },
  { value: "8", label: "August" },
  { value: "9", label: "September" },
  { value: "10", label: "October" },
  { value: "11", label: "November" },
  { value: "12", label: "December" },
];

const WEEKDAYS = [
  { value: "0", label: "Monday" },
  { value: "1", label: "Tuesday" },
  { value: "2", label: "Wednesday" },
  { value: "3", label: "Thursday" },
  { value: "4", label: "Friday" },
  { value: "5", label: "Saturday" },
  { value: "6", label: "Sunday" },
];

function Field({ label, hint, children }) {
  return (
    <label className="block">
      <span className="text-sm font-medium text-ink">{label}</span>
      {children}
      {hint && <span className="mt-1 block text-xs text-muted">{hint}</span>}
    </label>
  );
}

const inputClass =
  "mt-1.5 w-full rounded border border-hairline bg-surface px-3 py-2 text-sm text-ink transition-colors focus:border-ink";

function Toggle({ label, checked, onChange }) {
  return (
    <label className="flex items-center justify-between rounded border border-hairline bg-surface px-4 py-3">
      <span className="text-sm font-medium text-ink">{label}</span>
      <span className="relative inline-flex h-5 w-9 shrink-0 items-center">
        <input
          type="checkbox"
          checked={checked}
          onChange={onChange}
          className="peer absolute inset-0 h-full w-full cursor-pointer opacity-0"
        />
        <span className="pointer-events-none absolute inset-0 rounded-full bg-hairline transition-colors peer-checked:bg-teal" />
        <span className="pointer-events-none absolute left-0.5 h-4 w-4 rounded-full bg-white shadow transition-transform peer-checked:translate-x-4" />
      </span>
    </label>
  );
}

export default function PredictionForm({
  formData,
  onFieldChange,
  onSubmit,
  onReset,
  modelInfo,
  predicting,
}) {
  const options = modelInfo ? modelInfo.options : null;
  const predictDisabled = !modelInfo || predicting;

  const handleTextChange = (id) => (e) => onFieldChange(id, e.target.value);
  const handleCheckChange = (id) => (e) => onFieldChange(id, e.target.checked);

  return (
    <form onSubmit={onSubmit} className="space-y-8">
      <fieldset>
        <legend className="text-xs font-semibold uppercase tracking-wide text-marigold-dark">
          Store &amp; Product
        </legend>
        <div className="mt-3 grid gap-4 sm:grid-cols-2">
          <Field label="Store ID">
            <input
              type="number"
              required
              className={inputClass}
              value={formData.store}
              onChange={handleTextChange("store")}
            />
          </Field>
          <Field label="Item ID">
            <input
              type="number"
              required
              className={inputClass}
              value={formData.item}
              onChange={handleTextChange("item")}
            />
          </Field>
        </div>
      </fieldset>

      <fieldset>
        <legend className="text-xs font-semibold uppercase tracking-wide text-marigold-dark">
          Date &amp; Time
        </legend>
        <div className="mt-3 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <Field label="Year">
            <input
              type="number"
              required
              className={inputClass}
              value={formData.year}
              onChange={handleTextChange("year")}
            />
          </Field>
          <Field label="Month">
            <select
              required
              className={inputClass}
              value={formData.month}
              onChange={handleTextChange("month")}
            >
              {MONTHS.map((m) => (
                <option key={m.value} value={m.value}>
                  {m.label}
                </option>
              ))}
            </select>
          </Field>
          <Field label="Day of month">
            <input
              type="number"
              min="1"
              max="31"
              required
              className={inputClass}
              value={formData.day}
              onChange={handleTextChange("day")}
            />
          </Field>
          <Field label="Weekday">
            <select
              required
              className={inputClass}
              value={formData.weekday}
              onChange={handleTextChange("weekday")}
            >
              {WEEKDAYS.map((w) => (
                <option key={w.value} value={w.value}>
                  {w.label}
                </option>
              ))}
            </select>
          </Field>
        </div>
      </fieldset>

      <fieldset>
        <legend className="text-xs font-semibold uppercase tracking-wide text-marigold-dark">
          Festival Information
        </legend>
        <div className="mt-3 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <Field label="Festival name">
            <select
              className={inputClass}
              value={formData.festival_name}
              onChange={handleTextChange("festival_name")}
            >
              {(options?.festival_name || []).map((name) => (
                <option key={name} value={name}>
                  {name}
                </option>
              ))}
            </select>
          </Field>
          <Field label="Festival type">
            <select
              className={inputClass}
              value={formData.festival_type}
              onChange={handleTextChange("festival_type")}
            >
              {(options?.festival_type || []).map((type) => (
                <option key={type} value={type}>
                  {type}
                </option>
              ))}
            </select>
          </Field>
          <Field label="Region">
            <select
              className={inputClass}
              value={formData.region}
              onChange={handleTextChange("region")}
            >
              {(options?.region || []).map((region) => (
                <option key={region} value={region}>
                  {region}
                </option>
              ))}
            </select>
          </Field>
          <Field label="Impact scale" hint={`${formData.impact_scale} / 100`}>
            <input
              type="range"
              min="0"
              max="100"
              value={formData.impact_scale}
              onChange={handleTextChange("impact_scale")}
            />
          </Field>
        </div>
      </fieldset>

      <fieldset>
        <legend className="text-xs font-semibold uppercase tracking-wide text-marigold-dark">
          Event Indicators
        </legend>
        <div className="mt-3 grid gap-4 sm:grid-cols-2">
          <Field label="Days to next festival">
            <input
              type="number"
              min="0"
              required
              className={inputClass}
              value={formData.days_to_next_festival}
              onChange={handleTextChange("days_to_next_festival")}
            />
          </Field>
          <div className="grid gap-3">
            <Toggle
              label="Regional event"
              checked={formData.is_regional_event}
              onChange={handleCheckChange("is_regional_event")}
            />
            <Toggle
              label="Festival day"
              checked={formData.is_festival_day}
              onChange={handleCheckChange("is_festival_day")}
            />
            <Toggle
              label="Pre-festival week"
              checked={formData.pre_festival_week}
              onChange={handleCheckChange("pre_festival_week")}
            />
          </div>
        </div>
      </fieldset>

      <div className="flex flex-wrap gap-3 pt-2">
        <button
          type="submit"
          disabled={predictDisabled}
          className="inline-flex items-center justify-center gap-2.5 rounded bg-ink px-6 py-3 text-sm font-semibold text-white transition-opacity hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-40"
        >
          {predicting && <FestivalSpinner size="sm" />}
          {predicting ? "Analyzing demand…" : "Predict Demand"}
        </button>
        <button
          type="button"
          onClick={onReset}
          className="rounded border border-hairline px-6 py-3 text-sm font-semibold text-ink transition-colors hover:border-ink"
        >
          Reset
        </button>
      </div>
    </form>
  );
}
