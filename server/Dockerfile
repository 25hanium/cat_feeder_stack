FROM python:3.11-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# tzdata for TZ
RUN apt-get update && apt-get install -y --no-install-recommends tzdata && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY .env ./.env

ENV TZ=Asia/Seoul

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
