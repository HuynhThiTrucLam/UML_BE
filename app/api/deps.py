from app.core.database import SessionLocal
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import uuid
from app.core.security import verify_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_active_user(token: str = Depends(oauth2_scheme)):
    payload = verify_access_token(token)
    # You may want to fetch the user from the DB here using payload["sub"]
    user = {"id": uuid.UUID(payload["sub"]), "email": payload["email"], "role": payload["role"]}
    return user

def require_roles(*roles):
    def role_checker(current_user=Depends(get_current_active_user)):
        if current_user["role"] not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Operation not permitted for role: {current_user['role']}"
            )
        return current_user
    return role_checker
