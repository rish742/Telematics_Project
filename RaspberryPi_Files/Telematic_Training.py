import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from joblib import dump

# Load labeled training data
df = pd.read_csv("tucson_telematics_1000_enhanced.csv")

# Select features and target
X = df[["fuel_level", "engine_temp", "eye_closed_duration", "head_tilt", "head_direction", "speed"]]
y = df["driver_state"]

# Train model
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2)
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# Save model
dump(model, "telematics_classifier.joblib")
print("✅ Model saved as telematics_classifier.joblib")
