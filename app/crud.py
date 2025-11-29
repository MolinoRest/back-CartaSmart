# app/crud.py
from decimal import Decimal
from typing import List, Optional
from sqlalchemy.orm import Session

from . import models, schemas


# ---------- Restaurant ----------
def create_restaurant(db: Session, restaurant_in: schemas.RestaurantCreate) -> models.Restaurant:
    restaurant = models.Restaurant(**restaurant_in.model_dump())
    db.add(restaurant)
    db.commit()
    db.refresh(restaurant)
    return restaurant


def get_restaurants(db: Session, skip: int = 0, limit: int = 100) -> List[models.Restaurant]:
    return db.query(models.Restaurant).offset(skip).limit(limit).all()


def get_restaurant(db: Session, restaurant_id: int) -> Optional[models.Restaurant]:
    return db.query(models.Restaurant).filter(models.Restaurant.id == restaurant_id).first()

def update_restaurant(
    db: Session,
    restaurant_id: int,
    restaurant_in: schemas.RestaurantUpdate,
) -> Optional[models.Restaurant]:
    restaurant = get_restaurant(db, restaurant_id)
    if not restaurant:
        return None

    data = restaurant_in.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(restaurant, field, value)

    db.add(restaurant)
    db.commit()
    db.refresh(restaurant)
    return restaurant

def delete_restaurant(db: Session, restaurant_id: int) -> bool:
    restaurant = get_restaurant(db, restaurant_id)
    if not restaurant:
        return False

    db.delete(restaurant)
    db.commit()
    return True


