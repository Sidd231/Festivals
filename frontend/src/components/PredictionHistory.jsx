export default function PredictionHistory({ history, onClear }) {
  return (
    <div className="rounded border border-hairline bg-surface p-6">
      <div className="flex items-center justify-between">
        <p className="text-xs font-semibold uppercase tracking-wide text-muted">
          Recent Predictions
        </p>
        {history.length > 0 && (
          <button
            type="button"
            onClick={onClear}
            className="text-xs font-medium text-muted underline decoration-hairline underline-offset-2 hover:text-ink"
          >
            Clear
          </button>
        )}
      </div>

      {history.length === 0 ? (
        <p className="mt-3 text-sm text-muted">
          Predictions you run in this browser will appear here.
        </p>
      ) : (
        <ul className="mt-3 space-y-3">
          {history.map((entry) => (
            <li
              key={entry.id}
              className="flex items-center justify-between border-b border-hairline pb-3 last:border-0 last:pb-0"
            >
              <div>
                <p className="text-sm text-ink">
                  Store {entry.store} · Item {entry.item}
                </p>
                <p className="text-xs text-muted">
                  {entry.festival_name} · {entry.timestamp}
                </p>
              </div>
              <p className="font-display text-lg font-semibold text-ink">
                {entry.prediction.toFixed(1)}
              </p>
            </li>
          ))}
        </ul>
      )}
      <p className="mt-4 text-xs text-muted">
        Stored only in this browser — never sent to a server.
      </p>
    </div>
  );
}
