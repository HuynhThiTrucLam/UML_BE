from uuid import UUID
from logging import getLogger
from sqlalchemy.orm import Session
from app.models.student import Student
from app.schemas.student import StudentCreate

logger = getLogger(__name__)


def get_student(db: Session, student_id: int):
    return db.query(Student).filter(Student.id == student_id).first()


def create_student(db: Session, student_in: StudentCreate):

    student = Student(user_id=student_in.user_id)
    logger.debug(f"Created student: {student}")
    db.add(student)
    db.commit()
    db.refresh(student)
    return student
