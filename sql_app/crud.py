from datetime import date
from sqlalchemy.orm import Session , join , outerjoin
import itertools
from sqlalchemy import and_
from fastapi import HTTPException

import models, schemas


# $$$$$$$$$$$$$$$$$$$$$$ food operations $$$$$$$$$$$$$$$$$$$$$$$$4

def exist_food(db: Session , food_id : int):
    return db.query(models.Food).filter(models.Food.food_id == food_id).first()

def food_available(db: Session , food_id : int):
    return db.query(models.Food).filter(and_(models.Food.food_id == food_id,models.Food.food_quantity > 0)).first()

def get_food(db: Session):
    return db.query(models.Food).all()


def get_food_by_category(db: Session , category : str):
    return db.query(models.Food). filter(models.Food.food_category == category).all()


def create_food(db: Session, new_food: schemas.Food_data ):
    db_food = models.Food(**new_food.dict())
    db.add(db_food)
    db.commit()
    db.refresh(db_food)
    return db_food

    
def update_food(db: Session , food : schemas.Food_data,  food_id : int):
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


#  &&&&&&&&&&&&&&&&&& Customer operations &&&&&&&&&&&&&&&&&&&&&&&&&&&

def get_customer(db: Session):
    return db.query(models.Customer).all()

def validate_customer(db: Session , customer_id: int):
    return db.query(models.Customer).filter(models.Customer.id == customer_id).first()


def create_customer(db: Session , new_customer : str):
    db_customer = models.Customer()
    db_customer.name = new_customer
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer



# ********************* Order operations will be added here *************** 

def show_order(db: Session):
    return db.query(models.Order).all()


def create_order(db: Session, customer_id : int , food_id : int ):
    db_order = models.Order()
    db_order.customer_id = customer_id
    db_order.food_id = food_id
    db_order.status = "Order Created"
    db.add(db_order)

    update_quantity = db.query(models.Food). filter(models.Food.food_id == food_id).first()
    update_quantity.food_quantity -= 1

    db.commit()
    print("commit done")
    db.refresh(db_order)
    return db_order


def feedback_add(db: Session , feedback_content : schemas.Feedback_data):
    add_content = models.Feedback(**feedback_content.dict())
    db.add(add_content)
    db.commit()
    db.refresh(add_content)
    return {"Feedback Added"}



def order_update(db: Session, order_id: int, update_status: str ):
    current_status = db.query(models.Order).filter(models.Order.id == order_id).first()
    print(current_status.status)
    if current_status.status == "Order Created" and update_status == "Order Processed" :
        current_status.status = "Order Processed"
        db.commit()
        db.refresh(current_status)
        return current_status    

    if current_status.status == "Order Processed" and update_status == "Order Delivered" :
        current_status.status = "Order Delivered"
        db.commit()
        db.refresh(current_status)
        return current_status

    return {"Can not update order"}
            

def delete_order(db: Session, order_id : int):
    order_remove = db.query(models.Order).filter(models.Order.id == order_id).first()
    if order_remove is None:
        raise HTTPException(status_code=404, detail="Wrong Orderd ID")
    else:
        db.delete(order_remove)

        update_quantity = db.query(models.Food). filter(models.Food.food_id == order_remove.food_id).first()
        update_quantity.food_quantity += 1
        db.commit()
        return {"Order removed"}    

# &&&&&&&&&&&&&&&& Bill &&&&&&&&&&&&&&&&&

def fatch_bill(db: Session , customer_id : int):
    # all_food = db.query(models.Order.food_id).filter(models.Order.customer_id == customer_id).all()
    customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    all_orders = customer.orders
    total = 0
    for each_order in all_orders:
        total += each_order.food.food_price
  
    return total


#&&&&&&&&&&&&&&&&&&&&&&&&&&&& Table Details &&&&&&&&&&&&&&&&&&&

def get_table(db: Session):
    return db.query(models.Table).all()

def create_table(db: Session , new_table : schemas.Add_table):
    db_table = models.Table(**new_table.dict())
    db.add(db_table)
    db.commit()
    db.refresh(db_table)
    return db_table



# !!!!!!!!!!!!!!!!!!!!!!! Table reservation system !!!!!!!!!!!!!!!!!!!!!!!!!!


def get_reservation(db: Session):
    return db.query(models.Reservation).all() 

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


def delete_reservation(db: Session, r_id : int ):
    reservation_remove = db.query(models.Reservation).filter(models.Reservation.id == r_id).first()
    db.delete(reservation_remove)
    db.commit()
    return {"Reservation Cancelled"} 


