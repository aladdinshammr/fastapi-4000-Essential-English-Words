from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import schemas, database, models, utils, auth2
from datetime import date


router = APIRouter(tags=["Authentication"])


def update_streak(user, db: Session):
    today = date.today()

    if not user.last_active_date:
        user.current_streak = 1
        user.longest_streak = 1
    else:
        last_date = user.last_active_date
        if hasattr(last_date, "date"):
            last_date = last_date.date()
        delta = (today - last_date).days

        if delta == 0:
            pass
        elif delta == 1:
            user.current_streak += 1
        else:
            user.current_streak = 1

    user.last_active_date = today

    if user.current_streak > user.longest_streak:
        user.longest_streak = user.current_streak

    db.commit()
    db.refresh(user)
    return user


@router.post(
    "/users",
    response_model=schemas.UserOut,
    status_code=status.HTTP_201_CREATED,
    description="Register a new account",
)
def sign_up(
    user: schemas.User,
    db: Session = Depends(database.get_db),
):
    email = db.query(models.User).filter(models.User.email == user.email).first()
    if email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already registered"
        )
    user.password = utils.get_password_hash(user.password)
    new_user = models.User(**user.model_dump(), last_active_date=(date.today()))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get(
    "/users/{id}",
    response_model=schemas.UserOut,
    description="Get user info",
)
def get_user(
    id: int,
    db: Session = Depends(database.get_db),
):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id:{id} does not exist",
        )
    return user


@router.post(
    "/login",
    response_model=schemas.Token,
)
def login(
    user_cred: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db),
):
    query = db.query(models.User).filter(models.User.email == user_cred.username)
    user = query.first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials"
        )
    if not utils.verify_password(user_cred.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials"
        )
    access_token = auth2.create_access_token({"id": user.id})
    new_login = models.UserLogin(user_id=user.id)
    db.add(new_login)
    db.commit()
    db.refresh(new_login)
    update_streak(user=user, db=db)
    return schemas.Token(access_token=access_token, token_type="bearer")
