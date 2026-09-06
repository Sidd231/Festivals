import FestivalSpinner from "./FestivalSpinner";

export default function SplashScreen() {
  return (
    <div className="fixed inset-0 z-50 flex flex-col items-center justify-center gap-5 bg-paper">
      <FestivalSpinner size="lg" />
      <p className="font-display text-lg font-semibold text-ink">
        Hyperlocal AI
      </p>
      <p className="text-sm text-muted">Getting things ready…</p>
    </div>
  );
}
