const API_BASE_URL = "http://127.0.0.1:5000";

async function parseJsonSafely(res) {
  try {
    return await res.json();
  } catch {
    return null;
  }
}

export async function getModelInfo() {
  const res = await fetch(`${API_BASE_URL}/api/model-info`);
  const data = await parseJsonSafely(res);

  if (!res.ok || !data || data.error) {
    throw new Error((data && data.error) || "Could not load model info from the backend.");
  }
  return data;
}

export async function predictDemand(payload) {
  const res = await fetch(`${API_BASE_URL}/api/predict`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const data = await parseJsonSafely(res);

  if (!res.ok || !data || data.error) {
    throw new Error((data && data.error) || "Prediction request failed.");
  }
  return data;
}
