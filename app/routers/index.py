from fastapi import APIRouter, Depends, Path, HTTPException, status
from sqlalchemy.orm import Session
from enum import Enum


from .. import database, models, schemas


class BookNum(int, Enum):
    book1 = 1
    book2 = 2
    book3 = 3
    book4 = 4
    book5 = 5
    book6 = 6


router = APIRouter(tags=["Index"], prefix="/indexs")


@router.get("/book/{book_num}")
def get_words_by_book(
    # book_num: int = Path(..., gt=0, lt=6, description="Book number between 1 and 6"),
    book_num: BookNum,
    db: Session = Depends(database.get_db),
):
    words = db.query(models.Index).filter(models.Index.book == book_num).all()
    return words


@router.get("/{letter}")
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
