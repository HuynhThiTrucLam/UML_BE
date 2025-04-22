from typing import Optional, Dict, List, Any
from uuid import UUID
from logging import getLogger
from sqlalchemy.orm import Session, joinedload
from app.models.course_registration import CourseRegistration
from app.models.exam_result import ExamResult
from app.models.exam import Exam
from app.models.student import Student
from app.schemas.student import StudentCreate, Student as StudentSchema, StudentUpdate
from sqlalchemy.sql import text
import uuid

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


def get_registered_students(db: Session, course_id: Optional[UUID]=None):
    filter_condition = f"AND cr.course_id = '{course_id}'" if course_id else ""
    query = text(f"""
        SELECT s.id as student_id, u.user_name as name, c.course_name, c.id as course_id,
            MAX(CASE WHEN ex.type = 'theory' THEN er.score ELSE NULL END) as theory_score,
            MAX(CASE WHEN ex.type = 'practice' THEN er.score ELSE NULL END) as practice_score
        FROM course_registrations cr
        LEFT JOIN courses c ON c.id = cr.course_id
        LEFT JOIN students s ON cr.student_id = s.id
        LEFT JOIN users u ON s.user_id = u.id
        LEFT JOIN exam_results er ON s.id = er.student_id 
        left join exams ex on ex.id = er.exam_id 
        WHERE cr.status = 'successful' {filter_condition}
        GROUP BY s.id, u.user_name, c.course_name, c.id
    """)
    result = db.execute(query)
    students = []
    for row in result:
        student_dict = {
            "student_id": str(row.student_id),
            "name": row.name,
            "course_name": row.course_name,
            "theory_score": row.theory_score,
            "practice_score": row.practice_score,
            "course_id": str(row.course_id)
        }
        students.append(student_dict)
    return students


def update_scores(db: Session, student_id: UUID, student_in: StudentUpdate):
    """
    Update or create exam results for a student
    
    Args:
        db: Database session
        student_id: UUID of the student
        student_in: StudentUpdate schema with course_id and scores
        
    Returns:
        List of registered students with updated scores
    """
    # Define a function to get or create exam
    def get_or_create_exam(course_id: UUID, exam_type: str):
        exam = db.query(Exam).filter(
            Exam.course_id == course_id,
            Exam.type == exam_type
        ).first()
        
        if not exam:
            # Create a new exam if one doesn't exist
            exam = Exam(
                id=uuid.uuid4(),
                course_id=course_id,
                type=exam_type
            )
            db.add(exam)
            db.commit()
            db.refresh(exam)
            
        return exam
    
    # Function to update or create an exam result
    def update_or_create_exam_result(student_id: UUID, exam_id: UUID, score: float):
        # Check if an exam result exists
        exam_result = db.query(ExamResult).filter(
            ExamResult.student_id == student_id,
            ExamResult.exam_id == exam_id
        ).first()
        print(f"exam_result: {exam_result}")
        if exam_result:
            # Update existing result
            exam_result.score = score
        else:
            # Create new result
            new_result = ExamResult(
                id=uuid.uuid4(),
                exam_id=exam_id,
                student_id=student_id,
                score=score
            )
            db.add(new_result)
        
        db.commit()
    
    # Update theory score if provided
    if student_in.theory_score is not None:
        theory_exam = get_or_create_exam(student_in.course_id, "theory")
        update_or_create_exam_result(student_id, theory_exam.id, student_in.theory_score)
    
    # Update practice score if provided
    if student_in.practical_score is not None:
        practice_exam = get_or_create_exam(student_in.course_id, "practice")
        update_or_create_exam_result(student_id, practice_exam.id, student_in.practical_score)
    
    # Return updated list of registered students for this course
    return get_registered_students(db, student_in.course_id)
