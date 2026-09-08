import { useEffect, useRef, useState } from "react";
import Navbar from "./components/Navbar";
import Hero from "./components/Hero";
import About from "./components/About";
import HowItWorks from "./components/HowItWorks";
import PredictWorkspace from "./components/PredictWorkspace";
import FAQ from "./components/FAQ";
import Footer from "./components/Footer";
import SplashScreen from "./components/SplashScreen";
import { getModelInfo, predictDemand } from "./services/api";

const SPLASH_DURATION_MS = 2000;

const INITIAL_FORM_DATA = {
  store: "",
  item: "",
  year: "2026",
  month: "8",
  day: "9",
  weekday: "6",
  festival_name: "",
  festival_type: "",
  region: "",
  impact_scale: "50",
  days_to_next_festival: "5",
  is_regional_event: false,
  is_festival_day: false,
  pre_festival_week: false,
};

const HISTORY_KEY = "hyperlocal-ai:prediction-history";
const HISTORY_LIMIT = 5;

function loadHistory() {
  try {
    const raw = localStorage.getItem(HISTORY_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch {
    return [];
  }
}

export default function App() {
  const [showSplash, setShowSplash] = useState(true);
  const [modelInfo, setModelInfo] = useState(null);
  const [formData, setFormData] = useState(INITIAL_FORM_DATA);
  const [predicting, setPredicting] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [prediction, setPrediction] = useState(null);
  const [showResult, setShowResult] = useState(false);
  const [history, setHistory] = useState(loadHistory);

  const resultRef = useRef(null);

  useEffect(() => {
    const timer = setTimeout(() => setShowSplash(false), SPLASH_DURATION_MS);
    return () => clearTimeout(timer);
  }, []);

  useEffect(() => {
    let cancelled = false;

    getModelInfo()
      .then((data) => {
        if (cancelled) return;
        setModelInfo(data);

        setFormData((prev) => ({
          ...prev,
          festival_name: prev.festival_name || data.options.festival_name[0] || "",
          festival_type: prev.festival_type || data.options.festival_type[0] || "",
          region: prev.region || data.options.region[0] || "",
        }));
      })
      .catch((err) => {
        console.error(err);
      });

    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    if (showResult && resultRef.current) {
      resultRef.current.scrollIntoView({ behavior: "smooth", block: "center" });
    }
  }, [showResult]);

  function handleFieldChange(id, value) {
    setFormData((prev) => ({ ...prev, [id]: value }));
  }

  function handleReset() {
    setFormData((prev) => ({
      ...INITIAL_FORM_DATA,
      festival_name: modelInfo?.options.festival_name[0] || "",
      festival_type: modelInfo?.options.festival_type[0] || "",
      region: modelInfo?.options.region[0] || "",
    }));
    setPrediction(null);
    setShowResult(false);
    setErrorMessage("");
  }

  function scrollTo(hash) {
    document.querySelector(hash)?.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  function handleClearHistory() {
    setHistory([]);
    localStorage.removeItem(HISTORY_KEY);
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setErrorMessage("");
    setShowResult(false);
    setPredicting(true);

    try {
        const data = await predictDemand(formData);
      await new Promise((resolve) => setTimeout(resolve, 2000));
      setPrediction(data.prediction);
      setShowResult(true);

      const entry = {
        id: Date.now(),
        store: formData.store,
        item: formData.item,
        festival_name: formData.festival_name,
        prediction: data.prediction,
        timestamp: new Date().toLocaleString(),
      };
      setHistory((prev) => {
        const next = [entry, ...prev].slice(0, HISTORY_LIMIT);
        localStorage.setItem(HISTORY_KEY, JSON.stringify(next));
        return next;
      });
    } catch (err) {
      setErrorMessage(err.message || "Request failed. Check backend server.");
    } finally {
      setPredicting(false);
    }
  }

  return (
    <div className="font-sans text-ink">
      {showSplash && <SplashScreen />}

      <Navbar />
      <Hero onScrollTo={scrollTo} />
      <About />
      <HowItWorks />
      <PredictWorkspace
        formData={formData}
        onFieldChange={handleFieldChange}
        onSubmit={handleSubmit}
        onReset={handleReset}
        modelInfo={modelInfo}
        predicting={predicting}
        errorMessage={errorMessage}
        prediction={prediction}
        showResult={showResult}
        resultRef={resultRef}
        history={history}
        onClearHistory={handleClearHistory}
      />
      <FAQ />
      <Footer />
    </div>
  );
}
