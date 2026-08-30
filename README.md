# Festive Demand Forecast AI

An AI-powered demand forecasting application that uses a trained XGBoost regression model to predict inventory demand based on store, item, date, and festival-related factors.

---

## Tech Stack

### Backend
* **Python 3.12+**
* **Flask** - REST API server
* **Flask-CORS** - Enable Cross-Origin Resource Sharing
* **XGBoost** - Gradient boosted decision trees model
* **Scikit-learn** - Machine learning utilities
* **Pandas & NumPy** - Data processing and numerical calculations

### Frontend
* **HTML5 & Vanilla CSS** - Structure and custom modern styling
* **JavaScript (ES6)** - API consumption, dynamic state management, and charting
* **Chart.js** - Dynamic interactive demand forecast visualizations
* **Google Fonts (Inter)** - Modern typography

---

## Project Structure

```text
Festivals/
├── .venv/                  # Python Virtual Environment (created during setup)
├── DataSet/                # Raw datasets for modeling
│   ├── sample_submission.csv
│   └── test.csv
├── Model/                  # Notebooks for model training & exploratory data analysis
│   ├── Cleaning.ipynb      # Notebook for dataset preprocessing & cleaning
│   └── Festival_model.ipynb# XGBoost regression model training and validation
├── backend/                # Flask API server
│   ├── XGmodel.pkl         # Serialized (pickled) XGBoost regression model
│   ├── app.py              # Flask server and prediction routes
│   ├── requirements.txt    # Dependencies specific to the backend API server
│   └── test_unpickle.py    # Utility script to test model deserialization
├── frontend/               # Frontend user interface
│   └── index.html          # Interactive client dashboard
├── .gitignore              # Git ignore configuration
├── README.md               # Project documentation (this file)
├── requirements.txt        # Comprehensive root project dependencies
└── run_backend.bat         # Batch script to easily run backend on Windows
```

---

## Getting Started

