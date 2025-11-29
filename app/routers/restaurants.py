# app/routers/restaurants.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, crud
from ..deps import get_db

router = APIRouter(prefix="/restaurants", tags=["restaurants"])


@router.post("/", response_model=schemas.RestaurantRead)
def create_restaurant(
    restaurant_in: schemas.RestaurantCreate,
    db: Session = Depends(get_db),
):
    restaurant = crud.create_restaurant(db, restaurant_in)
    return restaurant


@router.get("/", response_model=List[schemas.RestaurantRead])
def list_restaurants(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    restaurants = crud.get_restaurants(db, skip, limit)
    return restaurants


@router.get("/{restaurant_id}", response_model=schemas.RestaurantRead)
def get_restaurant(
    restaurant_id: int,
    db: Session = Depends(get_db),
):
    restaurant = crud.get_restaurant(db, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant

@router.put("/{restaurant_id}", response_model=schemas.RestaurantRead)
def update_restaurant(
    restaurant_id: int,
    restaurant_in: schemas.RestaurantUpdate,
    db: Session = Depends(get_db),
):
    restaurant = crud.update_restaurant(db, restaurant_id, restaurant_in)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant


@router.delete("/{restaurant_id}", status_code=204)
def delete_restaurant(
    restaurant_id: int,
    db: Session = Depends(get_db),
):
    deleted = crud.delete_restaurant(db, restaurant_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return
