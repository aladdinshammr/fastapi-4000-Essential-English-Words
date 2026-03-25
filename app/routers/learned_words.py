from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session, joinedload
from typing import List
from .. import schemas, database, models, auth2


router = APIRouter(prefix="/learned-words", tags=["Learned Words"])


@router.get("/", response_model=List[schemas.LearnedWordResponse])
def get_learned_words(
    db: Session = Depends(database.get_db),
    current_user: schemas.TokenData = Depends(auth2.get_current_user),
):
    learned_words = (
        db.query(models.LearnedWord)
        .filter(models.LearnedWord.user_id == current_user.id)
        .options(joinedload(models.LearnedWord.word))
        .options(joinedload(models.LearnedWord.user))
        .all()
    )

    if not learned_words:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"you have no saved words",
        )
    return learned_words


@router.post("/{word}", status_code=status.HTTP_201_CREATED)
def add_to_learned(
    word: int,
    db: Session = Depends(database.get_db),
    current_user: schemas.TokenData = Depends(auth2.get_current_user),
):
    has_answered = (
        db.query(models.LearnedWord)
        .filter(
            (models.LearnedWord.word_id == word)
            & (models.LearnedWord.user_id == current_user.id)
        )
        .first()
    )

    if has_answered:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"You have already saved the word with id={word}",
        )
    new_word = models.LearnedWord(user_id=current_user.id, word_id=word)
    db.add(new_word)
    db.commit()
    db.refresh(new_word)
    return new_word


@router.delete("/{word}")
def remove_from_learned(
    word: int,
    db: Session = Depends(database.get_db),
    current_user: schemas.TokenData = Depends(auth2.get_current_user),
):
    query = db.query(models.LearnedWord).filter(
        (models.LearnedWord.word_id == word)
        & (models.LearnedWord.user_id == current_user.id)
    )

    if not query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"you have no answer for word with id f{word}",
        )
    query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
