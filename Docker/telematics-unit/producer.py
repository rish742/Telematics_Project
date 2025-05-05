from kafka import KafkaProducer
import json
import time
import random

producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

while True:
    data = {
        "vehicle_id": "V123",
        "speed": random.randint(0, 120),
        "fuel_level": random.uniform(10, 100),
        "timestamp": time.time()
    }
    producer.send('telematics', data)
    print(f"Sent: {data}")
    time.sleep(5)
