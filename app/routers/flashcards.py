from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from .. import database, models, schemas


router = APIRouter(prefix="/flashcards", tags=["Flashcards"])


@router.get("/", response_model=List[schemas.Flashcard])
def get_flashcards(
    unit: int = Query(None, ge=1, le=180),
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(database.get_db),
):

    flashcards = ""
    if unit:
        flashcards = (
            db.query(models.Word)
            .filter(models.Word.unit_id == unit)
            .offset(skip)
            .limit(limit)
            .all()
        )
    else:
        flashcards = db.query(models.Word).offset(skip).limit(limit).all()

    if not flashcards:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="no more flashcards,try changing query params",
        )

    return flashcards


@router.get("/{flashcard}", response_model=schemas.Flashcard)
def get_flashcard_by_word(flashcard: str, db: Session = Depends(database.get_db)):
    word = db.query(models.Word).filter(models.Word.word == flashcard.lower()).first()
    if not word:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{flashcard} can not be found",
        )
    return word
