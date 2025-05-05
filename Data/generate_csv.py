import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Load dataset (adjust path if needed)
df = pd.read_csv("raspberrypi_telematics_dataset.csv", nrows=1000)

# Rename head position columns
df = df.rename(columns={
    "head_position_X": "head_direction",
    "head_position_Y": "head_tilt"
})

# Tucson, Arizona GPS bounding box
lat_bounds = (32.1, 32.3)
lon_bounds = (-111.0, -110.8)

np.random.seed(42)
df['latitude'] = np.random.uniform(lat_bounds[0], lat_bounds[1], len(df))
df['longitude'] = np.random.uniform(lon_bounds[0], lon_bounds[1], len(df))

# Simulate head movements
df['head_direction'] = np.random.normal(loc=0, scale=15, size=len(df))
df['head_tilt'] = np.random.normal(loc=0, scale=10, size=len(df))

# Create timestamps spaced 5 seconds apart
base_time = datetime.now()
df['timestamp'] = [(base_time - timedelta(seconds=5 * i)).isoformat() for i in range(len(df))]

# Add flag: engine_overheat if engine_temp > 100
df['engine_overheat'] = df['engine_temp'] > 100

# Add flag: harsh_braking if speed drops > 20 km/h compared to previous row
df['prev_speed'] = df['speed'].shift(1)
df['harsh_braking'] = (df['prev_speed'] - df['speed']) > 20
df['harsh_braking'] = df['harsh_braking'].fillna(False)

# Compute fatigue_score (range approx 0–1)
df['fatigue_score'] = (
    (df['eye_closed_duration'] / df['eye_closed_duration'].max()) * 0.6 +
    (np.abs(df['head_tilt']) / df['head_tilt'].max()) * 0.4
).round(2)

# Drop helper column
df = df.drop(columns=['prev_speed'])

# Add speeding_flag if speed > threshold (e.g., 100 km/h)
df['speeding_flag'] = df['speed'] > 100

def classify_driver(row):
    if row['eye_closed_duration'] >= 3 or row['fatigue_score'] >= 0.6:
        return "drowsy"
    elif abs(row['head_direction']) > 20 or abs(row['head_tilt']) > 15:
        return "distracted"
    else:
        return "awake"

df['driver_state'] = df.apply(classify_driver, axis=1)


# Save result
df.to_csv("tucson_telematics_1000_enhanced.csv", index=False)
print("✅ File saved as tucson_telematics_1000_enhanced.csv")
