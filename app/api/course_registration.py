import uuid
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.crud import course_registration as crud_cousre_registration
from app.schemas.course_registration import CourseRegistration, CourseRegistrationCreate, CourseRegistrationUpdate
from typing import Dict, Any

router = APIRouter()

#Create a new course registration
@router.post("/", response_model=Dict[str, Any])
def create_course_registration(
    course_registration: CourseRegistrationCreate,
    response: Response,
    db: Session = Depends(get_db),
):
    result = crud_cousre_registration.create_course_registration(db=db, course_registration=course_registration)
    response.status_code = result.get("status_code", 201)
    return result

#Get a course registration by ID
@router.get("/{course_registration_id}", response_model=CourseRegistration)
def get_course_registration(
    course_registration_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    db_course_registration = crud_cousre_registration.get_course_registration_by_id(db=db, course_registration_id=course_registration_id)
    if not db_course_registration:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course registration not found")
    return db_course_registration