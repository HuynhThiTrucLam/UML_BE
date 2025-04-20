from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.crud import health_check_schedule as crud_health_check_schedule
from app.crud import course as crud_course
from app.schemas.health_check_schedule import HealthCheckSchedule, HealthCheckScheduleCreate, HealthCheckScheduleUpdate, HealthCheckScheduleList
from app.api.deps import get_db, get_current_active_user, require_roles
from typing import List, Dict, Any
import uuid

router = APIRouter()

# Check health check schedule by ID
@router.get("/{schedule_id}", response_model=HealthCheckSchedule, summary="Get Health Check Schedule by ID")
def get_health_check_schedule(
    schedule_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user)
):
    """
    Retrieve a health check schedule by its ID.
    
    Args:
        schedule_id: The ID of the health check schedule to retrieve.
    
    Returns:
        HealthCheckSchedule: The health check schedule with the specified ID.
    
    Raises:
        HTTPException: If the health check schedule is not found.
    """
    health_check_schedule = crud_health_check_schedule.get_health_check_schedule(db=db, health_check_schedule_id=schedule_id)
    if health_check_schedule is None:
        raise HTTPException(status_code=404, detail="Health check schedule not found")
    return health_check_schedule

# Create a new health check schedule
@router.post("/", response_model=HealthCheckSchedule, status_code=status.HTTP_201_CREATED)
def create_health_check_schedule(
    schedule_in: HealthCheckScheduleCreate,  
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin"))
):
    """
    Create a new health check schedule.
    
    Only administrators can create health check schedules.
    """
    # Check if the course exists
    course = crud_course.get_course(db=db, course_id=schedule_in.course_id)
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Create the health check schedule
    health_check_schedule = crud_health_check_schedule.create_health_check_schedule(db=db, health_check_schedule_in=schedule_in)
    return health_check_schedule

# List health check schedules
@router.get("/", response_model=HealthCheckScheduleList, summary="List Health Check Schedules")
def list_health_check_schedules(
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """
    Retrieve all health check schedules.
    
    Args:
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return
    """
    schedules = crud_health_check_schedule.get_health_check_schedules(db, skip=skip, limit=limit)
    return schedules

# Update health check schedule
@router.put("/{schedule_id}", response_model=HealthCheckSchedule, summary="Update Health Check Schedule")
def update_health_check_schedule(
    schedule_id: uuid.UUID,
    schedule_in: HealthCheckScheduleUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin"))
):
    """
    Update an existing health check schedule.
    
    This endpoint supports partial updates - you only need to include the fields you want to change.
    Fields not included in the request will retain their current values.
    
    Only administrators can update health check schedules.
    """
    # If course_id is being updated, verify the course exists
    if schedule_in.course_id is not None:
        course = crud_course.get_course(db=db, course_id=schedule_in.course_id)
        if course is None:
            raise HTTPException(status_code=404, detail="Course not found")
    
    # Log the update request data
    print(f"Update request for schedule {schedule_id}: {schedule_in.model_dump(exclude_unset=True)}")
    
    try:
        updated_schedule = crud_health_check_schedule.update_health_check_schedule(db=db, schedule_id=schedule_id, schedule_in=schedule_in)
        if updated_schedule is None:
            raise HTTPException(status_code=404, detail="Health check schedule not found")
        return updated_schedule
    except ValueError as e:
        # Provide more detailed error response
        error_msg = str(e)
        print(f"Validation error for schedule {schedule_id}: {error_msg}")
        raise HTTPException(
            status_code=422, 
            detail={"message": error_msg, "error_type": "validation_error"}
        )
    except Exception as e:
        # Log unexpected errors
        error_msg = str(e)
        print(f"Unexpected error updating schedule {schedule_id}: {error_msg}")
        raise HTTPException(
            status_code=500, 
            detail="An unexpected error occurred while updating the health check schedule"
        )
    

# Delete health check schedule
@router.delete("/{schedule_id}", response_model=HealthCheckSchedule, summary="Delete Health Check Schedule")
def delete_health_check_schedule(
    schedule_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin"))
):
    """
    Delete a health check schedule by ID.
    
    Only administrators can delete health check schedules.
    """
    result = crud_health_check_schedule.delete_health_check_schedule(db=db, health_check_schedule_id=schedule_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Health check schedule not found")
    return result


