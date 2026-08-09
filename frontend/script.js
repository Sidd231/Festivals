const API_BASE = "http://127.0.0.1:5000";

const STORE_MAP = {
  "Store 1 (Lucknow Central)": 1,
  "Store 2 (Prayagraj Urban)": 2,
  "Store 3 (Varanasi Cluster)": 3,
  "Store 4 (Kanpur Hub)": 4,
  "Store 5 (Noida Sector 62)": 5,
  "Store 6 (Prayagraj Rural)": 6,
  "Store 7 (Ghaziabad Center)": 7,
  "Store 8 (Gorakhpur Outlet)": 8,
  "Store 9 (Agra Heritage Store)": 9,
  "Store 10 (Meerut Mart)": 10
};

const ITEM_MAP = {
  "Traditional Sweets Box": 1,
  "Dry Fruits Gift Hamper": 2,
  "Designer Clay Diyas (Pack of 12)": 3,
  "LED Decorative String Lights (10m)": 4,
  "Traditional Silk Saree": 5,
  "Designer Men's Kurta": 6,
  "Brass Pooja Thali Set": 7,
  "Premium Incense Sticks (Agarbatti)": 8,
  "Fresh Flower Garlands (Marigold)": 9,
  "Rangoli Stencil & Color Kit": 10,
  "Chocolate & Cookie Gift Box": 11,
  "Handcrafted Wall Hangings (Toran)": 12,
  "Traditional Silver Coin (10g)": 13,
  "Ganesh & Lakshmi Clay Idols": 14,
  "Assorted Dry Namkeen Box": 15,
  "Sparklers & Eco-Friendly Crackers": 16,
  "Ethnic Kids Wear Set": 17,
  "Designer Greeting Cards (Pack of 5)": 18,
  "Handmade Scented Gel Candles": 19,
  "Perfume & Fragrance Gift Set": 20,
  "Copper Water Bottle Set": 21,
  "Non-Stick Kitchen Cookware Set": 22,
  "Electric Juicer Mixer Grinder": 23,
  "Microwave Oven (20L)": 24,
  "Air Fryer (4L)": 25,
  "Smart LED TV (32 inch)": 26,
  "Bluetooth Party Speaker": 27,
  "Wireless Earbuds (ANC)": 28,
  "Fitness Smartwatch": 29,
  "5G Android Smartphone": 30,
  "Travel Luggage Suitcase (Medium)": 31,
  "Stainless Steel Dinner Set (36 pcs)": 32,
  "Cotton Bed Sheets Set": 33,
  "Microfiber Pillls (Pack of 2)": 34,
  "Ethnic Home Carpet/Rug": 35,
  "Electric Tea Kettle (1.5L)": 36,
  "Garment Steam Iron": 37,
  "Automatic Espresso Coffee Maker": 38,
  "Instant Water Geyser (3L)": 39,
  "Electric Room Heater": 40,
  "Duffle Gym Bag": 41,
  "Sports Running Shoes": 42,
  "UV Air Purifier for Home": 43,
  "Handcrafted Wooden Spice Box": 44,
  "Handmade Ceramic Serving Bowls": 45,
  "Gold-Plated Photo Frame": 46,
  "Artificial Bonsai Plant with Pot": 47,
  "Aromatic Essential Oil Diffuser": 48,
  "Digital Kitchen Weighing Scale": 49,
  "Premium Leather Wallet & Belt Set": 50
};

const statusPill = document.getElementById("statusPill");
const statusText = document.getElementById("statusText");
const predictBtn = document.getElementById("predictBtn");
const form = document.getElementById("predictForm");
const errorBox = document.getElementById("errorBox");
const resultCard = document.getElementById("resultCard");
const resultValue = document.getElementById("resultValue");

function fillSelect(id, options) {
  const el = document.getElementById(id);
  el.innerHTML = options.map(o => `<option value="${o}">${o}</option>`).join("");
}

async function init() {
  try {
    fillSelect("store", Object.keys(STORE_MAP));
    fillSelect("item", Object.keys(ITEM_MAP));
    const res = await fetch(`${API_BASE}/api/model-info`);
    const data = await res.json();
    if (data.error) throw new Error(data.error);
    statusText.textContent = "HYPERLOCAL AI";
    fillSelect("festival_name", data.options.festival_name);
    fillSelect("festival_type", data.options.festival_type);
    fillSelect("region", data.options.region);
    predictBtn.disabled = false;
  } catch (err) {
    statusText.textContent = "HYPERLOCAL AI";
    console.error(err);
  }
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  errorBox.classList.remove("show");
  resultCard.classList.remove("show");
  predictBtn.disabled = true;
  predictBtn.textContent = "⏳ Analyzing Demand...";

  const storeName = document.getElementById("store").value;
  const itemName = document.getElementById("item").value;
  const dateInput = document.getElementById("forecast_date").value;
  if (!dateInput) {
    errorBox.textContent = "Error: Please select a valid date.";
    errorBox.classList.add("show");
    predictBtn.disabled = false;
    predictBtn.textContent = "🔮 Predict Demand";
    return;
  }
  const [yearStr, monthStr, dayStr] = dateInput.split("-");
  const year = parseInt(yearStr, 10);
  const month = parseInt(monthStr, 10);
  const day = parseInt(dayStr, 10);
  const dateVal = new Date(year, month - 1, day);
  const weekday = dateVal.toLocaleDateString('en-US', { weekday: 'long' });
  const payload = {
    store: STORE_MAP[storeName],
    item: ITEM_MAP[itemName],
    year: year,
    month: month,
    day: day,
    weekday: weekday,
    festival_name: document.getElementById("festival_name").value,
    festival_type: document.getElementById("festival_type").value,
    region: document.getElementById("region").value,
    impact_scale: document.getElementById("impact_scale").value,
    days_to_next_festival: document.getElementById("days_to_next_festival").value,
    is_regional_event: document.getElementById("is_regional_event").checked,
    is_festival_day: document.getElementById("is_festival_day").checked,
    pre_festival_week: document.getElementById("pre_festival_week").checked
  };
  try {
    const res = await fetch(`${API_BASE}/api/predict`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    if (data.error) {
      errorBox.textContent = "Error: " + data.error;
      errorBox.classList.add("show");
    } else {
      resultValue.textContent = data.prediction.toFixed(2);
      resultCard.classList.add("show");
      resultCard.scrollIntoView({ behavior: "smooth", block: "center" });
    }
  } catch (err) {
    errorBox.textContent = "Request failed. Check backend server.";
    errorBox.classList.add("show");
    console.error(err);
  } finally {
    predictBtn.disabled = false;
    predictBtn.textContent = "🔮 Predict Demand";
  }
});

init();
