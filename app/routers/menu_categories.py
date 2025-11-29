# app/routers/menu_categories.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, crud
from ..deps import get_db

router = APIRouter(
    prefix="/menu-categories",
    tags=["menu_categories"],
)


@router.post("/", response_model=schemas.MenuCategoryRead)
def create_menu_category(
    category_in: schemas.MenuCategoryCreate,
    db: Session = Depends(get_db),
):
    return crud.create_menu_category(db, category_in)


@router.get("/", response_model=List[schemas.MenuCategoryRead])
def list_menu_categories(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    categories = crud.list_menu_categories(db, skip=skip, limit=limit)
    return categories


@router.get("/by-restaurant/{restaurant_id}", response_model=List[schemas.MenuCategoryRead])
def list_menu_categories_by_restaurant(
    restaurant_id: int,
    db: Session = Depends(get_db),
):
    categories = crud.list_menu_categories_by_restaurant(db, restaurant_id=restaurant_id)
    return categories


@router.get("/{category_id}", response_model=schemas.MenuCategoryRead)
def get_menu_category(
    category_id: int,
    db: Session = Depends(get_db),
):
    category = crud.get_menu_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Menu category not found")
    return category


@router.put("/{category_id}", response_model=schemas.MenuCategoryRead)
def update_menu_category(
    category_id: int,
    category_in: schemas.MenuCategoryBase,
    db: Session = Depends(get_db),
):
    category = crud.update_menu_category(db, category_id, category_in)
    if not category:
        raise HTTPException(status_code=404, detail="Menu category not found")
    return category


@router.delete("/{category_id}", status_code=204)
def delete_menu_category(
    category_id: int,
    db: Session = Depends(get_db),
):
    deleted = crud.delete_menu_category(db, category_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Menu category not found")
    return
