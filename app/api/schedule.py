from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_db, require_roles
import uuid
from app.crud import schedule as crud_schedule
from app.schemas.schedule import Schedule, ScheduleCreate, ScheduleList

router = APIRouter()


# get list of practice and theore class during a week of the date passed
@router.get("/", response_model=ScheduleList)
def get_schedule(
    start_time: str = "2023-10-01",
    end_time: str = "2023-10-07",
    db: Session = Depends(get_db),
):
    """
    Get a list of practice and theory classes during a week of the date passed.
    """
    db_schedule = crud_schedule.get_schedule(
        db=db, start_time=start_time, end_time=end_time
    )
    return db_schedule


# create schedule
@router.post("/", response_model=Schedule, status_code=status.HTTP_201_CREATED)
def create_schedule(
    schedule: ScheduleCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(require_roles(["admin"])),
):
    """
    Create a new schedule.
    """
    db_schedule = crud_schedule.create_schedule(db=db, schedule_in=schedule)
    result = Schedule.model_validate(db_schedule)
    print(result)
    return result
