from sqlalchemy.orm import Session
import uuid
from datetime import date
from app.models.health_check_document import HealthCheckDocument
from app.models.student import Student
from app.schemas.health_check_document import HealthCheckDocumentCreate, HealthCheckDocumentUpdate
from fastapi import HTTPException, status
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def create_health_check_document(db: Session, health_check_document: HealthCheckDocumentCreate):
    """
    Create a new health check document in the database.

    Args:
        db (Session): The database session.
        health_check_document (HealthCheckDocumentCreate): The health check document to create.

    Returns:
        HealthCheckDocument: The created health check document.
    
    Raises:
        HTTPException: If the student doesn't exist.
    """
    # First validate that the student exists
    student = db.query(Student).filter(Student.id == health_check_document.student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID {health_check_document.student_id} not found",
        )
    
    db_health_check_document = HealthCheckDocument(
        id=uuid.uuid4(),
        student_id=health_check_document.student_id,
        health_check_id=health_check_document.health_check_id,
        document=health_check_document.document,
        status=health_check_document.status,
        created_at= date.today(),  # Assuming you want to set the created_at to the current date
    )
    db.add(db_health_check_document)
    db.commit()
    db.refresh(db_health_check_document)
    print(f"Created health check document: {db_health_check_document}")
    return db_health_check_document


def get_health_check_documents_by_student_id(db: Session, student_id: uuid.UUID):
    """
    Get all health check documents for a specific student.

    Args:
        db (Session): The database session.
        student_id (uuid.UUID): The ID of the student.

    Returns:
        List[HealthCheckDocument]: A list of health check documents for the student.
    """
    return db.query(HealthCheckDocument).filter(HealthCheckDocument.student_id == student_id).all()

def update_health_check_document(
    db: Session, health_check_document_id: uuid.UUID, health_check_document: HealthCheckDocumentUpdate
):
    """
    Update an existing health check document.

    Args:
        db (Session): The database session.
        health_check_document_id (uuid.UUID): The ID of the health check document to update.
        health_check_document (HealthCheckDocumentUpdate): The updated health check document data.

    Returns:
        HealthCheckDocument: The updated health check document.
    """
    db_health_check_document = db.query(HealthCheckDocument).filter(HealthCheckDocument.id == health_check_document_id).first()
    if db_health_check_document:
        for key, value in health_check_document.dict(exclude_unset=True).items():
            setattr(db_health_check_document, key, value)
        db.commit()
        db.refresh(db_health_check_document)
        return db_health_check_document
    return None