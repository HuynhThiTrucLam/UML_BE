from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_db, require_roles
import uuid
from app.crud import schedule as crud_schedule
from app.schemas.schedule import Schedule, ScheduleCreate, ScheduleList, ScheduleUpdate

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


# update schedule
@router.put("/{schedule_id}", response_model=Schedule)
def update_schedule(
    schedule_id: uuid.UUID,
    schedule: ScheduleUpdate,
    db: Session = Depends(get_db),
    current_user: str = Depends(require_roles(["admin"])),
):
    """
    Update an existing schedule.
    
    This endpoint supports partial updates - you only need to include the fields you want to change.
    Fields not included in the request will retain their current values.
    """
    existing_schedule = crud_schedule.get_schedule_by_id(db, schedule_id=schedule_id)
    if not existing_schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Schedule not found"
        )
        
    updated_schedule = crud_schedule.update_schedule(
        db=db, schedule_id=schedule_id, schedule_in=schedule
    )
    return Schedule.model_validate(updated_schedule, from_attributes=True)


# delete schedule
@router.delete("/{schedule_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_schedule(
    schedule_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: str = Depends(require_roles(["admin"])),
):
    """
    Delete a schedule.
    """
    existing_schedule = crud_schedule.get_schedule_by_id(db, schedule_id=schedule_id)
    if not existing_schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Schedule not found"
        )
    
    deletion_successful = crud_schedule.delete_schedule(db=db, schedule_id=schedule_id)
    if not deletion_successful:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete schedule"
        )
    
    return None
