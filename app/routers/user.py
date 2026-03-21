from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import schemas, database, models, utils, auth2


router = APIRouter(tags=["Authentication"])


@router.post(
    "/users", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED
)
def register(
    user: schemas.User,
    db: Session = Depends(database.get_db),
):
    email = db.query(models.User).filter(models.User.email == user.email).first()
    if email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already registered"
        )
    user.password = utils.get_password_hash(user.password)
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/users/{id}", response_model=schemas.UserOut)
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


@router.post("/login")
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
    return schemas.Token(access_token=access_token, token_type="bearer")
