from sqlalchemy.orm import Session
import uuid
from datetime import date, datetime
from app.models.health_check_schedule import HealthCheckSchedule
from app.schemas.health_check_schedule import HealthCheckScheduleCreate, HealthCheckScheduleUpdate

# Get health check schedule by ID
def get_health_check_schedule(db: Session, health_check_schedule_id: uuid.UUID):
    """
    Retrieve a health check schedule by its ID.
    
    Args:
        db: Database session
        health_check_schedule_id: UUID of the health check schedule to retrieve
        
    Returns:
        HealthCheckSchedule object, or None if not found
    """
    return db.query(HealthCheckSchedule).filter(HealthCheckSchedule.id == health_check_schedule_id).first()

#create health check schedule
def create_health_check_schedule(db: Session, health_check_schedule_in: HealthCheckScheduleCreate):
    """
    Create a new health check schedule.
    
    Args:
        db: Database session
        health_check_schedule_in: Data for the new health check schedule
        
    Returns:
        Created HealthCheckSchedule object
    """
    health_check_schedule = HealthCheckSchedule(
        course_id=health_check_schedule_in.course_id,
        address=health_check_schedule_in.address,
        scheduled_datetime=health_check_schedule_in.scheduled_datetime,
        description=health_check_schedule_in.description if health_check_schedule_in.description else None,
        status=health_check_schedule_in.status if hasattr(health_check_schedule_in, 'status') else "scheduled"
        # Let SQLAlchemy handle id, created_at and updated_at with default values
    )
    db.add(health_check_schedule)
    db.commit()
    db.refresh(health_check_schedule)
    return health_check_schedule

# Update health check schedule
def update_health_check_schedule(db: Session, schedule_id: uuid.UUID, schedule_in: HealthCheckScheduleUpdate):
    """
    Update an existing health check schedule.
    
    This function only updates the fields that are provided in the request.
    Fields not included in the request retain their current values.
    
    Args:
        db: Database session
        schedule_id: UUID of the health check schedule to update
        schedule_in: Data for updating the health check schedule
        
    Returns:
        Updated HealthCheckSchedule object, or None if not found
    """
    # Get the existing schedule
    db_schedule = get_health_check_schedule(db, health_check_schedule_id=schedule_id)
    if db_schedule is None:
        return None
    
    # Extract only the fields that were provided (not None)
    update_data = schedule_in.model_dump(exclude_unset=True)
    
    # Apply the updates
    for key, value in update_data.items():
        setattr(db_schedule, key, value)
    
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule

# Get all health check schedules
def get_health_check_schedules(db: Session, skip: int = 0, limit: int = 100):
    """
    Retrieve all health check schedules.
    
    Args:
        db: Database session
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return
        
    Returns:
        List of HealthCheckSchedule objects
    """
    health_check_schedules = db.query(HealthCheckSchedule).offset(skip).limit(limit).all()
    total = db.query(HealthCheckSchedule).count()
    return {"items": health_check_schedules, "total": total}

# Delete health check schedule
def delete_health_check_schedule(db: Session, health_check_schedule_id: uuid.UUID):
    """
    Delete a health check schedule by its ID.
    
    Args:
        db: Database session
        health_check_schedule_id: UUID of the health check schedule to delete
        
    Returns:
        Deleted HealthCheckSchedule object, or None if not found
    """
    # # Ensure health_check_schedule_id is properly converted to UUID
    # if isinstance(health_check_schedule_id, str):
    #     health_check_schedule_id = uuid.UUID(health_check_schedule_id)
    
    # # First get the schedule record to confirm it exists
    # db_schedule = db.query(models.health_check_schedule.HealthCheckSchedule).filter(
    #     models.health_check_schedule.HealthCheckSchedule.id == health_check_schedule_id
    # ).first()
    
    # if db_schedule is None:
    #     return None
    
    # # Fetch all related health check documents first
    # related_docs = db.query(models.health_check_document.HealthCheckDocument).filter(
    #     models.health_check_document.HealthCheckDocument.health_check_id == health_check_schedule_id
    # ).all()
    
    # # Delete them individually to avoid type casting issues
    # for doc in related_docs:
    #     db.delete(doc)

    schedule = get_health_check_schedule(db, health_check_schedule_id)
    if schedule is None:
        return None
    
    # Then delete the schedule
    db.delete(schedule)
    db.commit()
    
    return schedule