from sqlalchemy.orm import Session
import uuid
from app.api import user
from app.schemas.personal_infor_document import PersonalInformationDocumentBase, PersonalInformationDocument, PersonalInformationDocumentCreate
from datetime import date
from app.models.personal_infor_document import PersonalInforDocument


def create(db: Session, obj_in:PersonalInformationDocumentCreate ):
    """
    Create a new personal_infor_document record in the database.

    Args:
        db (Session): The database session.
        personal_infor_document: The personal_infor_document object to create.

    Returns:
        The created personal_infor_document object.
    """
    
    personal_infor_document = PersonalInforDocument(
        id=uuid.uuid4(),
        user_id=obj_in.user_id,
        full_name=obj_in.full_name,
        date_of_birth=obj_in.date_of_birth,
        gender = obj_in.gender,
        address = obj_in.address,

        identity_number = obj_in.identity_number,
        identity_img_front = obj_in.identity_img_front,
        identity_img_back = obj_in.identity_img_back,
        avatar = obj_in.avatar,
    )
    
    db.add(personal_infor_document)
    db.commit()
    db.refresh(personal_infor_document)
    return personal_infor_document

def getByUserID(db: Session, id: uuid.UUID):
    """
    Get a personal_infor_document record by student ID.

    Args:
        db (Session): The database session.
        student_id (str): The student ID.

    Returns:
        The personal_infor_document object if found, None otherwise.
    """
    
    result = db.query(PersonalInforDocument).filter(PersonalInforDocument.user_id == id).first()
    return result