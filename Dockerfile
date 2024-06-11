FROM python:3.12.4-alpine3.20

WORKDIR /app

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY dynamo_to_s3.py .

CMD ["python3", "dynamo_to_s3.py"]
