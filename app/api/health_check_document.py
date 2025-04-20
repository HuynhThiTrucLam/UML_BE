from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.health_check_document import HealthCheckDocument,HealthCheckDocumentCreate, HealthCheckDocumentUpdate
from app.crud import health_check_document as crud_health_check_document
from app.api.deps import get_db, get_current_active_user, require_roles
import uuid


router = APIRouter()

# create health check document
@router.post(
    "/",
    response_model=HealthCheckDocument,

    status_code=status.HTTP_201_CREATED,
    summary="Create a health check document",
)
async def create_health_check_document(
    health_check_document: HealthCheckDocumentCreate,
    db: Session = Depends(get_db),
) -> HealthCheckDocument:
    """
    Create a new health check document.
    """

    # Create the health check document in the database
    health_check_document = crud_health_check_document.create_health_check_document(
        db=db,
        health_check_document=health_check_document,
    )
    return health_check_document


# get all health check documents by student id and role
@router.get(
    "/",
    response_model=list[HealthCheckDocument],
    status_code=status.HTTP_200_OK,
    summary="Get all health check documents by student id and role",
)
@router.get(
    "/{student_id}",
    response_model=list[HealthCheckDocument],
    status_code=status.HTTP_200_OK,
    summary="Get all health check documents by student id",
)
async def get_health_check_documents_by_student_id(
    student_id: uuid.UUID,
    db: Session = Depends(get_db),
) -> list[HealthCheckDocument]:
    """
    Get all health check documents by student id.
    """
    health_check_documents = crud_health_check_document.get_health_check_documents_by_student_id(
        db=db,
        student_id=student_id,
    )
    return health_check_documents

# update health check document 
@router.put(
    "/{document_id}",
    response_model=HealthCheckDocument,
    status_code=status.HTTP_200_OK,
    summary="Update a health check document",
)
async def update_health_check_document(
    document_id: uuid.UUID,
    health_check_document: HealthCheckDocumentUpdate,
    db: Session = Depends(get_db),
) -> HealthCheckDocument:
    """
    Update a health check document.
    """
    # Update the health check document in the database
    health_check_document = crud_health_check_document.update_health_check_document(
        db=db,
        document_id=document_id,
        health_check_document=health_check_document,
    )
    return health_check_document