import os
import pickle

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "Model", "ML model", "XGmodel.pkl")

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

print(type(model))         
print(model)                

if hasattr(model, "n_features_in_"):
    print("Number of features:", model.n_features_in_)

if hasattr(model, "feature_names_in_"):
    print("Feature names:", model.feature_names_in_)