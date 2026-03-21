from fastapi import APIRouter, HTTPException, status, Depends, Query, Response
from sqlalchemy.orm import Session
from typing import List


from .. import schemas, models, database, auth2


router = APIRouter(prefix="/answers", tags=["Answer"])


@router.get("/reading-comperhension", response_model=List[schemas.UserAnswerRespone])
def get_reading_comperhension_answers(
    unit_num: int = Query(None, ge=1, le=180),
    db: Session = Depends(database.get_db),
    current_user: schemas.TokenData = Depends(auth2.get_current_user),
):
    query = db.query(models.ReadingAnswer).filter(
        models.ReadingAnswer.user_id == current_user.id
    )
    answers = ""
    if unit_num:
        answers = query.filter(models.ReadingAnswer.unit_id == unit_num).all()
        if not answers:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"you have no answers for unit number:{unit_num}",
            )
    else:
        answers = query.all()
        if not answers:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"you have no answers.",
            )
    return answers


@router.post("/reading-comperhension", response_model=schemas.UserAnswerRespone)
def answer_reading_comperhension(
    user_answer: schemas.UserAnswer,
    db: Session = Depends(database.get_db),
    current_user: schemas.TokenData = Depends(auth2.get_current_user),
):

    already_answered = (
        db.query(models.ReadingAnswer)
        .filter(
            (models.ReadingAnswer.user_id == current_user.id)
            & (models.ReadingAnswer.unit_id == user_answer.unit_id)
        )
        .first()
    )
    if already_answered:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"You have already answered for unit {user_answer.unit_id} try updating it instead.",
        )
    new_answer = models.ReadingAnswer(
        **user_answer.model_dump(), user_id=current_user.id
    )
    db.add(new_answer)
    db.commit()
    db.refresh(new_answer)
    return new_answer


@router.put("/reading-comperhension")
def update_reading_comperhention_answer(
    user_answer: schemas.UserAnswer,
    db: Session = Depends(database.get_db),
    current_user: schemas.TokenData = Depends(auth2.get_current_user),
):
    query = db.query(models.ReadingAnswer).filter(
        (models.ReadingAnswer.user_id == current_user.id)
        & (models.ReadingAnswer.unit_id == user_answer.unit_id)
    )

    answer = query.first()
    if not answer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"You have no answers to be updated",
        )
    print(user_answer)
    # query.update(user_answer.model_dump(), synchronize_session=False)
    answer.answer = user_answer.answer  # type: ignore
    db.commit()
    db.refresh(answer)
    return answer


@router.delete("/reading-comperhension/{unit_num}")
def delete_reading_comperhension_answer(
    unit_num: int,
    db: Session = Depends(database.get_db),
    current_user: schemas.TokenData = Depends(auth2.get_current_user),
):
    query = db.query(models.ReadingAnswer).filter(
        (models.ReadingAnswer.unit_id == unit_num)
        & (models.ReadingAnswer.user_id == current_user.id)
    )
    answer = query.first()
    if not answer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"you have no answers for unit number:{unit_num}",
        )
    query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
