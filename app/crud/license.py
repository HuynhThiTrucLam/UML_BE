from sqlalchemy.orm import Session
from app.models.license import License
from app.schemas.license import LicenseCreate, LicenseUpdate
from typing import List, Optional
import uuid


def get_licenses(db: Session, skip: int = 0, limit: int = 100):
    """Get all licenses with pagination"""
    return db.query(License).offset(skip).limit(limit).all()


def get_license_by_id(db: Session, license_id: int) -> Optional[License]:
    """Get a license by its ID"""
    return db.query(License).filter(License.id == license_id).first()


def get_license_by_number(db: Session, license_number: str) -> Optional[License]:
    """Get a license by its number"""
    return db.query(License).filter(License.license_number == license_number).first()


def get_licenses_by_student_id(db: Session, student_id: int) -> List[License]:
    """Get all licenses for a specific student"""
    return db.query(License).filter(License.student_id == student_id).all()


def get_licenses_by_license_type_id(db: Session, license_type_id: int) -> List[License]:
    """Get all licenses of a specific license type"""
    return db.query(License).filter(License.license_type_id == license_type_id).all()


def create_license(db: Session, license_obj: LicenseCreate) -> License:
    """Create a new license"""
    db_license = License(
        license_number=license_obj.license_number,
        license_type_id=license_obj.license_type_id,
        student_id=license_obj.student_id,
        expiration_date=license_obj.expiration_date,
        status=license_obj.status,
    )
    db.add(db_license)
    db.commit()
    db.refresh(db_license)
    return db_license


def update_license(
    db: Session, db_license: License, license_update: LicenseUpdate
) -> License:
    """Update an existing license"""
    update_data = license_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_license, key, value)

    db.commit()
    db.refresh(db_license)
    return db_license


def delete_license(db: Session, db_license: License) -> None:
    """Delete a license"""
    db.delete(db_license)
    db.commit()


def count_licenses(db: Session) -> int:
    """Count total number of licenses"""
    return db.query(License).count()