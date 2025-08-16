from pydantic import BaseModel
from datetime import datetime

class FeedingLogIn(BaseModel):
    tag_id: str
    weight: float | None = None
    timestamp_start: datetime
    timestamp_end: datetime
    feeding_amount: int
    left_amount: int
    file_path: str | None = None

class FeederStateIn(BaseModel):
    left_amount: int

class FeedingInfoIn(BaseModel):
    tag_id: str
    feeding_log_id: int | None = None
    behavior: str

class PlanOut(BaseModel):
    feeding_time: datetime | None = None
    feeding_amount: int | None = None
    limits: dict
    allowed_amount_now: int | None = None
    meals_left_today: int | None = None
