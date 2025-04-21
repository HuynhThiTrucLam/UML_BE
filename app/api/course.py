from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import uuid
from app.crud import course as crud_course
from app.schemas.course import Course, CourseCreate, CourseList, CourseUpdate
from app.api.deps import get_db, require_roles

router = APIRouter()

@router.post("/", response_model=Course, status_code=status.HTTP_201_CREATED)
def create_course(
    course_in: CourseCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(["admin"]))

):
    """
    Create a new course.
    
    Only administrators can create courses.
    """
    course = crud_course.create_course(db=db, course_in=course_in)
    return course

@router.get("/", response_model=CourseList)
def list_course(
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """
    Retrieve all courses.
    """
    courses = crud_course.get_courses(db, skip=skip, limit=limit)
    return courses

@router.get("/{course_id}", response_model=Course, summary="Get Course By ID")
def get_course_by_id(
    course_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    """
    Get a specific course by ID.
    """
    course = crud_course.get_course(db, course_id=course_id)
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

# update course
@router.put("/{course_id}", response_model=Course, summary="Update Course")
def update_course(
    course_id: uuid.UUID,
    course_in: CourseUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin"))
):
    """
    Update an existing course.
    
    This endpoint supports partial updates - you only need to include the fields you want to change.
    Fields not included in the request will retain their current values.
    
    Only administrators can update courses.
    """
    # Log the update request data
    print(f"Update request for course {course_id}: {course_in.model_dump(exclude_unset=True)}")
    
    try:
        course = crud_course.update_course(db=db, course_id=course_id, course_in=course_in)
        if course is None:
            raise HTTPException(status_code=404, detail="Course not found")
        return course
    except ValueError as e:
        # Provide more detailed error response
        error_msg = str(e)
        print(f"Validation error for course {course_id}: {error_msg}")
        raise HTTPException(
            status_code=422, 
            detail={"message": error_msg, "error_type": "validation_error"}
        )
    except Exception as e:
        # Log unexpected errors
        error_msg = str(e)
        print(f"Unexpected error updating course {course_id}: {error_msg}")
        raise HTTPException(
            status_code=500, 
            detail="An unexpected error occurred while updating the course"
        )
    
#delete course
@router.delete("/{course_id}", response_model=Course, summary="Delete Course")
def delete_course(
    course_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin"))
):
    """
    Delete a course by ID.
    
    Only administrators can delete courses.
    """
    course = crud_course.delete_course(db=db, course_id=course_id)
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course