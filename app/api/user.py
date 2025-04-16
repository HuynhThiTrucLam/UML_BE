from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import uuid
from app.crud import user as crud_user
from app.schemas.user import User, UserCreate
from app.api.deps import get_db, get_current_active_user
from app.core.security import verify_access_token, create_access_token, pwd_context

router = APIRouter()

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_email(db, email=user_in.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud_user.create_user(db=db, user_in=user_in)

@router.get("/{user_id}", response_model=User)
def read_user(user_id: uuid.UUID, db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    user = crud_user.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud_user.get_user_by_email(db, email=form_data.username)
    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token = create_access_token({"sub": str(user.id), "role": user.role, "email": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