### Prerequisites
Make sure you have [Python 3.12+](https://www.python.org/downloads/) installed.

### Installation & Setup

1. **Clone or open the workspace folder:**
   ```bash
   cd Festivals
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment:**
   * **Windows (Command Prompt / PowerShell):**
     ```powershell
     .venv\Scripts\activate
     ```
   * **macOS / Linux:**
     ```bash
     source .venv/bin/activate
     ```

4. **Install dependencies:**
   * For model training & data exploration (includes Jupyter, seaborn, matplotlib, openpyxl, etc.):
     ```bash
     pip install -r requirements.txt
     ```
   * For running only the Flask backend API server:
     ```bash
     pip install -r backend/requirements.txt
     ```

---

## Running the Application

### 1. Launch the Backend Server
* **On Windows:**
  Simply double-click the `run_backend.bat` script file, or run it in the terminal:
  ```cmd
  run_backend.bat
  ```
* **Or manually run via Python:**
  Ensure your virtual environment is active, then navigate to the backend folder and run `app.py`:
  ```bash
  cd backend
  python app.py
  ```
  The server will start at `http://127.0.0.1:5000`.

### 2. Launch the Frontend Dashboard
* Simply open `frontend/index.html` in any web browser of your choice (you can double-click the file or use a web server like Live Server in VS Code).

---

## API Documentation

### 1. Health Check
* **Endpoint:** `GET /`
* **Response:**
  ```json
  {
    "status": "Backend is running",
    "model_loaded": true
  }
  ```

### 2. Model Info
* **Endpoint:** `GET /api/model-info`
* **Response:** Returns the type of the model, feature order, and allowed dropdown values for categorical options.
  ```json
  {
    "feature_names": [
      "store", "item", "year", "month", "day", "weekday",
      "festival_name", "festival_type", "region", "impact_scale",
      "is_regional_event", "days_to_next_festival",
      "is_festival_day", "pre_festival_week"
    ],
    "model_type": "XGBRegressor",
    "n_features": 14,
    "options": {
      "festival_name": ["None", "Diwali", "Holi", "Raksha Bandhan", "Navratri", "Eid", "Christmas", "Republic Day", "Independence Day", "Dussehra"],
      "festival_type": ["None", "National", "Regional", "Religious"],
      "region": ["Prayagraj Urban", "Prayagraj Rural", "Lucknow Central", "Varanasi Cluster"]
    }
  }
  ```

### 3. Predict Demand
* **Endpoint:** `POST /api/predict`
* **Headers:** `Content-Type: application/json`
* **Request Body Example:**
  ```json
  {
    "store": 1,
    "item": 5,
    "year": 2026,
    "month": 8,
    "day": 28,
    "weekday": 4,
    "festival_name": "Raksha Bandhan",
    "festival_type": "Religious",
    "region": "Lucknow Central",
    "impact_scale": 70,
    "is_regional_event": false,
    "days_to_next_festival": 2,
    "is_festival_day": false,
    "pre_festival_week": true
  }
  ```
* **Response Example:**
  ```json
  {
    "encoded_input": {
      "days_to_next_festival": 2.0,
      "day": 28.0,
      "festival_name": 7.0,
      "festival_type": 3.0,
      "impact_scale": 70.0,
      "is_festival_day": 0.0,
      "is_regional_event": 0.0,
      "item": 5.0,
      "month": 8.0,
      "pre_festival_week": 1.0,
      "region": 1.0,
      "store": 1.0,
      "weekday": 4.0,
      "year": 2026.0
    },
    "prediction": 425.32
  }
  ```

---

## Item ID to Item Name Mapping

Based on the sales behavior (daily averages, peak volumes, and statistical profiles) analyzed from `cleaned_data.csv`, the 50 item numbers have been mapped to realistic retail/grocery products:

| Item ID | Item Name | Sales Tier | Avg Daily Sales | Characterized Behavior |
| :---: | :--- | :---: | :---: | :--- |
| **1** | Premium Organic Saffron | Low | 21.85 | Premium niche cooking spice with low, stable demand |
| **2** | Whole Milk (1 Gallon) | Medium-High | 58.20 | Daily dairy staple with strong consistent weekly turnover |
| **3** | Ground Coffee Beans | Medium | 36.44 | High-turnover breakfast pantry beverage |
| **4** | Extra Virgin Olive Oil | Low | 21.85 | Slow-moving premium cooking oil |
| **5** | Truffle Butter | Low | 18.21 | Lowest volume luxury gourmet item |
| **6** | Salted Butter (500g) | Medium-High | 58.17 | High-volume baking and cooking essential |
| **7** | Fresh Eggs (Dozen) | Medium-High | 58.22 | High-frequency daily breakfast staple |
| **8** | Bottled Spring Water (24pk) | High | 76.50 | Very high-turnover essential beverage product |
| **9** | Fresh Bananas (Bunch) | Medium-High | 51.06 | Rapidly rotating fresh produce item |
| **10** | Soft Drinks (6-pack) | High | 72.86 | Popular high-demand carbonated beverage |
| **11** | Toilet Paper (Ultra Soft) | High | 69.21 | High-volume non-perishable household essential |
| **12** | Paper Towels (2-ply) | High | 69.21 | High-volume non-perishable cleaning staple |
| **13** | Dishwashing Liquid Soap | High | 83.85 | Top-tier high-turnover cleaning product |
| **14** | Sliced White Bread | Medium-High | 58.31 | Short shelf-life bakery staple with constant sales |
| **15** | Laundry Detergent Pods | High | 87.48 | Highest-demand household utility item |
| **16** | Dark Chocolate Bar | Medium-Low | 25.47 | Moderate indulgence snack |
| **17** | Scented Candles (Lavender) | Medium-Low | 32.79 | Medium-low demand home fragrance product |
| **18** | Multi-Surface Spray Cleaner | High | 83.79 | High-volume sanitation and cleaning product |
| **19** | Raw Almonds (500g) | Medium | 40.14 | Healthy snack with steady year-round sales |
| **20** | Organic Wheat Flour (5kg) | Medium | 47.17 | Stable bulk baking dry ingredient |
| **21** | Organic Green Tea (Box) | Medium | 40.07 | Consistent health beverage item |
| **22** | Hand Sanitizer Gel | High | 80.01 | High-demand hygiene and sanitizing product |
| **23** | Pure Maple Syrup | Medium-Low | 29.13 | Medium-low volume premium pancake topping |
| **24** | Fresh Avocados | Medium-High | 65.62 | Highly popular fresh fruit produce |
| **25** | Toothpaste (Mint Whitening) | High | 80.20 | Standard daily personal care item |
| **26** | Basmati Rice (5kg) | Medium | 47.31 | Staple grain with stable consumption |
| **27** | Aged Balsamic Vinegar | Low | 21.93 | Slow-moving specialty premium condiment |
| **28** | Heavy Duty Trash Bags | High | 87.38 | Top household utility consumable |
| **29** | Liquid Hand Soap Refill | High | 69.26 | Standard high-frequency bathroom consumable |
| **30** | Salted Potato Chips | Medium | 40.13 | High-frequency salty snack item |
| **31** | Cheddar Cheese Block | Medium-High | 58.31 | Highly popular refrigerated food item |
| **32** | Penne Pasta (500g) | Medium | 43.72 | Low-cost pasta dry grocery staple |
| **33** | Sparkling Water (12pk) | High | 69.14 | High-volume sugar-free beverage item |
| **34** | Pure Wildflower Honey | Medium-Low | 25.61 | Medium-low demand natural sweetener |
| **35** | Fresh Strawberries (1lb) | Medium-High | 65.37 | High-volume fresh berry produce |
| **36** | Aluminum Foil Roll | High | 76.60 | Standard high-demand kitchen wrapping product |
| **37** | Epsom Bath Salts | Medium-Low | 29.11 | Relaxing health and wellness product |
| **38** | Antibacterial Wipes | High | 80.03 | Very high-turnover surface sanitizing product |
| **39** | Marinara Pasta Sauce | Medium | 43.69 | Meal companion pasta sauce jar |
| **40** | Lavender Essential Oil | Medium-Low | 29.11 | Specialty aromatherapy personal care item |
| **41** | Organic Vanilla Extract | Low | 21.88 | Premium baking flavoring agent |
| **42** | Whole Bean Decaf Coffee | Medium | 36.45 | Specialty decaf hot beverage |
| **43** | Corn Tortillas (30ct) | Medium-High | 50.96 | Regular flatbread Mexican food staple |
| **44** | Hydrating Body Lotion | Medium-Low | 29.21 | Moderate-sales skin care moisturizer |
| **45** | Garbage Bin Liners | High | 80.11 | High-frequency waste disposal product |
| **46** | Flour Tortillas (10ct) | Medium-High | 58.36 | Regular flatbread staple |
| **47** | Himalayan Pink Salt | Low | 21.88 | Long-lasting specialty cooking salt |
| **48** | Fresh Gala Apples (3lb) | Medium-High | 51.04 | Standard fruit bag fresh produce |
| **49** | Organic Cane Sugar (2kg) | Medium-Low | 29.14 | Essential baking sweetener |
| **50** | Fresh Blueberries (6oz) | Medium-High | 65.45 | High-demand berry produce |