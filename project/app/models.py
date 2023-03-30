from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import date as dt_date


class StatisticBase(SQLModel):
    date: dt_date
    views: Optional[int] = None
    clicks: Optional[int] = None
    cost: Optional[float] = None


class Statistic(StatisticBase, table=True):
    id: int = Field(default=None, primary_key=True)
    cpc: float
    cpm: float


class StatisticCreate(StatisticBase):
    pass
