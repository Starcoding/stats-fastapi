from fastapi import Depends, FastAPI
from sqlalchemy.future import select
from sqlalchemy import desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session, init_db, clear_db
from app.models import Statistic, StatisticCreate
from datetime import date
from typing import Optional

app = FastAPI()

FIELDS = ("views", "clicks", "cost", "cpc", "cpm", "id")


@app.on_event("startup")
async def on_startup():
    await init_db()


@app.get("/stats", response_model=list[Statistic])
async def get_stats(
    from_date: date,
    to_date: date,
    sort: Optional[str] = None,
    sort_by_desc: Optional[bool] = False,
    session: AsyncSession = Depends(get_session),
):
    if sort in FIELDS:
        query = (
            select(Statistic)
            .where(Statistic.date >= from_date, Statistic.date <= to_date)
            .order_by(getattr(Statistic, sort))
        )
        if sort_by_desc:
            query = (
                select(Statistic)
                .where(Statistic.date >= from_date, Statistic.date <= to_date)
                .order_by(desc(getattr(Statistic, sort)))
            )
    else:
        query = (
            select(Statistic)
            .where(Statistic.date >= from_date, Statistic.date <= to_date)
            .order_by(Statistic.date)
        )
    result = await session.execute(query)
    stats = result.scalars()
    return [
        Statistic(
            id=stat.id,
            date=stat.date,
            views=stat.views,
            clicks=stat.clicks,
            cost=stat.cost,
            cpc=stat.cpc,
            cpm=stat.cpm,
        )
        for stat in stats
    ]


@app.post(
    "/stats",
    response_model=Statistic,
)
async def add_stat(
    date: date,
    views: Optional[int] = None,
    clicks: Optional[int] = None,
    cost: Optional[float] = None,
    session: AsyncSession = Depends(get_session),
):
    statistic_record = Statistic(date=date, views=views, clicks=clicks, cost=cost)
    if clicks == 0:
        statistic_record.cpc = 0.0
    else:
        statistic_record.cpc = cost / clicks
    if views == 0:
        statistic_record.cpm = 0.0
    else:
        statistic_record.cpm = cost / views * 1000
    session.add(statistic_record)
    await session.commit()
    await session.refresh(statistic_record)
    return statistic_record


@app.delete("/stats")
async def delete_stats(session: AsyncSession = Depends(get_session)):
    result = await clear_db()
    return "Successfully deleted stats."
