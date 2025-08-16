import os, time, requests
from dotenv import load_dotenv
from datetime import datetime, timezone

load_dotenv()

BASE = os.getenv("SERVER_BASE_URL", "").rstrip("/")
API_KEY = os.getenv("API_KEY")
HEAD = {"X-API-Key": API_KEY}

def now_utc():
    return datetime.now(timezone.utc).isoformat()

def post(path, data, retries=3):
    url = f"{BASE}{path}"
    for i in range(retries):
        try:
            r = requests.post(url, headers=HEAD, json=data, timeout=5)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            if i == retries - 1:
                raise
            time.sleep(2)

def get(path):
    url = f"{BASE}{path}"
    r = requests.get(url, headers=HEAD, timeout=5)
    r.raise_for_status()
    return r.json()
