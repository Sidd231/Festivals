# Festive Demand Forecast AI

An AI-powered demand forecasting application that uses a trained XGBoost regression model to predict store-item demand based on store, item, date, and festival/regional context (festival name, festival type, region, impact scale, and proximity to upcoming festivals).

## Tech Stack

**Backend**
- Python
- Flask + Flask-CORS
- XGBoost
- Scikit-learn
- Pandas / NumPy

**Frontend**
- React (Vite)
- Tailwind CSS

**Modeling**
- Jupyter Notebooks (data cleaning + model training)

## Project Structure

```text
Festivals/
├── backend/
│   ├── app.py                 # Flask app — /api/predict, /api/model-info
│   ├── routes/                # (reserved for route modules)
│   ├── services/              # (reserved for service modules)
│   └── test_unpickle.py
├── frontend/                  # React + Vite + Tailwind app
│   ├── index.html
│   ├── src/
│   │   ├── App.jsx
│   │   ├── components/        # Navbar, Hero, PredictWorkspace, ResultCard, etc.
│   │   └── services/
│   │       └── api.js         # Calls the Flask backend
│   ├── package.json
│   └── vite.config.js
├── Model/
│   ├── Cleaning.ipynb          # Data cleaning / preprocessing notebook
│   ├── Festival_model.ipynb    # Model training notebook
│   └── ML model/
│       └── XGmodel.pkl         # Serialized trained XGBoost model
├── DataSet/
│   ├── train.csv               # Historical store-item sales data
│   └── festivals_base.xlsx     # Festival and regional event metadata
├── requirements.txt
├── .gitignore
└── README.md
```

## Setup and Installation

### Backend
```bash
pip install -r requirements.txt
cd backend
python app.py
```
Server starts at `http://127.0.0.1:5000`

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## How It Works

1. The React frontend collects store, item, date, and festival details through the prediction form.
2. On submit, `services/api.js` sends a request to the Flask backend (`/api/predict`).
3. The backend encodes the categorical fields (festival name, festival type, region, weekday) into the numeric format the model expects and builds the 14-feature input row.
4. The serialized XGBoost model (`Model/ML model/XGmodel.pkl`) generates a prediction.
5. The predicted demand value is returned as JSON and displayed on the frontend.

## API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | Health check — confirms the server and model are running |
| `/api/model-info` | GET | Returns model type, feature list, and valid dropdown options |
| `/api/predict` | POST | Accepts the 14 input fields and returns the predicted demand |
