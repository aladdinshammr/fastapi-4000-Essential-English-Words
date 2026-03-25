from fastapi import APIRouter, Depends, HTTPException, status, Query
from .. import schemas, database, models
from sqlalchemy.orm import Session
from typing import List


router = APIRouter(prefix="/stories", tags=["Readings (Stroies)"])


@router.get(
    "/",
    response_model=schemas.Story | List[schemas.Story],
    description="Get a list of stories or a single story",
)
def get_stories(
    unit_num: int = Query(None, ge=1, le=180),
    db: Session = Depends(database.get_db),
):
    stories = ""
    if unit_num:
        stories = (
            db.query(models.Reading)
            .filter(
                (models.Reading.type == "story") & (models.Reading.unit_id == unit_num)
            )
            .first()
        )
    else:
        stories = db.query(models.Reading).filter(models.Reading.type == "story").all()

    return stories


@router.get(
    "/comprehension",
    response_model=List[schemas.Exercise] | schemas.Exercise,
    description="Get a list of reading comprehension exercises,change parameters if needed",
)
def get_reading_comprehension(
    unit_num: int = Query(None, ge=1, le=180),
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(database.get_db),
):
    reading_comperhention = ""
    if unit_num:
        reading_comperhention = (
            db.query(models.Reading)
            .filter(
                (models.Reading.type == "faq") & (models.Reading.unit_id == unit_num)
            )
            .offset(skip)
            .limit(limit)
            .first()
        )
    else:
        reading_comperhention = (
            db.query(models.Reading)
            .filter(models.Reading.type == "faq")
            .offset(skip)
            .limit(limit)
            .all()
        )
    if not reading_comperhention:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="no more flashcards,try changing query params",
        )
    return reading_comperhention


@router.get(
    "/answer-keys",
    response_model=List[schemas.AnswerKey] | schemas.AnswerKey,
    description="returns a list of reading comperhension answer keys change parameters if needed",
)
def get_answer_keys(
    unit_num: int = Query(None, ge=1, le=180),
    db: Session = Depends(database.get_db),
):
    answer_key = ""
    if unit_num:
        answer_key = (
            db.query(models.Reading)
            .filter(
                (models.Reading.type == "answer") & (models.Reading.unit_id == unit_num)
            )
            .first()
        )

    else:
        answer_key = (
            db.query(models.Reading).filter((models.Reading.type == "answer")).all()
        )

    return answer_key
