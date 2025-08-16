import os
from .client import post, now_utc
from dotenv import load_dotenv
load_dotenv()

TAG_ID = os.getenv("TAG_ID", "cat-001")

def upload_feeding_log(weight_g, amt_g, left_g, start_iso=None, end_iso=None, file_path=None):
    start_iso = start_iso or now_utc()
    end_iso = end_iso or now_utc()
    payload = {
        "tag_id": TAG_ID,
        "weight": float(weight_g),
        "timestamp_start": start_iso,
        "timestamp_end": end_iso,
        "feeding_amount": int(amt_g),
        "left_amount": int(left_g),
        "file_path": file_path,
    }
    return post("/api/feeding-logs", payload)
