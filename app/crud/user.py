from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash
import uuid
from datetime import datetime


def get_user(db: Session, user_id: uuid.UUID):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.user_name == username).first()


def create_user(db: Session, user_in: UserCreate):
    hashed_password = get_password_hash(user_in.password)
    user = User(
        user_name=user_in.user_name,
        email=user_in.email,
        phone_number=user_in.phone_number,
        hashed_password=hashed_password,
        role=user_in.role,
        created_at=datetime.now().isoformat(),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, user: User, user_in: UserUpdate):
    update_data = user_in.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
