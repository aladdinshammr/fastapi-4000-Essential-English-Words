from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session, joinedload, contains_eager
from typing import List
from .. import database, schemas, models


router = APIRouter(prefix="/units", tags=["Units"])


@router.get(
    "/",
    response_model=List[schemas.Unit],
    summary="Get all units",
    description="returns a list of units, change parameters if needed",
)
def get_units(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(database.get_db),
):
    units = (
        db.query(models.Unit)
        .options(
            joinedload(models.Unit.words),
            joinedload(models.Unit.readings),
            joinedload(models.Unit.exercises),
        )
        .offset(skip)
        .limit(limit)
    )

    return units.all()


@router.get(
    "/{unit_num}",
    response_model=schemas.Unit,
    summary="Get a unit",
)
def get_unit(
    unit_num: int = Path(
        ..., ge=1, le=180, description="Unit number between 1 and 180"
    ),
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

    return unit
