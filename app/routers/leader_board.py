from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, desc
from sqlalchemy.orm import Session
from .. import models, schemas, database

router = APIRouter(prefix="/leaderboards", tags=["Leaderboard"])


@router.get("/", response_model=list[schemas.LeaderboardEntry])
def leaderboard(
    limit: int = Query(10, ge=1, le=100), db: Session = Depends(database.get_db)
):
    results = (
        db.query(
            models.User.id,
            models.User.email,
            func.count(models.LearnedWord.id).label("learned_count"),
        )
        .join(models.LearnedWord, models.User.id == models.LearnedWord.user_id)
        .group_by(models.User.id)
        .order_by(desc("learned_count"))
        .limit(limit)
        .all()
    )

    return [
        schemas.LeaderboardEntry(user_id=r[0], email=r[1], learned_count=r[2])
        for r in results
    ]
