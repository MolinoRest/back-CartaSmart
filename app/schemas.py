# app/schemas.py
from typing import List, Optional
from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import datetime


# ---------- Restaurant ----------
class RestaurantBase(BaseModel):
    name: str
    address: Optional[str] = None
    phone: Optional[str] = None
    is_active: bool = True


class RestaurantCreate(RestaurantBase):
    pass


class RestaurantUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = None


class RestaurantRead(RestaurantBase):
    id: int

    class Config:
        from_attributes = True


# ---------- Menu Category ----------
class MenuCategoryBase(BaseModel):
    name: str


class MenuCategoryCreate(MenuCategoryBase):
    restaurant_id: int


class MenuCategoryRead(MenuCategoryBase):
    id: int
    restaurant_id: int

    class Config:
        from_attributes = True


# ---------- Menu Item ----------
class MenuItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: Decimal = Field(..., gt=0)
    discount: Optional[Decimal] = Field(
        default=None,
        ge=0,
        le=100,
        description="Porcentaje de descuento 0-100"
    )
    is_available: bool = True


class MenuItemCreate(MenuItemBase):
    restaurant_id: int
    category_id: Optional[int] = None


class MenuItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    discount: Optional[Decimal] = None
    is_available: Optional[bool] = None
    category_id: Optional[int] = None


class MenuItemRead(MenuItemBase):
    id: int
    restaurant_id: int
    category_id: Optional[int]

    class Config:
        from_attributes = True


# ---------- Customer ----------
class CustomerBase(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None


class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None


class CustomerRead(CustomerBase):
    id: int

    class Config:
        from_attributes = True


# ---------- Orders ----------
class OrderItemCreate(BaseModel):
    menu_item_id: int
    quantity: int = Field(..., gt=0)


class OrderItemRead(BaseModel):
    id: int
    menu_item_id: int
    quantity: int
    unit_price: Decimal
    subtotal: Decimal

    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    restaurant_id: int
    customer_id: int
    items: List[OrderItemCreate]

class OrderUpdate(BaseModel):
    status: Optional[str] = None       # pending, confirmed, preparing, delivered, cancelled
    channel: Optional[str] = None



class OrderRead(BaseModel):
    id: int
    restaurant_id: int
    customer_id: int
    status: str
    total_amount: Decimal
    channel: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    items: List[OrderItemRead] = []

    class Config:
        from_attributes = True
