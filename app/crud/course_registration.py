from venv import logger
from fastapi import HTTPException
from sqlalchemy.orm import Session
import uuid
from datetime import datetime
from typing import Dict, Any

from app.crud.health_check_document import create_health_check_document
from app.crud.personal_infor_document import create as create_personal_info
from app.crud.student import create_student
from app.crud.user import create_user
from app.models.course_registration import CourseRegistration
from app.models.personal_infor_document import PersonalInforDocument
from app.models.health_check_document import (
    HealthCheckDocument as HealthCheckDocumentModel,
)
from app.models.student import Student
from app.schemas.course import Course
from app.schemas.course_registration import (
    CourseRegistrationCreate,
    CourseRegistration as CourseRegistrationSchema,
)
from app.schemas.health_check_document import (
    HealthCheckDocument,
    HealthCheckDocumentCreate,
)
from app.schemas.personal_infor_document import (
    PersonalInformationDocument,
    PersonalInformationDocumentCreate,
)
from app.schemas.student import Student as StudentSchema, StudentCreate
from app.schemas.user import UserBase, UserCreate

from logging import getLogger

logger = getLogger(__name__)
# Constants
ROLE_USER = "user"
ROLE_ADMIN = "admin"
STATUS_PENDING = "pending"
STATUS_REGISTERED = "registered"
METHOD_ONLINE = "online"
METHOD_OFFLINE = "offline"


def create_course_registration(
    db: Session, course_registration: CourseRegistrationCreate
):
    """
    Create a complete course registration including user, student, personal information,
    and health check document records.

    Args:
        db: SQLAlchemy database session
        course_registration: Registration data containing all required information

    Returns:
        dict: A dictionary containing the status code and success message
    """
    try:
        # Create related records
        user = _create_user_for_registration(db, course_registration)
        student = _create_student_for_registration(db, user.id)
        personal_doc = _create_personal_information(db, user.id, course_registration)
        health_check_doc = _create_health_check_document(
            db, student.id, course_registration
        )

        # Determine registration method based on current user role
        method = _determine_registration_method(course_registration.role)
        logger.info(f"Registration method determined: {method}")
        # Create course registration
        db_course_registration = CourseRegistration(
            id=uuid.uuid4(),
            student_id=student.id,
            course_id=course_registration.course_id,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            status=STATUS_PENDING,
            method=method,
        )
        db.add(db_course_registration)
        db.commit()
        db.refresh(db_course_registration)

        # result = CourseRegistrationSchema.model_validate(db_course_registration, from_attributes=True)
        # result.health_check_doc = HealthCheckDocument.model_validate(health_check_doc)
        # result.personal_doc = PersonalInformationDocument.model_validate(personal_doc)
        # result.student = Student.model_validate(student, from_attributes=True)
        # result.course = Course.model_validate(db_course_registration.course, from_attributes=True)
        # return result

        return {
            "status_code": 201,
            "message": "Course registration created successfully.",
            "registration_id": str(db_course_registration.id),
        }
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating course registration: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to create course registration: {str(e)}"
        )


def _create_user_for_registration(
    db: Session, course_registration: CourseRegistrationCreate
):
    """Create a new user for the registration"""
    # Use a default email if none provided
    email = (
        course_registration.email
        if course_registration.email
        else f"{course_registration.identity_number}@example.com"
    )

    new_user = UserCreate(
        email=email,
        phone_number=course_registration.phone_number,
        user_name=course_registration.identity_number,
        password=course_registration.identity_number,
        role=ROLE_USER,
    )
    return create_user(db, new_user)


def _create_student_for_registration(db: Session, user_id: uuid.UUID):
    """Create a new student record linked to the user"""
    # Create StudentCreate without user_id and pass it separately
    return create_student(db, StudentCreate(user_id=user_id))


def _create_personal_information(
    db: Session, user_id: str, course_registration: CourseRegistrationCreate
):
    """Create personal information document for the user"""
    return create_personal_info(
        db,
        PersonalInformationDocumentCreate(
            user_id=user_id,
            full_name=course_registration.full_name,
            date_of_birth=course_registration.date_of_birth,
            gender=course_registration.gender,
            address=course_registration.address,
            identity_number=course_registration.identity_number,
            identity_img_back=course_registration.identity_image_back,
            identity_img_front=course_registration.identity_image_front,
            avatar=course_registration.avatar,
        ),
    )