# ---------- Menu Item ----------
def create_menu_item(db: Session, item_in: schemas.MenuItemCreate) -> models.MenuItem:
    item = models.MenuItem(**item_in.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def get_menu_items_by_restaurant(db: Session, restaurant_id: int) -> List[models.MenuItem]:
    return (
        db.query(models.MenuItem)
        .filter(models.MenuItem.restaurant_id == restaurant_id, models.MenuItem.is_available == True)
        .all()
    )

def get_menu_items_by_menu_category_id(db: Session, menu_category_id: int) -> List[models.MenuItem]:
    return(
        db.query(models.MenuItem)
        .filter(models.MenuItem.category_id == menu_category_id, models.MenuItem.is_available == True)
        .all()
    )

def get_menu_item(db: Session, menu_item_id: int) -> Optional[models.MenuItem]:
    return db.query(models.MenuItem).filter(models.MenuItem.id == menu_item_id).first()


def update_menu_item(
    db: Session,
    menu_item_id: int,
    item_in: schemas.MenuItemUpdate,
) -> Optional[models.MenuItem]:
    item = get_menu_item(db, menu_item_id)
    if not item:
        return None

    data = item_in.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(item, field, value)

    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def delete_menu_item(db: Session, menu_item_id: int) -> bool:
    item = get_menu_item(db, menu_item_id)
    if not item:
        return False

    db.delete(item)
    db.commit()
    return True



# ---------- Customer ----------
def get_or_create_customer(db: Session, customer_in: schemas.CustomerCreate) -> models.Customer:
    if customer_in.email:
        existing = db.query(models.Customer).filter(models.Customer.email == customer_in.email).first()
        if existing:
            return existing
    customer = models.Customer(**customer_in.model_dump())
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer

def get_customer(db: Session, customer_id: int) -> Optional[models.Customer]:
    return db.query(models.Customer).filter(models.Customer.id == customer_id).first()


def get_customers(db: Session, skip: int = 0, limit: int = 100) -> List[models.Customer]:
    return db.query(models.Customer).offset(skip).limit(limit).all()


def update_customer(
    db: Session,
    customer_id: int,
    customer_in: schemas.CustomerUpdate,
) -> Optional[models.Customer]:
    customer = get_customer(db, customer_id)
    if not customer:
        return None

    data = customer_in.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(customer, field, value)

    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


def delete_customer(db: Session, customer_id: int) -> bool:
    customer = get_customer(db, customer_id)
    if not customer:
        return False

    db.delete(customer)
    db.commit()
    return True



# ---------- Order ----------
def create_order(db: Session, order_in: schemas.OrderCreate) -> models.Order:
    restaurant = db.query(models.Restaurant).filter(models.Restaurant.id == order_in.restaurant_id).first()
    if not restaurant:
        raise ValueError("Restaurant not found")

    customer = db.query(models.Customer).filter(models.Customer.id == order_in.customer_id).first()
    if not customer:
        raise ValueError("Customer not found")

    # Calculamos total usando los precios actuales
    total = Decimal("0.00")
    order_items_models: List[models.OrderItem] = []

    for item_in in order_in.items:
        menu_item = db.query(models.MenuItem).filter(models.MenuItem.id == item_in.menu_item_id).first()
        if not menu_item or not menu_item.is_available:
            raise ValueError(f"Menu item {item_in.menu_item_id} not available")

        unit_price = Decimal(menu_item.price)
        if menu_item.discount:
          discount_price = Decimal(menu_item.discount)
          unit_price = unit_price - ((discount_price/100) * unit_price)
        
        subtotal = unit_price * item_in.quantity
        total += subtotal

        order_item = models.OrderItem(
            menu_item_id=menu_item.id,
            quantity=item_in.quantity,
            unit_price=unit_price,
            subtotal=subtotal,
        )
        order_items_models.append(order_item)

    order = models.Order(
        restaurant_id=order_in.restaurant_id,
        customer_id=order_in.customer_id,
        total_amount=total,
        status="pending",
        channel="chatbot",
    )
    db.add(order)
    db.flush()  # para obtener order.id antes de commit

    for oi in order_items_models:
        oi.order_id = order.id
        db.add(oi)

    db.commit()
    db.refresh(order)
    return order


def get_order(db: Session, order_id: int) -> Optional[models.Order]:
    return db.query(models.Order).filter(models.Order.id == order_id).first()


def list_orders_by_customer(db: Session, customer_id: int) -> List[models.Order]:
    return db.query(models.Order).filter(models.Order.customer_id == customer_id).all()

def update_order(
    db: Session,
    order_id: int,
    order_in: schemas.OrderUpdate,
) -> Optional[models.Order]:
    order = get_order(db, order_id)
    if not order:
        return None

    data = order_in.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(order, field, value)

    db.add(order)
    db.commit()
    db.refresh(order)
    return order


def delete_order(db: Session, order_id: int) -> bool:
    order = get_order(db, order_id)
    if not order:
        return False

    db.delete(order)
    db.commit()
    return True




# ---------- Menu Category ----------

def create_menu_category(db: Session, category_in: schemas.MenuCategoryCreate) -> models.MenuCategory:
    category = models.MenuCategory(
        restaurant_id=category_in.restaurant_id,
        name=category_in.name,
    )
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def get_menu_category(db: Session, category_id: int) -> Optional[models.MenuCategory]:
    return db.query(models.MenuCategory).filter(models.MenuCategory.id == category_id).first()


def list_menu_categories(
    db: Session,
    skip: int = 0,
    limit: int = 100,
) -> List[models.MenuCategory]:
    return db.query(models.MenuCategory).offset(skip).limit(limit).all()


def list_menu_categories_by_restaurant(
    db: Session,
    restaurant_id: int,
) -> List[models.MenuCategory]:
    return (
        db.query(models.MenuCategory)
        .filter(models.MenuCategory.restaurant_id == restaurant_id)
        .all()
    )


def update_menu_category(
    db: Session,
    category_id: int,
    category_in: schemas.MenuCategoryBase,
) -> Optional[models.MenuCategory]:
    category = get_menu_category(db, category_id)
    if not category:
        return None

    if category_in.name is not None:
        category.name = category_in.name

    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def delete_menu_category(db: Session, category_id: int) -> bool:
    category = get_menu_category(db, category_id)
    if not category:
        return False

    db.delete(category)
    db.commit()
    return True