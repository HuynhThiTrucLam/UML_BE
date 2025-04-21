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
    return METHOD_OFFLINE if role == ROLE_ADMIN else METHOD_ONLINE


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
