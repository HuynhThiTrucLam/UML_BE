from sqlalchemy.orm import Session
from app.models.instructor import Instructor
from app.schemas.instructor import InstructorResponse

def list_instructors(db: Session, skip: int = 0, limit: int = 100):
    response = db.query(Instructor).offset(skip).limit(limit).all()
    
    # Fix: Use model_validate with from_attributes=True to convert SQLAlchemy objects
    return list(map(lambda x: InstructorResponse.model_validate(x, from_attributes=True), response))
