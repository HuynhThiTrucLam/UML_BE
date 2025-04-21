from sqlalchemy.orm import Session
from app.models.course import Course
from app.schemas.course import CourseCreate, CourseUpdate, CourseList
import uuid
from datetime import date


def get_course(db: Session, course_id: uuid.UUID):
    return db.query(Course).filter(Course.id == course_id).first()


def get_courses(db: Session, skip: int = 0, limit: int = 100):
    courses = db.query(Course).offset(skip).limit(limit).all()
    total = db.query(Course).count()
    return {"items": courses, "total": total}


def create_course(db: Session, course_in: CourseCreate):
    course = Course(
        id=uuid.uuid4(),
        course_name=course_in.course_name,
        license_type_id=course_in.license_type_id,
        start_date=course_in.start_date,
        end_date=course_in.end_date,
        max_students=course_in.max_students,
        current_students=0,  # New courses start with 0 students
        price=course_in.price,
        status=course_in.status,
        created_at=date.today(),
        updated_at=date.today(),
    )
    db.add(course)
    db.commit()
    db.refresh(course)
    return course


def update_course(db: Session, course_id: uuid.UUID, course_in: CourseUpdate):
    """
    Update a course if it exists.

    This function performs a partial update - only the fields provided in the request
    will be updated. Other fields will retain their current values.

    Args:
        db: Database session
        course_id: UUID of the course to update
        course_in: New course data (only provide fields you want to update)

    Returns:
        Updated course object, or None if course doesn't exist
    """
    # First check if the course exists
    course = get_course(db=db, course_id=course_id)
    if course is None:
        return None

    # Debug information
    print(f"Original course data: {course.__dict__}")

    # Get only the fields that were explicitly set (not None)
    # In Pydantic v2, model_dump properly handles Optional fields
    try:
        # Convert to dict and exclude unset/None values
        update_data = {}
        for key, value in course_in.model_dump(exclude_unset=True).items():
            if value is not None:
                update_data[key] = value

        print(f"Fields to update: {update_data}")
    except Exception as e:
        print(f"Error during model_dump: {e}")
        raise ValueError(f"Error processing update data: {e}")

    # If empty after filtering None values, return the course without changes
    if not update_data:
        print("No fields to update (all were None or unset)")
        return course

    # Date validations
    # Skip validation if neither date is being updated
    if not ("start_date" in update_data or "end_date" in update_data):
        pass
    # Validate date relationships if both dates are being updated
    elif "start_date" in update_data and "end_date" in update_data:
        if update_data["end_date"] < update_data["start_date"]:
            raise ValueError("End date must be after start date")
    # Validate if only end_date is being updated (compare with existing start_date)
    elif "end_date" in update_data:
        if update_data["end_date"] < course.start_date:
            raise ValueError("End date must be after the existing start date")
    # Validate if only start_date is being updated (compare with existing end_date)
    elif "start_date" in update_data:
        if update_data["start_date"] > course.end_date:
            raise ValueError("Start date must be before the existing end date")

    try:
        # Apply the updates
        for key, value in update_data.items():
            setattr(course, key, value)

        # Always update the updated_at field
        course.updated_at = date.today()

        db.add(course)
        db.commit()
        db.refresh(course)
        print(f"Course updated successfully: {course.__dict__}")
        return course
    except Exception as e:
        db.rollback()
        print(f"Database error during update: {e}")
        raise ValueError(f"Database error: {e}")


def delete_course(db: Session, course_id: uuid.UUID):
    course = get_course(db=db, course_id=course_id)
    if course is None:
        return None
    db.delete(course)
    db.commit()
    return course