def _create_health_check_document(
    db: Session, student_id: str, course_registration: CourseRegistrationCreate
):
    """Create health check document for the student"""
    logger.info(f"Creating health check document for student ID: {student_id}")
    return create_health_check_document(
        db,
        HealthCheckDocumentCreate(
            student_id=student_id,
            health_check_id=course_registration.health_check_schedule_id,
            status=STATUS_REGISTERED,
            document="",
        ),
    )


def _determine_registration_method(role: str) -> str:
    """Determine registration method based on user role"""
    # Add debug logging to see the exact role value
    logger.info(f"Determining method for role: '{role}'")
    
    # Make comparison case-insensitive and strip whitespace
    normalized_role = role.lower().strip() if role else ""
    normalized_admin = ROLE_ADMIN.lower().strip()
    
    is_admin = normalized_role == normalized_admin
    method = METHOD_OFFLINE if is_admin else METHOD_ONLINE
    
    logger.info(f"Role comparison: '{normalized_role}' == '{normalized_admin}' = {is_admin}, Method: {method}")
    
    return method


def get_course_registration_by_id(
    db: Session, course_registration_id: uuid.UUID
) -> CourseRegistrationSchema:
    """
    Get a course registration by its ID.

    Args:
        db: SQLAlchemy database session
        course_registration_id: The ID of the course registration

    Returns:
        CourseRegistration: The course registration record with all related data
    """
    db_course_registration = (
        db.query(CourseRegistration)
        .filter(CourseRegistration.id == course_registration_id)
        .first()
    )
    if not db_course_registration:
        raise HTTPException(status_code=404, detail="Course registration not found")

    # Create the basic registration schema first
    result = CourseRegistrationSchema.model_validate(
        db_course_registration, from_attributes=True
    )

    # Get the related student data
    student = db_course_registration.student
    if student:
        result.student = StudentSchema.model_validate(student, from_attributes=True)

    # Get the course data
    if db_course_registration.course:
        result.course = Course.model_validate(
            db_course_registration.course, from_attributes=True
        )

    # Get the health check document related to this student
    health_check_doc = (
        db.query(HealthCheckDocumentModel)
        .filter(
            HealthCheckDocumentModel.student_id == db_course_registration.student_id,
            (
                HealthCheckDocumentModel.health_check_id
                == db_course_registration.student.health_check_documents[
                    0
                ].health_check_id
                if db_course_registration.student
                and db_course_registration.student.health_check_documents
                else None
            ),
        )
        .first()
    )

    if health_check_doc:
        result.health_check_doc = HealthCheckDocument.model_validate(health_check_doc)

    # Get the personal information document related to this user
    if student and student.user:
        personal_doc = (
            db.query(PersonalInforDocument)
            .filter(PersonalInforDocument.user_id == student.user_id)
            .first()
        )

        if personal_doc:
            result.personal_doc = PersonalInformationDocument.model_validate(
                personal_doc
            )
            personal_user = UserBase.model_validate(
                personal_doc.user, from_attributes=True
            )
            result.personal_doc.email = personal_user.email
            result.personal_doc.phone_number = personal_user.phone_number

    return result


def get_course_registration_by_identity_number(
    db: Session, identity_number: str
) -> CourseRegistrationSchema:
    """
    Get a course registration by identity number.

    Args:
        db: SQLAlchemy database session
        identity_number: The identity number of the user

    Returns:
        CourseRegistration: The course registration record with all related data
    """
    # First, find the personal information document with the given identity number
    personal_info_doc = (
        db.query(PersonalInforDocument)
        .filter(PersonalInforDocument.identity_number == identity_number)
        .first()
    )

    if not personal_info_doc:
        raise HTTPException(
            status_code=404,
            detail="No personal information found with this identity number",
        )

    # Get the user ID from the personal information document
    user_id = personal_info_doc.user_id

    # Find the student associated with this user
    student = db.query(Student).filter(Student.user_id == user_id).first()

    if not student:
        raise HTTPException(
            status_code=404, detail="No student record found for this identity number"
        )

    # Find the course registration for this student
    course_registration = (
        db.query(CourseRegistration)
        .filter(CourseRegistration.student_id == student.id)
        .first()
    )

    if not course_registration:
        raise HTTPException(
            status_code=404,
            detail="No course registration found for this identity number",
        )

    # Reuse the existing function to get the full details
    return get_course_registration_by_id(db, course_registration.id)


