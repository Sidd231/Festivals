import os
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import xgboost as xg
from sklearn.metrics import mean_absolute_error, r2_score

def train_and_save_models(cleaned_csv_path, xgboost_output_path, rf_output_path):
    """
    Loads the cleaned dataset, splits the data by year (pre-2017 for training, 2017 for testing),
    trains RandomForestRegressor and XGBRegressor, evaluates them, and saves the trained models.
    """
    print(f"Loading cleaned dataset from {cleaned_csv_path}...")
    final_df = pd.read_csv(cleaned_csv_path)
    
    # Dividing data by year (matching the notebook)
    print("Splitting data into train and test sets based on year...")
    train_data = final_df[final_df["year"] < 2017]
    test_data = final_df[final_df["year"] == 2017]
    
    # X and y split
    X_train_full = train_data.drop(["sales"], axis=1)
    y_train_full = train_data["sales"]
    
    X_test_val = test_data.drop(["sales"], axis=1)
    y_test_val = test_data["sales"]
    
    # Internal validation split (80/20 train_test_split as in notebook)
    X_train, X_val, y_train, y_val = train_test_split(
        X_train_full, y_train_full, test_size=0.2, random_state=42
    )
    
    # 1. Random Forest Regressor
    print("\n--- Training Random Forest Regressor ---")
    rf = RandomForestRegressor(
        n_estimators=100,
        max_features="sqrt",
        random_state=42,
        n_jobs=-1
    )
    rf.fit(X_train, y_train)
    
    # RF predictions on 2017 test set
    rf_preds = rf.predict(X_test_val)
    rf_mae = mean_absolute_error(y_test_val, rf_preds)
    rf_r2 = r2_score(y_test_val, rf_preds)
    print(f"Random Forest - Test Set (2017) MAE: {rf_mae:.2f}")
    print(f"Random Forest - Test Set (2017) R² Score: {rf_r2:.2f}")
    
    # 2. XGBoost Regressor
    print("\n--- Training XGBoost Regressor ---")
    XGmodel = xg.XGBRegressor(
        n_estimators=100,
        random_state=42,
        n_jobs=-1
    )
    XGmodel.fit(X_train, y_train)
    
    # XGBoost predictions on 2017 test set
    xg_preds = XGmodel.predict(X_test_val)
    xg_mae = mean_absolute_error(y_test_val, xg_preds)
    xg_r2 = r2_score(y_test_val, xg_preds)
    print(f"XGBoost - Test Set (2017) MAE: {xg_mae:.2f}")
    print(f"XGBoost - Test Set (2017) R² Score: {xg_r2:.2f}")
    
    # Save the models
    print(f"\nSaving XGBoost model to {xgboost_output_path}...")
    os.makedirs(os.path.dirname(xgboost_output_path), exist_ok=True)
    with open(xgboost_output_path, "wb") as f:
        pickle.dump(XGmodel, f)
        
    print(f"Saving Random Forest model to {rf_output_path}...")
    os.makedirs(os.path.dirname(rf_output_path), exist_ok=True)
    with open(rf_output_path, "wb") as f:
        pickle.dump(rf, f)
        
    print("Model training and saving complete!")

if __name__ == "__main__":
    train_and_save_models(
        cleaned_csv_path=r"d:\Final\Festivals\DataSet\cleaned_data.csv",
        xgboost_output_path=r"d:\Final\Festivals\backend\XGmodel.pkl",
        rf_output_path=r"d:\Final\Festivals\backend\RandomFroest.pkl"
    )
