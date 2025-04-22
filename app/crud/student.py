from uuid import UUID
from logging import getLogger
from sqlalchemy.orm import Session
from app.models.student import Student
from app.schemas.student import StudentCreate, Student as StudentSchema

logger = getLogger(__name__)


def get_students(db: Session, skip: int = 0, limit: int = 100):
    response = db.query(Student).offset(skip).limit(limit).all()
    result = []
    for student in response:
        student_schema = StudentSchema.model_validate(student, from_attributes=True)
        result.append(student_schema)
    return result


def get_student(db: Session, student_id: int):
    return db.query(Student).filter(Student.id == student_id).first()


def create_student(db: Session, student_in: StudentCreate):

    student = Student(user_id=student_in.user_id)
    logger.debug(f"Created student: {student}")
    db.add(student)
    db.commit()
    db.refresh(student)
    return student
