from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session, joinedload
from .. import database, schemas, models


router = APIRouter(prefix="/units", tags=["Units"])


@router.get(
    "/",
    response_model=schemas.Unit,
    summary="Get all units",
    description="Returns a list of all units in this book series, change parameters if needed",
)
def get_unit(
    unit_num: int = Query(ge=1, le=180),
    db: Session = Depends(database.get_db),
):
    unit = (
        db.query(models.Unit)
        .filter(models.Unit.id == unit_num)
        .options(
            joinedload(models.Unit.words),
            joinedload(models.Unit.exercises),
            joinedload(models.Unit.readings),
        )
        .first()
    )

    print(unit)
    return unit
