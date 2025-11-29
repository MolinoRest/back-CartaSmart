# app/routers/menu_items.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, crud
from ..deps import get_db

router = APIRouter(prefix="/menu-items", tags=["menu_items"])


@router.post("/", response_model=schemas.MenuItemRead)
def create_menu_item(
    item_in: schemas.MenuItemCreate,
    db: Session = Depends(get_db),
):
    item = crud.create_menu_item(db, item_in)
    return item


@router.get("/by-restaurant/{restaurant_id}", response_model=List[schemas.MenuItemRead])
def list_menu_items_by_restaurant(
    restaurant_id: int,
    db: Session = Depends(get_db),
):
    items = crud.get_menu_items_by_restaurant(db, restaurant_id)
    return items

@router.get("/by-menu_category/{menu_category_id}", response_model=List[schemas.MenuItemRead])
def list_menu_items_by_menu_category(
    menu_category_id: int,
    db: Session = Depends(get_db),
):
    items = crud.get_menu_items_by_menu_category_id(db, menu_category_id)
    return items


@router.get("/{menu_item_id}", response_model=schemas.MenuItemRead)
def get_menu_item(
    menu_item_id: int,
    db: Session = Depends(get_db),
):
    item = crud.get_menu_item(db, menu_item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return item


@router.put("/{menu_item_id}", response_model=schemas.MenuItemRead)
def update_menu_item(
    menu_item_id: int,
    item_in: schemas.MenuItemUpdate,
    db: Session = Depends(get_db),
):
    item = crud.update_menu_item(db, menu_item_id, item_in)
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return item


@router.delete("/{menu_item_id}", status_code=204)
def delete_menu_item(
    menu_item_id: int,
    db: Session = Depends(get_db),
):
    deleted = crud.delete_menu_item(db, menu_item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return
