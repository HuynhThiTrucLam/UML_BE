#!/bin/bash
# This script generates a FastAPI project structure for a driving license management website.
# It creates directories and files with boilerplate code for core configurations, models, schemas,
# CRUD operations, API routers, and the application entry point.

set -e

# Define the base directory for the project
BASE_DIR="app"

echo "Creating project directories..."

# Create directory structure
mkdir -p ${BASE_DIR}/{core,models,schemas,crud,api}

# Create __init__.py files to mark packages
touch ${BASE_DIR}/__init__.py
touch ${BASE_DIR}/core/__init__.py
touch ${BASE_DIR}/models/__init__.py
touch ${BASE_DIR}/schemas/__init__.py
touch ${BASE_DIR}/crud/__init__.py
touch ${BASE_DIR}/api/__init__.py

##############################
# Core configuration files
##############################

echo "Creating core configuration files..."

# app/core/config.py - Application configuration
cat << 'EOF' > ${BASE_DIR}/core/config.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./test.db"
    SECRET_KEY: str = "your-secret-key"
    ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"

settings = Settings()
EOF

# app/core/database.py - Database connection and session management
cat << 'EOF' > ${BASE_DIR}/core/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
EOF

# app/core/security.py - Security and password utilities
cat << 'EOF' > ${BASE_DIR}/core/security.py
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Placeholder for authentication and authorization functions
EOF

##############################
# SQLAlchemy models
##############################

echo "Creating SQLAlchemy ORM model files..."

# app/models/user.py
cat << 'EOF' > ${BASE_DIR}/models/user.py
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(String, nullable=False)  # e.g., "student", "staff", "admin"

    # One-to-One relationships
    student = relationship("Student", back_populates="user", uselist=False)
    staff = relationship("Staff", back_populates="user", uselist=False)
    
    # One-to-Many: a user might have multiple personal documents
    personal_documents = relationship("PersonalDocument", back_populates="user")
EOF

# app/models/student.py
cat << 'EOF' > ${BASE_DIR}/models/student.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    enrollment_number = Column(String, unique=True, index=True)
    course_of_study = Column(String)

    # Relationship back to user
    user = relationship("User", back_populates="student")
EOF

# app/models/staff.py
cat << 'EOF' > ${BASE_DIR}/models/staff.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Staff(Base):
    __tablename__ = "staffs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    department = Column(String)
    certification = Column(String)

    # Relationship back to user
    user = relationship("User", back_populates="staff")
EOF

# app/models/personal_document.py
cat << 'EOF' > ${BASE_DIR}/models/personal_document.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class PersonalDocument(Base):
    __tablename__ = "personal_documents"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    document_type = Column(String)
    document_url = Column(String)

    user = relationship("User", back_populates="personal_documents")
EOF

# app/models/student_health_check.py
cat << 'EOF' > ${BASE_DIR}/models/student_health_check.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class StudentHealthCheck(Base):
    __tablename__ = "student_health_checks"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    status = Column(String)
    remarks = Column(String)

    # Relationship to Student can be defined here
EOF

# app/models/health_check_schedule.py
cat << 'EOF' > ${BASE_DIR}/models/health_check_schedule.py
from sqlalchemy import Column, Integer, String, DateTime
from app.core.database import Base

class HealthCheckSchedule(Base):
    __tablename__ = "health_check_schedules"
    
    id = Column(Integer, primary_key=True, index=True)
    scheduled_date = Column(DateTime)
    description = Column(String)
EOF

# app/models/license_type.py
cat << 'EOF' > ${BASE_DIR}/models/license_type.py
from sqlalchemy import Column, Integer, String
from app.core.database import Base

class LicenseType(Base):
    __tablename__ = "license_types"
    
    id = Column(Integer, primary_key=True, index=True)
    type_name = Column(String, unique=True)
    description = Column(String)
EOF

# app/models/license.py
cat << 'EOF' > ${BASE_DIR}/models/license.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class License(Base):
    __tablename__ = "licenses"
    
    id = Column(Integer, primary_key=True, index=True)
    license_number = Column(String, unique=True)
    license_type_id = Column(Integer, ForeignKey("license_types.id"))
    student_id = Column(Integer, ForeignKey("students.id"))

    # Relationships
    license_type = relationship("LicenseType")
    # You can define a relationship with Student if needed
EOF

# app/models/course.py
cat << 'EOF' > ${BASE_DIR}/models/course.py
from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Course(Base):
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True, index=True)
    course_name = Column(String, index=True)
    description = Column(String)
EOF

# app/models/course_registration.py
cat << 'EOF' > ${BASE_DIR}/models/course_registration.py
from sqlalchemy import Column, Integer, ForeignKey
from app.core.database import Base

