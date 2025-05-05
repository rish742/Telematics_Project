# 🚗 AI-Powered Telematics System

This project is a real-time telematics monitoring and analysis system that simulates vehicle sensor data, predicts driver behavior using Edge AI on Raspberry Pi, streams data to a Kafka broker, and displays live insights via a Streamlit dashboard. All data is logged to Supabase for long-term storage and querying.

---

## 📁 Project Structure

```
Telematics_Project/
├── Data/                    # Raw & generated datasets
├── Docker/                  # Kafka + Zookeeper Docker setup
├── Docs/                    # Architecture diagrams and documentation
├── Models/                  # Trained model artifacts and metadata
├── RaspberryPi_Files/      # Sensor simulator, ML inference, Supabase & Kafka integration
├── Streamlit_Dashboard/    # Live vehicle dashboard with filtering and analytics
├── README.md                # This file
```

---

## 🚦 Features

- **📡 Sensor Simulator**: Generates realistic data (location, fatigue, speed, etc.)
- **🤖 Edge AI (RandomForest)**: Predicts driver state (`awake`, `drowsy`, `distracted`)
- **🔥 Real-time Kafka Streaming**: Publishes telematics data to Kafka topics
- **📊 Streamlit Dashboard**: Displays location, risk factors, and historical metrics
- **☁️ Supabase Integration**: Stores all data for persistence and querying
- **📍 Tucson-AZ Based GPS**: GPS points generated around Tucson, AZ

---

## 🛠️ How to Run

### 📦 1. Backend Setup (Raspberry Pi or Local)

```bash
cd RaspberryPi_Files
pip install -r requirements.txt
python app.py
```

🔧 Configure `config.toml` with your Kafka and Supabase credentials.

---

### 🐳 2. Start Kafka Services

```bash
cd Docker
docker-compose up -d
```

Kafka runs on ports `9092`/`9093`, Zookeeper on `2181`.

---

### 📊 3. Launch Streamlit Dashboard

```bash
cd Streamlit_Dashboard
streamlit run streamlit_app.py
```

> Make sure `.streamlit/secrets.toml` contains your Supabase credentials.

---

## 🧠 Machine Learning

- Trained using: `RandomForestClassifier`
- Model: `telematics_classifier.joblib`
- Features used:
  - `fuel_level`, `engine_temp`, `eye_closed_duration`, `head_tilt`, `head_direction`, `speed`
- Target: `driver_state`

---

## 📉 Dashboard Highlights

- Real-time map of vehicle GPS points
- Fatigue & distraction detection with alerts
- Vehicle health tracking (e.g., engine temp, fuel level)
- Accelerometer-based harsh braking detection

---

## 📂 Datasets

- `tucson_telematics_1000_enhanced.csv`: 1000 synthetic but realistic rows of vehicle and driver data
- Reproducible via: `Data/generate_csv.py`

---

## 📌 Future Improvements

- 📲 Mobile-friendly UI
- 🧠 More advanced ML model (e.g., LSTM for time series)
- 🚗 Real CAN bus integration on hardware
- 🔔 Email/SMS alerts on fatigue detection

---

## 🙌 Credits

- Developed by: Rishab RK, Hsing I Wang
- Supabase, Streamlit, Confluent Kafka, scikit-learn