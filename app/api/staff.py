from fastapi import APIRouter

router = APIRouter()


# Define staff-related endpoints here
@router.get("/")
def read_staffs():
    return {"message": "List of staffs"}
