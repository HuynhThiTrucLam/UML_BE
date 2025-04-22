from datetime import datetime
from sqlalchemy.orm import Session, joinedload
from app.models.schedule import Schedule
from app.models.course import Course
from app.models.license_type import LicenseType
from app.models.instructor import Instructor
from app.schemas.schedule import (
    ScheduleCreate,
    ScheduleUpdate,
    ScheduleList,
    Schedule as ScheduleSchema,
)
import uuid


def get_schedule(db: Session, start_time: str, end_time: str):
    # convert start_time and end_time to datetime objects
    start_date = datetime.fromisoformat(start_time)
    end_date = datetime.fromisoformat(end_time)

    # Get schedules between the start and end dates and filter by type (theory and practice)
    # Use joinedload to eagerly load the course and license_type relationships
    schedules = (
        db.query(Schedule)
        .options(joinedload(Schedule.course).joinedload(Course.license_type))
        .filter(
            Schedule.start_time >= start_date,
            Schedule.start_time <= end_date,
            Schedule.type.in_(["theory", "practice", "exam"]),
        )
        .all()
    )

    # Prepare response with license type information
    schedule_list = []
    for schedule in schedules:
        # Handle the case where course might be None
        course = schedule.course
        license_type = course.license_type if course else None
        
        schedule_dict = {
            "id": schedule.id,
            "course_id": schedule.course_id,
            "start_time": schedule.start_time,
            "end_time": schedule.end_time,
            "location": schedule.location,
            "type": schedule.type,
            "instructor_id": schedule.instructor_id,
            "max_students": schedule.max_students,
            "license_type_id": license_type.id if license_type else None,
            "license_type_name": license_type.type_name if license_type else "",
            "course_name": course.course_name if course else "",
        }
        schedule_list.append(schedule_dict)

    # Return a dictionary with items and total that matches ScheduleList schema
    return {"items": schedule_list, "total": len(schedule_list)}


def get_schedule_by_id(db: Session, schedule_id: uuid.UUID):
    """
    Get a schedule by ID
    
    Args:
        db: Database session
        schedule_id: UUID of the schedule to find
        
    Returns:
        Schedule object if found, None otherwise
    """
    return db.query(Schedule).options(
        joinedload(Schedule.course),
        joinedload(Schedule.instructor)
    ).filter(Schedule.id == schedule_id).first()


def create_schedule(db: Session, schedule_in: ScheduleCreate):
    db_schedule = Schedule(
        id=uuid.uuid4(),
        course_id=schedule_in.course_id,
        exam_id=schedule_in.exam_id if hasattr(schedule_in, "exam_id") else None,
        start_time=schedule_in.start_time.isoformat(),
        end_time=schedule_in.end_time.isoformat(),
        location=schedule_in.location,
        type=schedule_in.type,
        instructor_id=schedule_in.instructor_id,
        max_students=schedule_in.max_students
    )
    
    db.add(db_schedule)
    db.commit()
    
    # Refresh the schedule with joined relationships to ensure all needed data is loaded
    db_schedule = db.query(Schedule).options(
        joinedload(Schedule.course),
        joinedload(Schedule.instructor)
    ).filter(Schedule.id == db_schedule.id).first()
    
    # Create a dictionary with the expected structure
    schedule_dict = {
        "id": db_schedule.id,
        "course_id": db_schedule.course_id,
        "exam_id": db_schedule.exam_id,
        # Use the actual start_time and end_time values without trying to parse them
        "start_time": db_schedule.start_time,
        "end_time": db_schedule.end_time,
        "location": db_schedule.location,
        "type": db_schedule.type,
        "instructor_id": db_schedule.instructor_id,
        "max_students": db_schedule.max_students,
        "course": {
            "id": db_schedule.course.id if db_schedule.course else None,
            "name": db_schedule.course.course_name if db_schedule.course else None
        },
        "instructor": {
            "id": db_schedule.instructor.id if db_schedule.instructor else None,
            "name": db_schedule.instructor.user.user_name if db_schedule.instructor and db_schedule.instructor.user else None
        }
    }
    
    # Validate using the dictionary which has the expected structure
    return ScheduleSchema.model_validate(schedule_dict)


def update_schedule(db: Session, schedule_id: uuid.UUID, schedule_in: ScheduleUpdate):
    """
    Update an existing schedule
    
    Args:
        db: Database session
        schedule_id: UUID of the schedule to update
        schedule_in: ScheduleUpdate schema with fields to update
        
    Returns:
        Updated Schedule object or None if not found
    """
    # Get the existing schedule
    db_schedule = get_schedule_by_id(db, schedule_id=schedule_id)
    if not db_schedule:
        return None
    
    # Extract only the fields that were provided (not None)
    update_data = schedule_in.model_dump(exclude_unset=True)
    
    # Convert datetime objects to isoformat strings if present
    if "start_time" in update_data and update_data["start_time"]:
        update_data["start_time"] = update_data["start_time"].isoformat()
    if "end_time" in update_data and update_data["end_time"]:
        update_data["end_time"] = update_data["end_time"].isoformat()
    
    # Apply the updates
    for key, value in update_data.items():
        setattr(db_schedule, key, value)
    
    # Commit the changes
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    
    # Reload the schedule with all needed relationships
    # Use class-bound attributes instead of string
    updated_schedule = db.query(Schedule).options(
        joinedload(Schedule.course),
        joinedload(Schedule.instructor).joinedload(Instructor.user)
    ).filter(Schedule.id == schedule_id).first()
    
    # Create a dictionary with the expected structure for the Pydantic model
    schedule_dict = {
        "id": updated_schedule.id,
        "course_id": updated_schedule.course_id,
        "exam_id": updated_schedule.exam_id,
        "start_time": updated_schedule.start_time,
        "end_time": updated_schedule.end_time,
        "location": updated_schedule.location,
        "type": updated_schedule.type,
        "instructor_id": updated_schedule.instructor_id,
        "max_students": updated_schedule.max_students,
        "course": {
            "id": updated_schedule.course.id if updated_schedule.course else None,
            "name": updated_schedule.course.course_name if updated_schedule.course else None
        },
        "instructor": {
            "id": updated_schedule.instructor.id if updated_schedule.instructor else None,
            "name": updated_schedule.instructor.user.user_name if updated_schedule.instructor and hasattr(updated_schedule.instructor, 'user') and updated_schedule.instructor.user else None
        }
    }
    
    # Return the validated Pydantic model
    return ScheduleSchema.model_validate(schedule_dict)


def delete_schedule(db: Session, schedule_id: uuid.UUID) -> bool:
    """
    Delete a schedule by ID
    
    Args:
        db: Database session
        schedule_id: UUID of the schedule to delete
        
    Returns:
        bool: True if deletion was successful, False otherwise
    """
    try:
        result = db.query(Schedule).filter(Schedule.id == schedule_id).delete()
        db.commit()
        return result > 0
    except Exception as e:
        db.rollback()
        raise e
