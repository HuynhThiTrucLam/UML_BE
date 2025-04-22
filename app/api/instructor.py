from typing import List
from fastapi import APIRouter, Depends
from app.api.deps import get_db
from app.schemas.instructor import InstructorResponse
from app.crud import instructor
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/",
    response_model=List[InstructorResponse],
            summary="List Instructors",)
async def list_instructors(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> List[InstructorResponse]:
    return instructor.list_instructors(db=db, skip=skip, limit=limit)
