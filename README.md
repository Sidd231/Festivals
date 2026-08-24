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