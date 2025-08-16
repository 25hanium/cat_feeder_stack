from sqlalchemy.orm import declarative_base, relationship, Mapped, mapped_column
from sqlalchemy import Integer, Float, String, DateTime, ForeignKey, Index, func, Date, cast

Base = declarative_base()

class Cat(Base):
    __tablename__ = "cats"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str | None] = mapped_column(String(50))
    age: Mapped[int | None] = mapped_column(Integer)
    gender: Mapped[str | None] = mapped_column(String(10))
    food_favor: Mapped[str | None] = mapped_column(String(50))
    feeding_time: Mapped[DateTime | None] = mapped_column(DateTime)
    feeding_amount: Mapped[int | None] = mapped_column(Integer)
    tag_id: Mapped[str | None] = mapped_column(String(50), unique=True, index=True)
    feedings = relationship("FeedingLog", back_populates="cat")

class FeedingLog(Base):
    __tablename__ = "feeding_logs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    cat_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("cats.id", ondelete="SET NULL"))
    weight: Mapped[float | None] = mapped_column(Float)
    timestamp_start: Mapped[DateTime | None] = mapped_column(DateTime, server_default=func.now())
    timestamp_end: Mapped[DateTime | None] = mapped_column(DateTime, server_default=func.now())
    feeding_amount: Mapped[int | None] = mapped_column(Integer)
    left_amount: Mapped[int | None] = mapped_column(Integer)
    file_path: Mapped[str | None] = mapped_column(String(255))
    cat = relationship("Cat", back_populates="feedings")

Index("ix_feeding_logs_cat_time", FeedingLog.cat_id, FeedingLog.timestamp_start)

class FeedingInfo(Base):
    __tablename__ = "feeding_info"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    feeding_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("feeding_logs.id", ondelete="CASCADE"))
    cat_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("cats.id", ondelete="SET NULL"))
    behavior: Mapped[str | None] = mapped_column(String(50))

class FeedingLimit(Base):
    __tablename__ = "feeding_limits"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    cat_id: Mapped[int] = mapped_column(Integer, ForeignKey("cats.id", ondelete="CASCADE"))
    max_amount_per_meal: Mapped[float | None] = mapped_column(Float)
    max_meals_per_day: Mapped[int | None] = mapped_column(Integer)

class FeederState(Base):
    __tablename__ = "feeder_state"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    timestamp: Mapped[DateTime | None] = mapped_column(DateTime, server_default=func.now())
    left_amount: Mapped[int | None] = mapped_column(Integer)
