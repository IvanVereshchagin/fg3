import pika
import json
import joblib
import pandas as pd
import time
from sqlalchemy.orm import Session
from datetime import datetime
from app import models
from app.database import get_db, engine
from app.main import get_current_features1

print("[*] ML worker started")

# Load model once
model = joblib.load('catboost_lr 0.38121, mae 0.1857300913901133 , mape 0.009344126631801567, rmse 0.10354896606489733.joblib')

def handle_task(ch, method, properties, body):
    try:
        print("[x] Task received")
        features = get_current_features1()

        if features.empty or features.isna().all().all():
            print("[!] Features are empty or invalid")
            return

        prediction = model.predict(features)[0]
        db = next(get_db())

        new_prediction = models.Prediction(
            value=float(prediction),
            timestamp=datetime.utcnow()
        )
        db.add(new_prediction)
        db.commit()
        print(f"[✓] Prediction saved: {prediction}")
    except Exception as e:
        print(f"[!] Error: {e}")

def start_worker():
    credentials = pika.PlainCredentials("rmuser", "rmpassword")
    parameters = pika.ConnectionParameters(
        host="rabbitmq",
        port=5672,
        virtual_host="/",
        credentials=credentials,
        heartbeat=30,
        blocked_connection_timeout=5
    )
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue="ml_tasks", durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue="ml_tasks", on_message_callback=handle_task, auto_ack=True)

    print("[*] Waiting for ML tasks. To exit press CTRL+C")
    channel.start_consuming()

if __name__ == "__main__":
    start_worker()