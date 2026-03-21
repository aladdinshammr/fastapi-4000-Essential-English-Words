from fastapi import APIRouter, Depends, HTTPException, status, Query
from .. import schemas, database, models
from sqlalchemy.orm import Session
from typing import List


router = APIRouter(prefix="/stories", tags=["Reading"])


@router.get("/", response_model=schemas.Story | List[schemas.Story])
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


@router.get("/comprehension", response_model=List[schemas.Exercise])
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


@router.get("/answer-key", response_model=List[schemas.AnswerKey] | schemas.AnswerKey)
def get_answer_key(
    unit_num: int = Query(None, ge=1, le=180),
    db: Session = Depends(database.get_db),
):
    answer_key = ""
    if unit_num:
        answer_key = (
            db.query(models.Reading)
            .filter(
                (models.Reading.type == None) & (models.Reading.unit_id == unit_num)
            )
            .first()
        )

    else:
        answer_key = (
            db.query(models.Reading).filter((models.Reading.type == None)).all()
        )

    return answer_key
