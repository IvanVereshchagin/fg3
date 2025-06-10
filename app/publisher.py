

def send_prediction_task():
    import pika
    import json
    task = {"task": "predict"}  
    credentials = pika.PlainCredentials("rmuser", "rmpassword")
    parameters = pika.ConnectionParameters(
        host="rabbitmq",
        port=5672,
        virtual_host="/",
        credentials=credentials,
    )
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue="ml_tasks", durable=True)
    channel.basic_publish(
        exchange="",
        routing_key="ml_tasks",
        body=json.dumps(task),
        properties=pika.BasicProperties(delivery_mode=2),
    )
    print("[x] Task sent")
    connection.close()