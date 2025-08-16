import os
from .client import get
from dotenv import load_dotenv
load_dotenv()
TAG_ID = os.getenv("TAG_ID", "cat-001")

def fetch_plan():
    return get(f"/api/cats/{TAG_ID}/plan")
