from fastapi import APIRouter, Depends, Path, HTTPException, status
from sqlalchemy.orm import Session
from enum import Enum
from typing import List


from .. import database, models, schemas


class BookNum(int, Enum):
    book1 = 1
    book2 = 2
    book3 = 3
    book4 = 4
    book5 = 5
    book6 = 6


router = APIRouter(tags=["Indexes"], prefix="/indexes")


@router.get(
    "/book/{book_num}",
    response_model=List[schemas.Words],
    description="Returns a list of words which every book covers",
)
def get_words_by_book(
    book_num: BookNum,
    db: Session = Depends(database.get_db),
):
    words = db.query(models.Index).filter(models.Index.book == book_num).all()
    return words


@router.get(
    "/{letter}",
    response_model=List[schemas.Words],
    description="Returns a list of words which all books contains grouped by letter",
)
def get_words_by_letter(
    letter: str = Path(
        ...,
        min_length=1,
        max_length=1,
        pattern="^[a-zA-Z]$",
        description="Single letter",
    ),
    db: Session = Depends(database.get_db),
):
    words = db.query(models.Index).filter(models.Index.letter == letter.lower()).all()
    if not words:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"There is no words that start with{letter}",
        )
    return words
