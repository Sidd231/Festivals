import PredictionForm from "./PredictionForm";
import ResultCard from "./ResultCard";
import ErrorBox from "./ErrorBox";
import PredictionHistory from "./PredictionHistory";
import FestivalSpinner from "./FestivalSpinner";

export default function PredictWorkspace({
  formData,
  onFieldChange,
  onSubmit,
  onReset,
  modelInfo,
  predicting,
  errorMessage,
  prediction,
  showResult,
  resultRef,
  history,
  onClearHistory,
}) {
  return (
    <section id="predict" className="border-b border-hairline bg-paper">
      <div className="mx-auto max-w-content px-6 py-20">
        <h2 className="font-display text-3xl font-semibold text-ink">
          Prediction workspace
        </h2>
        <p className="mt-3 max-w-2xl text-muted">
          Fill in the store, date and festival details for the day you want
          to plan around. The form is grouped to match how the model reads
          the data.
        </p>

        <div className="mt-10 grid gap-8 lg:grid-cols-3">
          <div className="rounded border border-hairline bg-surface p-6 shadow-panel lg:col-span-2">
            <PredictionForm
              formData={formData}
              onFieldChange={onFieldChange}
              onSubmit={onSubmit}
              onReset={onReset}
              modelInfo={modelInfo}
              predicting={predicting}
            />
          </div>

          <div className="space-y-6 lg:sticky lg:top-24 lg:self-start">
            <ErrorBox message={errorMessage} />

            {predicting ? (
              <div className="flex flex-col items-center gap-3 rounded border border-hairline bg-surface p-8 text-center">
                <FestivalSpinner />
                <p className="text-sm font-medium text-ink">
                  Crunching the numbers…
                </p>
                <p className="text-xs text-muted">
                  Running your inputs through the model.
                </p>
              </div>
            ) : (
              showResult && (
                <ResultCard ref={resultRef} visible={showResult} value={prediction} />
              )
            )}

            <PredictionHistory history={history} onClear={onClearHistory} />
          </div>
        </div>
      </div>
    </section>
  );
}
