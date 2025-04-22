from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
import uuid

from app.api.deps import get_db, get_current_active_user, require_roles
from app.crud import license as crud
from app.schemas.license import (
    License,
    LicenseCreate,
    LicenseList,
    LicenseUpdate,
)

router = APIRouter()


@router.post("/", response_model=License, status_code=status.HTTP_201_CREATED)
def create_license(
    *,
    db: Session = Depends(get_db),
    license_in: LicenseCreate,
    _: dict = Depends(require_roles("admin")),  # Only admin can create
):
    """
    Create a new license.
    Only accessible by admin users.
    """
    # Check if a license with the same number already exists
    existing_license = crud.get_license_by_number(db, license_in.license_number)
    if existing_license:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"License with number '{license_in.license_number}' already exists",
        )

    # Create the new license
    return crud.create_license(db=db, license_obj=license_in)


@router.get("/", response_model=LicenseList)
def list_licenses(
    *,
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=100),
    _: dict = Depends(require_roles(["admin", "staff"])),  # Admin or staff can access
):
    """
    Retrieve licenses with pagination.
    Accessible by admin and staff users.
    """
    licenses = crud.get_licenses(db, skip=skip, limit=limit)
    total = crud.count_licenses(db)

    return {"items": licenses, "total": total}


@router.get("/{license_id}", response_model=License)
def get_license(
    *,
    db: Session = Depends(get_db),
    license_id: int,
    _: dict = Depends(require_roles(["admin", "staff"])),  # Admin or staff can access
):
    """
    Get a specific license by ID.
    Accessible by admin and staff users.
    """
    license = crud.get_license_by_id(db, license_id=license_id)
    if not license:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="License not found"
        )
    return license


@router.get("/student/{student_id}", response_model=List[License])
def get_licenses_by_student(
    *,
    db: Session = Depends(get_db),
    student_id: int,
    _: dict = Depends(require_roles(["admin", "staff"])),  # Admin or staff can access
):
    """
    Get all licenses for a specific student.
    Accessible by admin and staff users.
    """
    licenses = crud.get_licenses_by_student_id(db, student_id=student_id)
    return licenses


@router.get("/type/{license_type_id}", response_model=List[License])
def get_licenses_by_type(
    *,
    db: Session = Depends(get_db),
    license_type_id: int,
    _: dict = Depends(require_roles(["admin", "staff"])),  # Admin or staff can access
):
    """
    Get all licenses of a specific license type.
    Accessible by admin and staff users.
    """
    licenses = crud.get_licenses_by_license_type_id(db, license_type_id=license_type_id)
    return licenses


@router.get("/number/{license_number}", response_model=License)
def get_license_by_number(
    *,
    db: Session = Depends(get_db),
    license_number: str,
    _: dict = Depends(require_roles(["admin", "staff"])),  # Admin or staff can access
):
    """
    Get a license by its number.
    Accessible by admin and staff users.
    """
    license = crud.get_license_by_number(db, license_number=license_number)
    if not license:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="License not found"
        )
    return license


@router.put("/{license_id}", response_model=License)
def update_license(
    *,
    db: Session = Depends(get_db),
    license_id: int,
    license_in: LicenseUpdate,
    _: dict = Depends(require_roles("admin")),  # Only admin can update
):
    """
    Update a license.
    Only accessible by admin users.
    """
    # Check if the license exists
    db_license = crud.get_license_by_id(db, license_id=license_id)
    if not db_license:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="License not found"
        )

    # If changing the license number, check if the new number already exists
    if (
        license_in.license_number
        and license_in.license_number != db_license.license_number
    ):
        existing_license = crud.get_license_by_number(db, license_in.license_number)
        if existing_license:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"License with number '{license_in.license_number}' already exists",
            )

    # Update the license
    return crud.update_license(
        db=db, db_license=db_license, license_update=license_in
    )


@router.delete("/{license_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_license(
    *,
    db: Session = Depends(get_db),
    license_id: int,
    _: dict = Depends(require_roles("admin")),  # Only admin can delete
):
    """
    Delete a license.
    Only accessible by admin users.
    """
    # Check if the license exists
    db_license = crud.get_license_by_id(db, license_id=license_id)
    if not db_license:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="License not found"
        )

    # Delete the license
    crud.delete_license(db=db, db_license=db_license)
    return None