def get_all_course_registrations(
    db: Session, type: str, status: str, skip: int = 0, limit: int = 100
) -> list[CourseRegistrationSchema]:
    """
    Get all course registrations with pagination.

    Args:
        db: SQLAlchemy database session
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return

    Returns:
        list[CourseRegistrationResponse]: List of course registration response records
    """
    from app.schemas.course_registration import (
        CourseRegistrationResponse,
        CourseStudent,
        CoursePersonalData,
        PersonalImgData,
        ChooseData,
        CourseType,
        HealthCheckType,
        ScheduleType,
        TypeOfLicense,
    )
    from app.models.schedule import Schedule
    from app.models.license_type import LicenseType

    db_course_registrations = (
        db.query(CourseRegistration)
        .filter((CourseRegistration.method == type if type != "all" else True))
        .filter((CourseRegistration.status == status if status != "all" else True))
        .offset(skip)
        .limit(limit)
        .all()
    )
    print(f"db_course_registrations: {len(db_course_registrations)}")
    result = []

    for registration in db_course_registrations:
        # Get associated data
        student = registration.student
        course = registration.course
        schedules = (
            db.query(Schedule).filter(Schedule.course_id == course.id).all()
            if course
            else []
        )

        # Get personal information
        personal_info = None
        if student and student.user_id:
            personal_info = (
                db.query(PersonalInforDocument)
                .filter(PersonalInforDocument.user_id == student.user_id)
                .first()
            )

        # Get health check document
        health_check_doc = None
        if student:
            health_check_doc = (
                db.query(HealthCheckDocumentModel)
                .filter(HealthCheckDocumentModel.student_id == student.id)
                .first()
            )

        if not personal_info or not student or not course:
            logger.warning(f"Missing related data for registration {registration.id}")
            continue

        # Get license type
        license_type = (
            db.query(LicenseType)
            .filter(LicenseType.id == course.license_type_id)
            .first()
            if course
            else None
        )
        # Build personal data
        personal_data = CoursePersonalData(
            name=personal_info.full_name,
            identityNumber=personal_info.identity_number,
            address=personal_info.address,
            phone=student.user.phone_number if student.user else "",
            gender=personal_info.gender,
            birthDate=personal_info.date_of_birth,  # date_of_birth is already a string
            licenseType=license_type.type_name if license_type else "",
            email=student.user.email if student.user else "",
            healthCheckDocURL=health_check_doc.document if health_check_doc else "",
        )

        # Build personal image data
        personal_img_data = PersonalImgData(
            avatar=personal_info.avatar if personal_info else "",
            cardImgFront=personal_info.identity_img_front if personal_info else "",
            cardImgBack=personal_info.identity_img_back if personal_info else "",
        )

        # Build course data
        course_data = CourseType(
            id=str(course.id),
            name=course.course_name,
            licenseTypeId=str(course.license_type_id),
            examDate=course.end_date.strftime("%Y-%m-%d") if course.end_date else "",
            startDate=(
                course.start_date.strftime("%Y-%m-%d") if course.start_date else ""
            ),
            endDate=course.end_date.strftime("%Y-%m-%d") if course.end_date else "",
            registeredCount=(
                course.registered_count if hasattr(course, "registered_count") else 0
            ),
            maxStudents=course.max_students if hasattr(course, "max_students") else 0,
        )

        # Build health check data
        health_check_data = HealthCheckType(
            id=str(health_check_doc.health_check_id) if health_check_doc else "",
            name=(
                health_check_doc.health_check.description
                if health_check_doc and hasattr(health_check_doc, "health_check")
                else ""
            ),
            date=(
                health_check_doc.health_check.scheduled_datetime
                if isinstance(health_check_doc.health_check.scheduled_datetime, str)
                else (
                    health_check_doc.health_check.scheduled_datetime.strftime(
                        "%Y-%m-%d"
                    )
                    if health_check_doc
                    and hasattr(health_check_doc, "health_check")
                    and health_check_doc.health_check.scheduled_datetime
                    else ""
                )
            ),
            address=(
                health_check_doc.health_check.address
                if health_check_doc and hasattr(health_check_doc, "health_check")
                else ""
            ),
            courseId=str(course.id),
        )

        # Build choose data
        choose_data = ChooseData(course=course_data, healthCheck=health_check_data)

        # Build student info
        student_info = CourseStudent(
            personalData=personal_data,
            personalImgData=personal_img_data,
            chooseData=choose_data,
        )

        # Build schedule info
        schedule_info = []
        for schedule in schedules:
            license_type_obj = (
                db.query(LicenseType)
                .filter(LicenseType.id == course.license_type_id)
                .first()
                if course
                else None
            )

            schedule_info.append(
                ScheduleType(
                    id=str(schedule.id),
                    courseId=str(schedule.course_id),
                    typeOfLicense=TypeOfLicense(
                        id=str(license_type_obj.id) if license_type_obj else "",
                        name=license_type_obj.type_name if license_type_obj else "",
                    ),
                    type=schedule.type if hasattr(schedule, "type") else "",
                    startTime=(
                        schedule.start_time.strftime("%Y-%m-%d %H:%M:%S")
                        if hasattr(schedule, "start_time") and schedule.start_time
                        else ""
                    ),
                    endTime=(
                        schedule.end_time.strftime("%Y-%m-%d %H:%M:%S")
                        if hasattr(schedule, "end_time") and schedule.end_time
                        else ""
                    ),
                    location=schedule.location if hasattr(schedule, "location") else "",
                    teacher=schedule.teacher if hasattr(schedule, "teacher") else None,
                )
            )

        # Create response object
        response_obj = CourseRegistrationResponse(
            id=registration.id,
            method=registration.method,
            registrationDate=(
                registration.created_at
                if isinstance(registration.created_at, str)
                else (
                    registration.created_at.strftime("%Y-%m-%d")
                    if registration.created_at
                    else ""
                )
            ),
            status=registration.status,
            studentInfor=student_info,
            scheduleInfor=schedule_info,
            scoreOverall=None,  # Not provided in the source data
            receiveDate=None,  # Not provided in the source data
            location=None,  # Not provided in the source data
        )

        result.append(response_obj)

    return result


