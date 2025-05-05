import time
import random
import json
import requests
import pandas as pd
from kafka import KafkaProducer
from joblib import load
import tomllib

# ==== CONFIG ====
with open("config.toml", "rb") as f:
    config = tomllib.load(f)

SUPABASE_URL = config["supabase"]["url"]
SUPABASE_KEY = config["supabase"]["key"]
SUPABASE_TABLE = config["supabase"].get("table", "telematics")
KAFKA_BROKER = config["kafka"]["broker"]
VEHICLE_TYPE = config["vehicle"]["type"]


# ==== LOAD MODEL ====
model = load("telematics_classifier.joblib")

# ==== SETUP KAFKA ====
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

# ==== SENSOR SIMULATION ====
def read_sensors():
    return {
        "timestamp": time.strftime('%Y-%m-%dT%H:%M:%S'),
        "latitude": round(random.uniform(32.1, 32.3), 6),
        "longitude": round(random.uniform(-111.0, -110.8), 6),
        "speed": random.randint(0, 120),
        "fuel_level": round(random.uniform(10, 100), 2),
        "engine_temp": random.randint(70, 120),
        "accelerometer_x": round(random.uniform(-3, 3), 2),
        "accelerometer_y": round(random.uniform(-3, 3), 2),
        "accelerometer_z": round(random.uniform(-3, 3), 2),
        "eye_closed_duration": round(random.uniform(0, 5), 2),
        "head_direction": round(random.uniform(-45, 45), 2),
        "head_tilt": round(random.uniform(-30, 30), 2)
    }


# ==== DRIVER STATE INFERENCE ====
def infer_driver_state(data):
    features = pd.DataFrame([{
        "fuel_level": data['fuel_level'],
        "engine_temp": data['engine_temp'],
        "eye_closed_duration": data['eye_closed_duration'],
        "head_tilt": data['head_tilt'],
        "head_direction": data['head_direction'],
        "speed": data['speed']
    }])

    prediction = model.predict(features)[0]
    return prediction

# ==== PUSH TO SUPABASE ====
def push_to_supabase(payload):
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.post(
        f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABLE}",
        headers=headers,
        json=payload
    )
    return response.status_code

distracted_start = None

# ==== MAIN LOOP ====
while True:
    data = read_sensors()
    data["driver_state"] = infer_driver_state(data)
    data["vehicle_type"] = VEHICLE_TYPE
    data["engine_overheat"] = data["engine_temp"] > 100
    data["speeding_flag"] = data["speed"] > 100
    data["vehicle_health"] = "needs_maintenance" if data["engine_temp"] > 100 else "normal"
    # Simulates harsh braking if random drop from prior speed > 20
    if "prev_speed" not in locals():
        prev_speed = data["speed"]
    data["harsh_braking"] = (prev_speed - data["speed"]) > 20
    prev_speed = data["speed"]
    data["fatigue_score"] = round(
        (data["eye_closed_duration"] / 5.0) * 0.6 +
        (abs(data["head_tilt"]) / 30.0) * 0.4, 2
    )

    # === 🔔 ALERT CHECK (Insert Here!) ===
    current_time = time.time()
    alerts = []

    if data["driver_state"] == "distracted":
        if distracted_start is None:
            distracted_start = current_time
        elif current_time - distracted_start >= 30:
            alerts.append("🚨 Driver distracted for over 30 seconds")
    else:
        distracted_start = None


    if data["driver_state"] == "drowsy":
        alerts.append("⚠️ Driver appears drowsy")
    if data["engine_overheat"]:
        alerts.append("🔥 Engine overheating!")
    if data["harsh_braking"]:
        alerts.append("🛑 Harsh braking detected")
    if data["speeding_flag"]:
        alerts.append("🚓 Speeding detected")

    if alerts:
        for alert in alerts:
            print(alert)

    # Send to Kafka & Supabase
    producer.send("telematics", value=data)
    status = push_to_supabase(data)

    print(f"Pushed to Kafka and Supabase ({status}): {data}")
    time.sleep(5)
