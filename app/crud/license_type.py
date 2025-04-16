from sqlalchemy.orm import Session
from app.models.license_type import LicenseType
from app.schemas.license_type import LicenseTypeCreate, LicenseTypeUpdate
import uuid
from typing import List, Optional


def get_license_types(db: Session, skip: int = 0, limit: int = 100) -> List[LicenseType]:
    """Get all license types with pagination"""
    return db.query(LicenseType).offset(skip).limit(limit).all()


def get_license_type_by_id(db: Session, license_type_id: uuid.UUID) -> Optional[LicenseType]:
    """Get a license type by its ID"""
    return db.query(LicenseType).filter(LicenseType.id == license_type_id).first()


def get_license_type_by_name(db: Session, type_name: str) -> Optional[LicenseType]:
    """Get a license type by its name"""
    return db.query(LicenseType).filter(LicenseType.type_name == type_name).first()


def create_license_type(db: Session, license_type: LicenseTypeCreate) -> LicenseType:
    """Create a new license type"""
    db_license_type = LicenseType(
        type_name=license_type.type_name,
        age_requirement=license_type.age_requirement,
        health_requirements=license_type.health_requirements,
        training_duration=license_type.training_duration,
        fee=license_type.fee,
    )
    db.add(db_license_type)
    db.commit()
    db.refresh(db_license_type)
    return db_license_type


def update_license_type(
    db: Session, db_license_type: LicenseType, license_type: LicenseTypeUpdate
) -> LicenseType:
    """Update an existing license type"""
    # Only update fields that are provided
    update_data = license_type.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_license_type, key, value)
    
    db.commit()
    db.refresh(db_license_type)
    return db_license_type


def delete_license_type(db: Session, db_license_type: LicenseType) -> None:
    """Delete a license type"""
    db.delete(db_license_type)
    db.commit()


def count_license_types(db: Session) -> int:
    """Count total number of license types"""
    return db.query(LicenseType).count()