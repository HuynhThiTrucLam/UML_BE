from fastapi import APIRouter

router = APIRouter()


# Define payment-related endpoints here
@router.get("/")
def read_payments():
    return {"message": "List of payments"}