def update_course_registration(
    db: Session, course_registration_id: uuid.UUID, course_registration: Dict[str, Any]
) -> CourseRegistrationSchema:
    """
    Update a course registration by its ID.

    Args:
        db: SQLAlchemy database session
        course_registration_id: The ID of the course registration
        course_registration: Dictionary containing the fields to update

    Returns:
        CourseRegistration: The updated course registration record
    """
    db_course_registration = (
        db.query(CourseRegistration)
        .filter(CourseRegistration.id == course_registration_id)
        .first()
    )
    if not db_course_registration:
        raise HTTPException(status_code=404, detail="Course registration not found")

    for key, value in course_registration.__dict__.items():
        setattr(db_course_registration, key, value)

    db.commit()
    db.refresh(db_course_registration)

    return CourseRegistrationSchema.model_validate(
        db_course_registration, from_attributes=True
    )


def delete_course_registration(
    db: Session, course_registration_id: uuid.UUID
) -> Dict[str, str]:
    """
    Delete a course registration by its ID.

    Args:
        db: SQLAlchemy database session
        course_registration_id: The ID of the course registration

    Returns:
        dict: A dictionary containing the status code and success message
    """
    db_course_registration = (
        db.query(CourseRegistration)
        .filter(CourseRegistration.id == course_registration_id)
        .first()
    )
    if not db_course_registration:
        raise HTTPException(status_code=404, detail="Course registration not found")

    db.delete(db_course_registration)
    db.commit()

    return {"status_code": 200, "message": "Course registration deleted successfully."}
