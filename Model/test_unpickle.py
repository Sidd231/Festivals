import pickle


with open("XGmodel.pkl", "rb") as f:
    model = pickle.load(f)

print(type(model))         
print(model)                

if hasattr(model, "n_features_in_"):
    print("Number of features:", model.n_features_in_)

if hasattr(model, "feature_names_in_"):
    print("Feature names:", model.feature_names_in_)