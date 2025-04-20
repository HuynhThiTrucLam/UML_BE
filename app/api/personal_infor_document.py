from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.crud import personal_infor_document as crud_personal_infor_document
from app.schemas.personal_infor_document import PersonalInformationDocumentBase, PersonalInformationDocument, PersonalInformationDocumentCreate
from app.api.deps import get_db, get_current_active_user



import uuid

router = APIRouter()


#Create a new personal infor document
@router.post("/", response_model=PersonalInformationDocument)
def create_personal_infor_document(
    *,
    db: Session = Depends(get_db),
    personal_infor_document_in: PersonalInformationDocumentCreate,
) -> PersonalInformationDocument:
    """
    Create new personal infor document.
    """
    personal_infor_document = crud_personal_infor_document.create(db=db, obj_in=personal_infor_document_in)
    return personal_infor_document

#get personal infor document by user id
@router.get("/{user_id}", response_model=PersonalInformationDocument)
def get_personal_infor_document(
    *,
    db: Session = Depends(get_db),
    user_id: uuid.UUID,
) -> PersonalInformationDocument:
    """
    Get personal infor document by user id.
    """
    # Instead of using authentication here, just look up the document directly
    personal_infor_document = crud_personal_infor_document.getByUserID(db=db, id=user_id)
    if not personal_infor_document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Personal information document not found for this user",
        )
    return personal_infor_document