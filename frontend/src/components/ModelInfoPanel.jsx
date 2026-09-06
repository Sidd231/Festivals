export default function ModelInfoPanel({ modelInfo }) {
  return (
    <div className="rounded border border-hairline bg-surface p-6">
      <p className="text-xs font-semibold uppercase tracking-wide text-muted">
        Model
      </p>
      {modelInfo ? (
        <dl className="mt-3 space-y-2 text-sm">
          <div className="flex justify-between">
            <dt className="text-muted">Model type</dt>
            <dd className="text-ink">{modelInfo.model_type}</dd>
          </div>
          <div className="flex justify-between">
            <dt className="text-muted">Input features</dt>
            <dd className="text-ink">{modelInfo.n_features}</dd>
          </div>
          <div className="flex justify-between">
            <dt className="text-muted">Festivals recognized</dt>
            <dd className="text-ink">
              {modelInfo.options.festival_name.length}
            </dd>
          </div>
        </dl>
      ) : (
        <p className="mt-3 text-sm text-muted">
          Connecting to the prediction backend…
        </p>
      )}
    </div>
  );
}