class CourseRegistration(Base):
    __tablename__ = "course_registrations"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))
EOF

# app/models/theory_class.py
cat << 'EOF' > ${BASE_DIR}/models/theory_class.py
from sqlalchemy import Column, Integer, String, DateTime
from app.core.database import Base

class TheoryClass(Base):
    __tablename__ = "theory_classes"
    
    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String)
    scheduled_time = Column(DateTime)
EOF

# app/models/practice_class.py
cat << 'EOF' > ${BASE_DIR}/models/practice_class.py
from sqlalchemy import Column, Integer, String, DateTime
from app.core.database import Base

class PracticeClass(Base):
    __tablename__ = "practice_classes"
    
    id = Column(Integer, primary_key=True, index=True)
    location = Column(String)
    scheduled_time = Column(DateTime)
EOF

# app/models/payment_method.py
cat << 'EOF' > ${BASE_DIR}/models/payment_method.py
from sqlalchemy import Column, Integer, String
from app.core.database import Base

class PaymentMethod(Base):
    __tablename__ = "payment_methods"
    
    id = Column(Integer, primary_key=True, index=True)
    method = Column(String, unique=True)
EOF

# app/models/payment.py
cat << 'EOF' > ${BASE_DIR}/models/payment.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.core.database import Base

class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    payment_method_id = Column(Integer, ForeignKey("payment_methods.id"))
    student_id = Column(Integer, ForeignKey("students.id"))
EOF

# app/models/exam.py
cat << 'EOF' > ${BASE_DIR}/models/exam.py
from sqlalchemy import Column, Integer, String, DateTime
from app.core.database import Base

class Exam(Base):
    __tablename__ = "exams"
    
    id = Column(Integer, primary_key=True, index=True)
    exam_name = Column(String)
    scheduled_time = Column(DateTime)
EOF

# app/models/exam_result.py
cat << 'EOF' > ${BASE_DIR}/models/exam_result.py
from sqlalchemy import Column, Integer, String, ForeignKey
from app.core.database import Base

class ExamResult(Base):
    __tablename__ = "exam_results"
    
    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, ForeignKey("exams.id"))
    student_id = Column(Integer, ForeignKey("students.id"))
    result = Column(String)
EOF

# app/models/staff_certification.py
cat << 'EOF' > ${BASE_DIR}/models/staff_certification.py
from sqlalchemy import Column, Integer, String, ForeignKey
from app.core.database import Base

class StaffCertification(Base):
    __tablename__ = "staff_certifications"
    
    id = Column(Integer, primary_key=True, index=True)
    staff_id = Column(Integer, ForeignKey("staffs.id"))
    certification_name = Column(String)
EOF

# app/models/vehicle.py
cat << 'EOF' > ${BASE_DIR}/models/vehicle.py
from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Vehicle(Base):
    __tablename__ = "vehicles"
    
    id = Column(Integer, primary_key=True, index=True)
    vehicle_number = Column(String, unique=True)
    model = Column(String)
EOF

# app/models/vehicle_maintenance.py
cat << 'EOF' > ${BASE_DIR}/models/vehicle_maintenance.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.core.database import Base

class VehicleMaintenance(Base):
    __tablename__ = "vehicle_maintenance"
    
    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))
    maintenance_date = Column(DateTime)
    description = Column(String)
EOF

# app/models/complaint.py
cat << 'EOF' > ${BASE_DIR}/models/complaint.py
from sqlalchemy import Column, Integer, String, ForeignKey
from app.core.database import Base

class Complaint(Base):
    __tablename__ = "complaints"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    description = Column(String)
EOF

# app/models/absent_form.py
cat << 'EOF' > ${BASE_DIR}/models/absent_form.py
from sqlalchemy import Column, Integer, String, ForeignKey
from app.core.database import Base

class AbsentForm(Base):
    __tablename__ = "absent_forms"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    reason = Column(String)
EOF

##############################
# Pydantic Schemas
##############################

echo "Creating Pydantic schema files..."

# app/schemas/user.py
cat << 'EOF' > ${BASE_DIR}/schemas/user.py
from pydantic import BaseModel, EmailStr
from typing import Optional

# Shared properties
class UserBase(BaseModel):
    email: EmailStr

# Schema for creating a user
class UserCreate(UserBase):
    password: str
    role: str

# Schema for updating a user
class UserUpdate(UserBase):
    is_active: Optional[bool] = True

# Schema for DB model
class UserInDBBase(UserBase):
    id: int
    is_active: bool
    role: str

    class Config:
        orm_mode = True

# Response schema
class User(UserInDBBase):
    pass
EOF

# Repeat a similar pattern for other schema files (student, staff, etc.)
cat << 'EOF' > ${BASE_DIR}/schemas/student.py
from pydantic import BaseModel
from typing import Optional

