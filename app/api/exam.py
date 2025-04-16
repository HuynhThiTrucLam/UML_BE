from fastapi import APIRouter

router = APIRouter()

# Define exam-related endpoints here
@router.get("/")
def read_exams():
    return {"message": "List of exams"}
