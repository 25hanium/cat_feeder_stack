import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func, cast, Date
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from .database import engine
from .models import Base, Cat, FeedingLog, FeedingInfo, FeedingLimit, FeederState
from .schemas import FeedingLogIn, FeederStateIn, FeedingInfoIn, PlanOut
from .deps import get_db, require_api_key

load_dotenv()

app = FastAPI(title="Cat Feeder API")

app.include_router(feeding.router, prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auto create tables on first run if enabled
if os.getenv("AUTO_CREATE_TABLES", "false").lower() in ("true", "1", "yes"):
    Base.metadata.create_all(bind=engine)

@app.get("/health")
def health(db: Session = Depends(get_db)):
    try:
        db.execute(func.now().select())  # lightweight check
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"ok": True}

@app.post("/api/feeding-logs")
def create_feeding_log(payload: FeedingLogIn, db: Session = Depends(get_db), _=Depends(require_api_key)):
    cat = db.query(Cat).filter(Cat.tag_id == payload.tag_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="cat not found for tag_id")
    log = FeedingLog(
        cat_id=cat.id,
        weight=payload.weight,
        timestamp_start=payload.timestamp_start,
        timestamp_end=payload.timestamp_end,
        feeding_amount=payload.feeding_amount,
        left_amount=payload.left_amount,
        file_path=payload.file_path,
    )
    db.add(log); db.commit(); db.refresh(log)
    return {"id": log.id}

@app.post("/api/feeder-state")
def report_state(payload: FeederStateIn, db: Session = Depends(get_db), _=Depends(require_api_key)):
    st = FeederState(left_amount=payload.left_amount)
    db.add(st); db.commit()
    return {"ok": True}

@app.post("/api/feeding-info")
def report_behavior(payload: FeedingInfoIn, db: Session = Depends(get_db), _=Depends(require_api_key)):
    cat = db.query(Cat).filter(Cat.tag_id == payload.tag_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="cat not found")
    info = FeedingInfo(feeding_id=payload.feeding_log_id, cat_id=cat.id, behavior=payload.behavior)
    db.add(info); db.commit(); db.refresh(info)
    return {"id": info.id}

@app.get("/api/cats/{tag_id}/plan", response_model=PlanOut)
def get_plan(tag_id: str, db: Session = Depends(get_db), _=Depends(require_api_key)):
    cat = db.query(Cat).filter(Cat.tag_id == tag_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="cat not found")

    limit = db.query(FeedingLimit).filter(FeedingLimit.cat_id == cat.id).first()

    today = func.current_date()
    total_amt_today, meals_today = db.query(
        func.coalesce(func.sum(FeedingLog.feeding_amount), 0),
        func.count(FeedingLog.id),
    ).filter(
        FeedingLog.cat_id == cat.id,
        cast(FeedingLog.timestamp_start, Date) == today
    ).first()

    allowed_amt = None
    meals_left = None
    if limit:
        meals_left = max((limit.max_meals_per_day or 0) - (meals_today or 0), 0)
        if limit.max_amount_per_meal is not None:
            base = cat.feeding_amount if cat.feeding_amount is not None else limit.max_amount_per_meal
            allowed_amt = int(min(limit.max_amount_per_meal, base))

    return PlanOut(
        feeding_time=cat.feeding_time,
        feeding_amount=cat.feeding_amount,
        limits={
            "max_amount_per_meal": getattr(limit, "max_amount_per_meal", None) if limit else None,
            "max_meals_per_day": getattr(limit, "max_meals_per_day", None) if limit else None,
            "meals_today": meals_today,
            "total_amount_today": total_amt_today,
        },
        allowed_amount_now=allowed_amt,
        meals_left_today=meals_left,
    )