class StudentBase(BaseModel):
    enrollment_number: str
    course_of_study: Optional[str] = None

class StudentCreate(StudentBase):
    pass

class StudentInDB(StudentBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

class Student(StudentInDB):
    pass
EOF

# You can add additional schemas for staff, personal_document, etc. following the same pattern.
# For brevity, only user and student schemas are shown.

##############################
# CRUD Operations
##############################

echo "Creating CRUD operation files..."

# app/crud/user.py
cat << 'EOF' > ${BASE_DIR}/crud/user.py
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user_in: UserCreate):
    hashed_password = get_password_hash(user_in.password)
    user = User(
        email=user_in.email,
        hashed_password=hashed_password,
        role=user_in.role
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update_user(db: Session, user: User, user_in: UserUpdate):
    update_data = user_in.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
EOF

# app/crud/student.py (example CRUD for Student)
cat << 'EOF' > ${BASE_DIR}/crud/student.py
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
EOF

# Additional CRUD modules (staff, course, etc.) would follow a similar pattern.

##############################
# API Routers
##############################

echo "Creating API router files..."

# app/api/deps.py - Common dependencies
cat << 'EOF' > ${BASE_DIR}/api/deps.py
from app.core.database import SessionLocal
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Security dependency placeholder
def get_current_active_user():
    # Dummy user for demonstration; replace with actual token-based auth logic.
    dummy_user = {"id": 1, "email": "user@example.com", "is_active": True, "role": "student"}
    return dummy_user
EOF

# app/api/user.py - User endpoints
cat << 'EOF' > ${BASE_DIR}/api/user.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.crud import user as crud_user
from app.schemas.user import User, UserCreate
from app.api.deps import get_db, get_current_active_user

router = APIRouter()

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_email(db, email=user_in.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud_user.create_user(db=db, user_in=user_in)

@router.get("/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    user = crud_user.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
EOF

# app/api/student.py - Student endpoints
cat << 'EOF' > ${BASE_DIR}/api/student.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.crud import student as crud_student
from app.schemas.student import Student, StudentCreate
from app.api.deps import get_db, get_current_active_user

router = APIRouter()

@router.post("/", response_model=Student, status_code=status.HTTP_201_CREATED)
def create_student(student_in: StudentCreate, db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    return crud_student.create_student(db=db, student_in=student_in, user_id=current_user["id"])

@router.get("/{student_id}", response_model=Student)
def read_student(student_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    student = crud_student.get_student(db, student_id=student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student
EOF

# app/api/staff.py - Staff endpoints (example placeholder)
cat << 'EOF' > ${BASE_DIR}/api/staff.py
from fastapi import APIRouter

router = APIRouter()

# Define staff-related endpoints here
@router.get("/")
def read_staffs():
    return {"message": "List of staffs"}
EOF

# app/api/course.py - Course endpoints (example placeholder)
cat << 'EOF' > ${BASE_DIR}/api/course.py
from fastapi import APIRouter

router = APIRouter()

# Define course-related endpoints here
@router.get("/")
def read_courses():
    return {"message": "List of courses"}
EOF

# app/api/exam.py - Exam endpoints (example placeholder)
cat << 'EOF' > ${BASE_DIR}/api/exam.py
from fastapi import APIRouter

router = APIRouter()

# Define exam-related endpoints here
@router.get("/")
def read_exams():
    return {"message": "List of exams"}
EOF

# app/api/payment.py - Payment endpoints (example placeholder)
cat << 'EOF' > ${BASE_DIR}/api/payment.py
from fastapi import APIRouter

router = APIRouter()

# Define payment-related endpoints here
@router.get("/")
def read_payments():
    return {"message": "List of payments"}
EOF

##############################
# Main application file
##############################

echo "Creating main.py..."

cat << 'EOF' > main.py
from fastapi import FastAPI
from app.api import user, student, staff, course, exam, payment
from app.core.database import engine, Base
from app.core.config import settings

# Create all tables (for production, use migrations instead)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Driving License Management API", version="1.0.0")

# Include API routers
app.include_router(user.router, prefix="/api/users", tags=["users"])
app.include_router(student.router, prefix="/api/students", tags=["students"])
app.include_router(staff.router, prefix="/api/staffs", tags=["staffs"])
app.include_router(course.router, prefix="/api/courses", tags=["courses"])
app.include_router(exam.router, prefix="/api/exams", tags=["exams"])
app.include_router(payment.router, prefix="/api/payments", tags=["payments"])

@app.on_event("startup")
async def startup_event():
    # Initialize any startup events here
    pass

@app.on_event("shutdown")
async def shutdown_event():
    # Cleanup tasks on shutdown
    pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
EOF

echo "Project structure generated successfully."
