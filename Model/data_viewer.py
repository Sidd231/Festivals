import os
import pickle
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def show_dataset_info(train_path, festivals_path, cleaned_path, encoders_pkl_path, model_pkl_path, output_plot_path):
    """
    Diagnostic script to print dataset shapes, details, missing values,
    label encoder mappings, and generate a feature importance plot.
    """
    print("="*60)
    print("Dataset Diagnostics and Exploration")
    print("="*60)
    
    # 1. Print info on raw datasets
    if os.path.exists(train_path):
        train_df = pd.read_csv(train_path)
        print(f"Raw Sales Data Shape: {train_df.shape}")
        print(f"Raw Sales Columns: {list(train_df.columns)}")
    else:
        print(f"Raw Sales Data not found at {train_path}")
        
    if os.path.exists(festivals_path):
        festivals_df = pd.read_excel(festivals_path)
        print(f"Raw Festivals Data Shape: {festivals_df.shape}")
        print(f"Raw Festivals Columns: {list(festivals_df.columns)}")
    else:
        print(f"Raw Festivals Data not found at {festivals_path}")
        
    # 2. Print info on cleaned dataset
    if os.path.exists(cleaned_path):
        cleaned_df = pd.read_csv(cleaned_path)
        print(f"\nCleaned Dataset Shape: {cleaned_df.shape}")
        print("\nCleaned Dataset Missing Values Count:")
        print(cleaned_df.isnull().sum())
        print("\nCleaned Dataset Preview (First 5 rows):")
        print(cleaned_df.head())
    else:
        print(f"\nCleaned dataset not found at {cleaned_path}")
        
    # 3. Print Label Encoder Mappings
    if os.path.exists(encoders_pkl_path):
        print("\n" + "="*40)
        print("Label Encoder Mappings")
        print("="*40)
        with open(encoders_pkl_path, 'rb') as f:
            encoders = pickle.load(f)
        for col, le in encoders.items():
            print(f"\nMappings for column '{col}':")
            for idx, val in enumerate(le.classes_):
                print(f"  {val} -> {idx}")
    else:
        print(f"\nLabel encoders not found at {encoders_pkl_path}")
        
    # 4. Generate Feature Importance Plot
    if os.path.exists(model_pkl_path) and os.path.exists(cleaned_path):
        print("\n" + "="*40)
        print("Generating XGBoost Feature Importances Plot")
        print("="*40)
        
        with open(model_pkl_path, 'rb') as f:
            model = pickle.load(f)
            
        cleaned_df = pd.read_csv(cleaned_path)
        X = cleaned_df.drop(["sales"], axis=1)
        
        importances = model.feature_importances_
        feature_imp_df = pd.DataFrame({
            'Feature': X.columns,
            'Importance': importances
        }).sort_values(by='Importance', ascending=False)
        
        # Plot
        plt.figure(figsize=(12, 6))
        sns.barplot(x='Importance', y='Feature', data=feature_imp_df, palette='viridis')
        plt.title('XGBoost Feature Importance')
        plt.xlabel('Importance Score')
        plt.ylabel('Features')
        plt.tight_layout()
        
        os.makedirs(os.path.dirname(output_plot_path), exist_ok=True)
        plt.savefig(output_plot_path)
        print(f"Plot saved successfully to: {output_plot_path}")
        plt.close()
    else:
        print(f"\nTrained model or cleaned dataset not found. Skipping feature importance plot.")
        
    print("\n"+"="*60)

if __name__ == "__main__":
    show_dataset_info(
        train_path=r"d:\Final\Festivals\DataSet\train.csv",
        festivals_path=r"d:\Final\Festivals\DataSet\festivals_base.xlsx",
        cleaned_path=r"d:\Final\Festivals\DataSet\cleaned_data.csv",
        encoders_pkl_path=r"d:\Final\Festivals\Model\label_encoders.pkl",
        model_pkl_path=r"d:\Final\Festivals\backend\XGmodel.pkl",
        output_plot_path=r"d:\Final\Festivals\Model\feature_importance.png"
    )
