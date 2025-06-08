# Dockerfile.worker

FROM python:3.11

WORKDIR /app

COPY ./app /app/app
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "-u", "app/consumer.py"]