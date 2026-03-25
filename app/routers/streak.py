from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from .. import models, database, schemas, utils, auth2


router = APIRouter(prefix="/streak", tags=["Streak"])


@router.get("/")
def get_streak(current_user=Depends(auth2.get_current_user)):
    return {
        "current_streak": current_user.current_streak,
        "longest_streak": current_user.longest_streak,
    }
