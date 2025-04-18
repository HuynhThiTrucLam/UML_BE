from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.crud import student as crud_student
from app.schemas.student import Student, StudentCreate
from app.api.deps import get_db, get_current_active_user, require_roles
from logging import getLogger

logger = getLogger(__name__)

router = APIRouter()

@router.post("/", response_model=Student, status_code=status.HTTP_201_CREATED)
def create_student(
    student_in: StudentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("staff", "admin"))
):
    return crud_student.create_student(db=db, student_in=student_in, user_id=current_user["id"])

# @router.get("/{student_id}", response_model=Student)
# def read_student(student_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
#     student = crud_student.get_student(db, student_id=student_id)
#     if not student:
#         raise HTTPException(status_code=404, detail="Student not found")
#     return student

@router.get("/")
def list_student(current_user=Depends(get_current_active_user)):
    logger(f"current_user: {current_user}")
    return []