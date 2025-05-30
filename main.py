from fastapi import FastAPI
from app.api import (
    course_registration,
    payment_method,
    user,
    student,
    staff,
    course,
    exam,
    payment,
    license_type,
    license,
    health_check_schedule,
    health_check_document,
    personal_infor_document,
    schedule,
    instructor
)
from app.core.database import engine, Base
from app.core.config import settings
from fastapi.middleware.cors import CORSMiddleware

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
app.include_router(
    license_type.router, prefix="/api/license_type", tags=["license_types"]
)
app.include_router(
    license.router, prefix="/api/licenses", tags=["licenses"]
)
app.include_router(
    health_check_schedule.router,
    prefix="/api/health_check_schedule",
    tags=["health_check_schedule"],
)
app.include_router(
    health_check_document.router,
    prefix="/api/health_check_document",
    tags=["health_check_document"],
)
app.include_router(
    personal_infor_document.router,
    prefix="/api/personal_infor_document",
    tags=["personal_infor_document"],
)
app.include_router(
    course_registration.router,
    prefix="/api/course_registration",
    tags=["course_registration"],
)
app.include_router(schedule.router, prefix="/api/schedule", tags=["schedule"])
app.include_router(payment_method.router, prefix="/api/payment_method", tags=["payment_method"])
app.include_router(instructor.router, prefix="/api/instructor", tags=["instructor"])


# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)


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
