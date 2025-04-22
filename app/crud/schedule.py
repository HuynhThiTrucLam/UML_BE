from datetime import datetime
from sqlalchemy.orm import Session, joinedload
from app.models.schedule import Schedule
from app.models.course import Course
from app.models.license_type import LicenseType
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
        schedule_dict = {
            "id": schedule.id,
            "course_id": schedule.course_id,
            "start_time": schedule.start_time,
            "end_time": schedule.end_time,
            "location": schedule.location,
            "type": schedule.type,
            "instructor_id": schedule.instructor_id,
            "max_students": schedule.max_students,
            "license_type": {
                "id": schedule.course.license_type.id if schedule.course else uuid.uuid4(),
                "type_name": schedule.course.license_type.type_name if schedule.course else "",
            },
            "course": {
                "id": schedule.course.id if schedule.course else "",
                "name": schedule.course.course_name if schedule.course else "",
            },
        }
        schedule_list.append(schedule_dict)

    # Return a dictionary with items and total that matches ScheduleList schema
    return {"items": schedule_list, "total": len(schedule_list)}


def create_schedule(db: Session, schedule_in: ScheduleCreate):
    schedule = Schedule(
        id=uuid.uuid4(),
        course_id=schedule_in.course_id,
        start_time=schedule_in.start_time,
        end_time=schedule_in.end_time,
        location=schedule_in.location,
        type=schedule_in.type,
        instructor_id=schedule_in.instructor_id or None,
        max_students=schedule_in.max_students,
    )
    db.add(schedule)
    db.commit()
    db.refresh(schedule)
    result = ScheduleSchema.model_validate(schedule)
    print(result)
    return result
