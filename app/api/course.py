from fastapi import APIRouter

router = APIRouter()

# Define course-related endpoints here
@router.get("/")
def read_courses():
    return {"message": "List of courses"}
