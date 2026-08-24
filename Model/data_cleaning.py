import os
import pickle
import pandas as pd
from sklearn.preprocessing import LabelEncoder

def clean_and_prepare_data(train_path, festivals_path, output_csv_path, encoders_pkl_path):
    """
    Cleans the store item demand forecasting data and merges it with festival information.
    Saves the cleaned dataset and fitted LabelEncoders.
    """
    print("Loading datasets...")
    df = pd.read_csv(train_path)
    fd = pd.read_excel(festivals_path)
    
    # Process dates
    df["date"] = pd.to_datetime(df['date'])
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["day"] = df["date"].dt.day
    df["weekday"] = df["date"].dt.day_name()
    
    fd["festival_date"] = pd.to_datetime(fd['festival_date'])
    
    # Merge datasets
    print("Merging sales and festival datasets...")
    big_d = pd.merge(df, fd, left_on="date", right_on="festival_date", how="left")
    
    # Ensure date fields are correctly extracted after merge
    big_d["year"] = big_d["date"].dt.year
    big_d["month"] = big_d["date"].dt.month
    big_d["day"] = big_d["date"].dt.day
    big_d["weekday"] = big_d["date"].dt.day_name()
    
    # Label encoding
    print("Encoding categorical columns...")
    encoders = {}
    cols_to_encode = {
        'festival_name': 'None',
        'weekday': None,         # Weekday has no NaNs
        'festival_type': 'None',
        'region': 'None',
        'impact_scale': 0        # Fill NaNs with 0 before encoding
    }
    
    for col, fill_val in cols_to_encode.items():
        le = LabelEncoder()
        if fill_val is not None:
            # We convert numerical/string values to standard string formatting for consistent encoding
            if col == 'impact_scale':
                series = big_d[col].fillna(fill_val).astype(int).astype(str)
            else:
                series = big_d[col].fillna(fill_val).astype(str)
        else:
            series = big_d[col].astype(str)
            
        big_d[col] = le.fit_transform(series)
        encoders[col] = le
        print(f"Encoded {col}: {dict(zip(le.classes_, le.transform(le.classes_)))}")
        
    # Save encoders for training / backend
    print(f"Saving encoders to {encoders_pkl_path}...")
    os.makedirs(os.path.dirname(encoders_pkl_path), exist_ok=True)
    with open(encoders_pkl_path, 'wb') as f:
        pickle.dump(encoders, f)
        
    # Generate festival date offsets (expanded window)
    print("Expanding festival dates to create offsets...")
    ldate = big_d["festival_date"].dropna().unique()
    offsets = range(-7, 4)
    
    fd_expanded = pd.DataFrame({
        "festival_date": [
            date + pd.Timedelta(days=offset)
            for date in ldate
            for offset in offsets
        ],
        "days_to_next_festival": [
            offset
            for date in ldate
            for offset in offsets
        ]
    })
    
    fd_expanded["is_festival_day"] = (
        fd_expanded["days_to_next_festival"] == 0
    ).astype("int8")
    
    fd_expanded["pre_festival_week"] = (
        fd_expanded["days_to_next_festival"].between(-7, 0)
    ).astype("int8")
    
    # Merge expanded window
    print("Merging expanded festival windows...")
    final_df = pd.merge(big_d, fd_expanded, left_on='date', right_on='festival_date', how='left')
    
    # Drop intermediate columns
    final_df.drop(["festival_date_x", "festival_date_y", "date"], axis=1, inplace=True)
    
    # Fill remaining nulls
    print("Filling missing values for non-festival days...")
    final_df["impact_scale"] = final_df["impact_scale"].fillna(0)
    final_df["is_festival_day"] = final_df["is_festival_day"].fillna(0)
    final_df["is_regional_event"] = final_df["is_regional_event"].fillna(0)
    final_df["days_to_next_festival"] = final_df["days_to_next_festival"].fillna(999)
    final_df["pre_festival_week"] = final_df["pre_festival_week"].fillna(0)
    
    # Save clean dataset
    print(f"Saving cleaned dataset to {output_csv_path}...")
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
    final_df.to_csv(output_csv_path, index=False)
    print("Data cleaning complete!")
    return final_df

if __name__ == "__main__":
    clean_and_prepare_data(
        train_path=r"d:\Final\Festivals\DataSet\train.csv",
        festivals_path=r"d:\Final\Festivals\DataSet\festivals_base.xlsx",
        output_csv_path=r"d:\Final\Festivals\DataSet\cleaned_data.csv",
        encoders_pkl_path=r"d:\Final\Festivals\Model\label_encoders.pkl"
    )
