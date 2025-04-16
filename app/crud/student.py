from sqlalchemy.orm import Session
from app.models.student import Student
from app.schemas.student import StudentCreate

def get_student(db: Session, student_id: int):
    return db.query(Student).filter(Student.id == student_id).first()

def create_student(db: Session, student_in: StudentCreate, user_id: int):
    student = Student(**student_in.dict(), user_id=user_id)
    db.add(student)
    db.commit()
    db.refresh(student)
    return student
