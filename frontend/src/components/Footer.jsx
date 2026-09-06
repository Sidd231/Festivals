export default function Footer() {
  return (
    <footer className="bg-ink text-white">
      <div className="mx-auto max-w-content px-6 py-14">
        <div className="grid gap-10 md:grid-cols-3">
          <div>
            <p className="font-display text-lg font-semibold">Hyperlocal AI</p>
            <p className="mt-2 max-w-xs text-sm text-white/60">
              Festive-aware demand forecasting for hyperlocal retail
              planning, powered by a trained XGBoost model.
            </p>
          </div>

          <div>
            <p className="text-sm font-semibold">Navigate</p>
            <ul className="mt-3 space-y-2 text-sm text-white/60">
              <li><a href="#about" className="hover:text-white">About</a></li>
              <li><a href="#how-it-works" className="hover:text-white">How It Works</a></li>
              <li><a href="#predict" className="hover:text-white">Predict</a></li>
              <li><a href="#faq" className="hover:text-white">FAQ</a></li>
            </ul>
          </div>

          <div>
            <p className="text-sm font-semibold">Contact</p>
            <ul className="mt-3 space-y-2 text-sm text-white/60">
              <li>contact@hyperlocalai.com</li>
              <li>+91 00000 00000</li>
            </ul>
          </div>
        </div>

        <div className="mt-10 border-t border-white/10 pt-6 text-xs text-white/50">
          © {new Date().getFullYear()} Hyperlocal Festive-Aware Demand AI.
        </div>
      </div>
    </footer>
  );
}
