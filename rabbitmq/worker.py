import sys
import json
import time
import requests
import threading
import os
import pika
import joblib 
from get_data import get_current_features1
from datetime import timedelta, datetime
from database import engine, get_db
from sqlalchemy import Column, Integer, String, Float, DateTime

exchange_name = 'ml_tasks'
queue_name = 'test'

credentials = pika.PlainCredentials('rmuser', 'rmpassword')
parameters = pika.ConnectionParameters(host='rabbitmq',
                                        port=5672,
                                        virtual_host='/',
                                        credentials=credentials,
                                        heartbeat=30,
                                        blocked_connection_timeout=2)

def callback(ch, method, properties, body):
    try:
        print(f"Получено сообщение с delivery_tag: {method.delivery_tag}") 

       
        class Prediction(Base):
            __tablename__ = "predictions"

            id = Column(Integer, primary_key=True, index=True)
            value = Column(Float)
            timestamp = Column(DateTime, default=datetime.utcnow) 
        
        try:

            ml_model = joblib.load("catboost_lr 0.38121, mae 0.1857300913901133 , mape 0.009344126631801567, rmse 0.10354896606489733.joblib")
            features = get_current_features1()
            
            if not features.empty and not features.isna().all().all():
                prediction = ml_model.predict(features)[0]
                current_time = datetime.utcnow()
                
                
                db = next(get_db())
                new_prediction = Prediction(
                    value=float(prediction),
                    timestamp=current_time
                )
                db.add(new_prediction)
                db.commit()
                
            
                
            

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при вызове ML сервиса: {e}")
            
            return 
    except Exception as e:
        print(f"Ошибка при обработке задачи: {e}")
       
def process_ml_task():
    try:
        
        print("Подключаемся к RabbitMQ...")
        connection = pika.BlockingConnection(parameters)
        print("Подключение успешно")
        channel = connection.channel()

        channel.queue_declare(queue=queue_name)

        channel.basic_consume(
            queue=queue_name,
            on_message_callback=callback,
            auto_ack=True
        )

        print(f" [*] Воркер {threading.current_thread().name} ожидает задач. Для выхода нажмите CTRL+C")
        channel.start_consuming()

    except Exception as e:
        print(f"Ошибка в process_ml_task: {e}", file=sys.stderr)

if __name__ == '__main__':
    try:
        print('Запускаемся')
        process_ml_task()
    except Exception as e:
        print(f"Необработанное исключение в main: {e}", file=sys.stderr)
        sys.exit(1)