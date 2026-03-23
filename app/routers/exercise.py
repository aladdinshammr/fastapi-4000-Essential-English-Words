from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, models, database


router = APIRouter(
    prefix="/exercises",
    tags=["Exercises"],
)


@router.get(
    "/",
    response_model=List[schemas.Exercise],
    summary="Get Exercises",
    description="Returns a list of all or some exercises, change parameters if needed. ",
)
def get_exercises(
    unit_num: int = Query(None, ge=1, le=180),
    db: Session = Depends(database.get_db),
):
    exercise = ""
    if unit_num:
        exercise = (
            db.query(models.Exercise)
            .filter(
                (models.Exercise.unit_id == unit_num)
                & (models.Exercise.type == "exercise")
            )
            .all()
        )

    else:
        exercise = (
            db.query(models.Exercise).filter((models.Exercise.type == "exercise")).all()
        )

    return exercise


@router.get(
    "/answer-keys",
    response_model=List[schemas.AnswerKey] | schemas.AnswerKey,
    description="Returns a single or a list of exercises answers keys, change parameters if needed.",
)
def get_answer_keys(
    unit_num: int = Query(None, ge=1, le=180),
    db: Session = Depends(database.get_db),
):
    answer_key = ""
    if unit_num:
        answer_key = (
            db.query(models.Exercise)
            .filter(
                (models.Exercise.unit_id == unit_num)
                & (models.Exercise.type == "answer")
            )
            .first()
        )

    else:
        answer_key = (
            db.query(models.Exercise).filter((models.Exercise.type == "answer")).all()
        )

    return answer_key
