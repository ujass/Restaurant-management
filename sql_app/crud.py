from datetime import date
from sqlalchemy.orm import Session , join , outerjoin
import itertools
from sqlalchemy import and_

import models, schemas


# $$$$$$$$$$$$$$$$$$$$$$ food operations $$$$$$$$$$$$$$$$$$$$$$$$4

# def get_user(db: Session, user_id: int):
#     return db.query(models.User).filter(models.User.id == user_id).first()


def exist_food(db: Session , food_id : int):
    return db.query(models.Food).filter(models.Food.food_id == food_id).first()

def food_available(db: Session , food_id : int):
    food = db.query(models.Food).filter(models.Food.food_id == food_id).first()
    return food.food_quantity
    
def update_food(db: Session , food : schemas.Food,  food_id : int):
    food_available =  db.query(models.Food).filter(models.Food.food_id == food_id).first()
    print(food_available.food_id, food_available.food_name)
    food_available.food_name = food.food_name
    food_available.food_price = food.food_price
    food_available.food_category = food.food_category
    food_available.food_quantity = food.food_quantity

    db.commit()
    db.refresh(food_available)
    return food_available

def delete_food(db: Session, food_id : int):
    food_remove = db.query(models.Food).filter(models.Food.food_id == food_id).first()
    db.delete(food_remove)
    db.commit()
    return {"Food removed"}


def get_food_by_category(db: Session , category : str):
    return db.query(models.Food). filter(models.Food.food_category == category).all()
    
# def get_user_by_email(db: Session, email: str):
#     return db.query(models.User).filter(models.User.email == email).first()

# def get_users(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.User).offset(skip).limit(limit).all()


# def create_user(db: Session, user: schemas.UserCreate):
#     fake_hashed_password = user.password + "notreallyhashed"
#     db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user


# def get_items(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Item).offset(skip).limit(limit).all()


# def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
#     db_item = models.Item(**item.dict(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item


def create_food(db: Session, new_food: schemas.Food ):
    db_food = models.Food(**new_food.dict())
    db.add(db_food)
    db.commit()
    db.refresh(db_food)
    return db_food

def get_food(db: Session):
    return db.query(models.Food).all()




#  &&&&&&&&&&&&&&&&&& Customer operations &&&&&&&&&&&&&&&&&&&&&&&&&&&


def get_customer(db: Session):
    return db.query(models.Customer).all()


def create_customer(db: Session , new_customer : schemas.Customer):
    db_customer = models.Customer(**new_customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def validate_customer(db: Session , customer_id: int):
    return db.query(models.Customer).filter(models.Customer.id == customer_id).first()

# &&&&&&&&&&&&&&&& Upade & delete will be added lastly  &&&&&&&&&&&

# ********************* Order operations will be added here *************** 

def create_order(db: Session, customer_id : int , food_id : int ):
    db_order = models.Order()
    db_order.customer_id = customer_id
    db_order.food_id = food_id
    db.add(db_order)

    update_quantity = db.query(models.Food). filter(models.Food.food_id == food_id).first()
    update_quantity.food_quantity -= 1

    db.commit()
    print("commit done")
    db.refresh(db_order)
    return db_order


def delete_order(db: Session, order_id : int):
    order_remove = db.query(models.Order).filter(models.Order.id == order_id).first()
    print(order_remove.id )
    print("$$$$$$$$$$$$$$$$$$$$$$$$444")
    db.delete(order_remove)

    # update_quantity = db.query(models.Food). filter(models.Food.food_id == food_id).first()
    # update_quantity.food_quantity += 1
    db.commit()
    return {"Order removed"}    

def show_order(db: Session):
    return db.query(models.Order).all()


def feedback_add(db: Session , feedback_content : schemas.Feedback_data):
    add_content = models.Feedback(**feedback_content.dict())
    db.add(add_content)
    db.commit()
    db.refresh(add_content)
    return {"Feedback Added"}


# &&&&&&&&&&&&&&&& Bill &&&&&&&&&&&&&&&&&

def fatch_bill(db: Session , customer_id : int):
    # all_food = db.query(models.Order.food_id).filter(models.Order.customer_id == customer_id).all()
    customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    all_orders = customer.orders
    total = 0
    for each_order in all_orders:
        total += each_order.food.food_price
  
    return total


# @@@@@@@@@@@@@@@@@@@@@@@@@ Table reservation @@@@@@@@@@@@@@@@@@@@@@@@@@

def create_table(db: Session , new_table : schemas.Table):
    db_table = models.Table(**new_table.dict())
    db.add(db_table)
    db.commit()
    db.refresh(db_table)
    return db_table


def get_table(db: Session):
    return db.query(models.Table).all()

def create_reservation(db: Session, customer_id : int , table_id : int ):
    db_reservation = models.Reservation()
    db_reservation.customer_id = customer_id
    db_reservation.food_id = table_id
    db.add(db_reservation)

    update_reserved = db.query(models.Table). filter(models.Table.id == table_id).first()
    update_reserved.reserved = True

    db.commit()
    print("commit done")
    db.refresh(db_reservation)
    return db_reservation

def delete_reservation(db: Session, reservaion_id : int ):
    reservation_remove = db.query(models.Reservation).filter(models.Reservation.id == reservaion_id).first()
    
    db.delete(reservation_remove)
    # update_reserved = db.query(models.Table). filter(models.Table.id == table_id).first()
    # update_reserved.reserved = False

    db.commit()
    return {"Reservation Cancelled"} 


# !!!!!!!!!!!!!!!!!!!!!!! Table reservation system !!!!!!!!!!!!!!!!!!!!!!!!!!

def check_table(db: Session , check_available : schemas.Check_reservation , person : int):

    q = db.query(models.Table).outerjoin(models.Reservation , and_(models.Table.id == models.Reservation.table_id, models.Reservation.r_date == check_available.r_date,
        models.Reservation.slot == check_available.slot )).filter(models.Table.seat >= person, models.Reservation.id == None).all()
    return q


def create_reservation(db: Session , reservation_data : schemas.Do_reservation):
    add_rrservation = models.Reservation(**reservation_data.dict())
    db.add(add_rrservation)
    db.commit()
    db.refresh(add_rrservation)
    return {"Reservation done"}

def get_reservation(db: Session):
    return db.query(models.Reservation).all() 


