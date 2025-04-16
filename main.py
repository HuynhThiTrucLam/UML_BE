from fastapi import FastAPI
from app.api import user, student, staff, course, exam, payment, license_type
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
app.include_router(license_type.router, prefix="/api/license_type", tags=["license_types"])


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
