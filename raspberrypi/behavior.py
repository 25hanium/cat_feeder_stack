import os
from .client import post
from dotenv import load_dotenv
load_dotenv()
TAG_ID = os.getenv("TAG_ID", "cat-001")

def report_behavior(behavior: str, feeding_log_id: int | None = None):
    return post("/api/feeding-info", {
        "tag_id": TAG_ID,
        "feeding_log_id": feeding_log_id,
        "behavior": behavior
    })
