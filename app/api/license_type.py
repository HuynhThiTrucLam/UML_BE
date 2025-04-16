from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
import uuid

from app.api.deps import get_db, get_current_active_user, require_roles
from app.crud import license_type as crud
from app.schemas.license_type import LicenseType, LicenseTypeCreate, LicenseTypeList, LicenseTypeUpdate

router = APIRouter()


@router.post("/", response_model=LicenseType, status_code=status.HTTP_201_CREATED)
def create_license_type(
    *,
    db: Session = Depends(get_db),
    license_type_in: LicenseTypeCreate,
    _: dict = Depends(require_roles("admin"))  # Only admin can create
):
    """
    Create a new license type.
    Only accessible by admin users.
    """
    # Check if a license type with the same name already exists
    existing_license_type = crud.get_license_type_by_name(db, license_type_in.type_name)
    if existing_license_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"License type with name '{license_type_in.type_name}' already exists"
        )
    
    # Create the new license type
    return crud.create_license_type(db=db, license_type=license_type_in)


@router.get("/", response_model=LicenseTypeList)
def list_license_types(
    *,
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=100),
):
    """
    Retrieve license types with pagination.
    Accessible by asll users without authentication.
    """
    license_types = crud.get_license_types(db, skip=skip, limit=limit)
    total = crud.count_license_types(db)
    
    return {
        "items": license_types,
        "total": total
    }


@router.get("/{license_type_id}", response_model=LicenseType)
def get_license_type(
    *,
    db: Session = Depends(get_db),
    license_type_id: uuid.UUID, # Any authenticated user can access
):
    """
    Get a specific license type by ID.
    Accessible by all authenticated users.
    """
    license_type = crud.get_license_type_by_id(db, license_type_id=license_type_id)
    if not license_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="License type not found"
        )
    return license_type


@router.put("/{license_type_id}", response_model=LicenseType)
def update_license_type(
    *,
    db: Session = Depends(get_db),
    license_type_id: uuid.UUID,
    license_type_in: LicenseTypeUpdate,
    _: dict = Depends(require_roles("admin"))  # Only admin can update
):
    """
    Update a license type.
    Only accessible by admin users.
    """
    # Check if the license type exists
    db_license_type = crud.get_license_type_by_id(db, license_type_id=license_type_id)
    if not db_license_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="License type not found"
        )
    
    # If changing the type name, check if the new name already exists
    if license_type_in.type_name and license_type_in.type_name != db_license_type.type_name:
        existing_license_type = crud.get_license_type_by_name(db, license_type_in.type_name)
        if existing_license_type:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"License type with name '{license_type_in.type_name}' already exists"
            )
    
    # Update the license type
    return crud.update_license_type(db=db, db_license_type=db_license_type, license_type=license_type_in)

@router.delete("/{license_type_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_license_type(
    *,
    db: Session = Depends(get_db),
    license_type_id: uuid.UUID,
    _: dict = Depends(require_roles("admin"))  # Only admin can delete
):
    """
    Delete a license type.
    Only accessible by admin users.
    """
    # Check if the license type exists
    db_license_type = crud.get_license_type_by_id(db, license_type_id=license_type_id)
    if not db_license_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="License type not found"
        )
    
    # Delete the license type
    crud.delete_license_type(db=db, db_license_type=db_license_type)
    return None