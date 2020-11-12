from datetime import date
from logging import exception
from sqlalchemy.orm import Session , join , outerjoin
import itertools
from sqlalchemy import and_
from fastapi import HTTPException


import models, schemas


"""
  Food operations

"""


# Check food exist or not
# If not, raise exception
def exist_food(db : Session, food_id : int):
    food_exist =  db.query(models.Food).filter(models.Food.food_id == food_id).first()
    if food_exist is None:
        raise HTTPException(status_code=404, detail = "Food not found")
    

# Check food is available in required quantity
# If not, raise exception
def food_available(db : Session, food_id : int,  q : int):
    available_food =  db.query(models.Food).filter(and_(
                        models.Food.food_id == food_id, 
                        models.Food.food_quantity >= q )).first()
    if available_food is None:
        raise HTTPException(status_code = 404,
            detail = "Sorry! Food is not available, Please order another food")

# Get all food
def get_food(db : Session):
    return db.query(models.Food).all()

# Get food by category
def get_food_by_category(db : Session, category : str):
    return db.query(models.Food).filter(models.Food.food_category == category).all()

# Add food
def create_food(db : Session, new_food : schemas.Food_data):
    db_food = models.Food(**new_food.dict())
    db.add(db_food)
    db.commit()
    db.refresh(db_food)
    return db_food

# Update food    
def update_food(db : Session, food : schemas.Food_data, food_id : int):
    exist_food(db = db, food_id = food_id )
    food_available = db.query(models.Food).filter(models.Food.food_id == food_id).first()
    food_available.food_name = food.food_name
    food_available.food_price = food.food_price
    food_available.food_category = food.food_category
    food_available.food_quantity = food.food_quantity

    db.commit()
    db.refresh(food_available)
    return food_available

# Delete food
def delete_food(db : Session, food_id : int):
    exist_food(db = db, food_id = food_id)
    food_remove = db.query(models.Food).filter(models.Food.food_id == food_id).first()
    db.delete(food_remove)
    db.commit()
    return {"Food removed"}


"""
    Customer operation

"""


# Check customer exist or not
# If not, raise exception
def validate_customer(db : Session, customer_id : int):
    customer_validate = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if customer_validate is None:
        raise HTTPException(status_code = 404, 
            detail = "Sorry! Customer is not Registered, Please make your acoount.")

# Get customers
def get_customer(db : Session):
    return db.query(models.Customer).all()

# Add customer
def create_customer(db : Session, new_customer : str):
    db_customer = models.Customer()
    db_customer.name = new_customer
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


"""
    Order operations

"""

# Check order exist or not 
# If not, raise exception
def validate_order(db : Session, order_id : int):
    order_validate =  db.query(models.Order).filter(models.Order.id == order_id).first()
    if order_validate is None :
        raise HTTPException(status_code=404, detail="Wrong Orderd ID")

# Get all orders
def show_order(db : Session):
    return db.query(models.Order).all()

# Create new order
# q = quantity
def create_order(db : Session, customer_id : int , food_id : int, q : int ):
    validate_customer(db = db, customer_id = customer_id)
    food_available(db = db, food_id = food_id, q = q)
    
    db_order = models.Order()
    db_order.customer_id = customer_id
    db_order.food_id = food_id
    db_order.status = "Order Created"
    db_order.quantity = q
    db.add(db_order)

    update_quantity = db.query(models.Food).filter(models.Food.food_id == food_id).first()
    update_quantity.food_quantity -= q

    db.commit()
    db.refresh(db_order)
    return db_order

# Update order
def order_update(db : Session, order_id : int, update_status : str ):
    validate_order(db = db, order_id = order_id)
    current_status = db.query(models.Order).filter(models.Order.id == order_id).first()
    
    if current_status.status == "Order Created" and update_status == "Order Processed":
        current_status.status = "Order Processed"
        db.commit()
        db.refresh(current_status)
        return current_status    

    if current_status.status == "Order Processed" and update_status == "Order Delivered":
        current_status.status = "Order Delivered"
        db.commit()
        db.refresh(current_status)
        return current_status

    return {"Can not update order"}
            
# Ddelete order
def delete_order(db : Session, order_id : int):
    validate_order(db = db, order_id = order_id)
    order_remove = db.query(models.Order).filter(models.Order.id == order_id).first()
    update_quantity = db.query(models.Food). filter(models.Food.food_id == order_remove.food_id).first()
    update_quantity.food_quantity += order_remove.quantity
    db.delete(order_remove)
    db.commit()
    return {"Order removed"}    

# Add feedback
def feedback_add(db : Session, feedback_content : schemas.Feedback_data):
    validate_customer(db = db, customer_id = feedback_content.customer_id)
    validate_order(db = db, order_id = feedback_content.order_id)

    add_content = models.Feedback(**feedback_content.dict())
    db.add(add_content)
    db.commit()
    db.refresh(add_content)
    return {"Feedback Added"}
    

"""
    Bill operation

"""


# Bill of total order
def fatch_bill(db : Session, customer_id : int):
    validate_customer(db = db, customer_id = customer_id)
    customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    all_orders = customer.orders
    total = 0
    for each_order in all_orders :
        order_quantity = each_order.quantity
        print(order_quantity)
        total += each_order.food.food_price * order_quantity
  
    return total


"""
    Table operations:

"""


# Check table exist or not
# If not, raise exception
def validate_table(db : Session, table_id: int):
    table_validate = db.query(models.Table).filter(models.Table.id == table_id).first()
    if table_validate is None:
        raise HTTPException(status_code = 404, detail = "Wrong table ID. Please enter correct table ID.")

# Get all tables
def get_table(db : Session):
    return db.query(models.Table).all()

# Add table
def create_table(db : Session, new_table : schemas.Add_table) :
    try:
        db_table = models.Table(**new_table.dict())
        db.add(db_table)
        db.commit()
        db.refresh(db_table)
        return db_table
    except:
        raise HTTPException(status_code = 400, detail = "Table with same name already exist.")


"""
    Reservation operations

"""

# Check reservation exist or not
# If not, raise exception
def validate_reservation(db : Session, reservation_id: int):
    reservation_validate = db.query(models.Reservation).filter(models.Reservation.id == reservation_id).first()
    if reservation_validate is None:
        raise HTTPException(status_code = 404, detail = "Wrong reservation ID. Please enter correct ID.")

# Get reservations
def get_reservation(db : Session):
    return db.query(models.Reservation).all() 

# Check table available or not on given date and slot for required people
def check_table(db : Session, check_available : schemas.Check_reservation, person : int):
    if check_available.slot not in [1,2,3,4]:
        raise HTTPException(status_code = 404, detail = "Wrong slot. Please enter correct slot.")

    available_tables = db.query(models.Table).outerjoin(models.Reservation, 
        and_(models.Table.id == models.Reservation.table_id, 
        models.Reservation.r_date == check_available.r_date,
        models.Reservation.slot == check_available.slot )).filter(models.Table.seat >= person, 
        models.Reservation.id == None).all()
    return available_tables

# Create reservation
def create_reservation(db : Session, reservation_data : schemas.Do_reservation) :
    validate_customer(db = db, customer_id = reservation_data.customer_id)
    validate_table(db = db, table_id = reservation_data.table_id)

    if (reservation_data.slot not in [1,2,3,4]) :
        raise HTTPException(status_code = 404, detail = "Wrong slot. Please enter correct slot.")

    add_rrservation = models.Reservation(**reservation_data.dict())
    db.add(add_rrservation)
    db.commit()
    db.refresh(add_rrservation)
    return {"Reservation done"}

    

# Delete reservation 
# Add new reservation if any customer with same requirement is waiting 
# If yes, then delete that customer from waiting table.
def delete_reservation(db : Session, r_id : int ):
    validate_reservation(db = db, reservation_id = r_id)
    reservation_remove = db.query(models.Reservation).filter(models.Reservation.id == r_id).first()
    db.delete(reservation_remove)
   
    waiting_exist = validate_waiting(db = db, waiting_data = reservation_remove)
    if waiting_exist is not None:
        add_reservation = models.Reservation()
        add_reservation.customer_id = waiting_exist.customer_id
        add_reservation.table_id = waiting_exist.table_id
        add_reservation.slot = waiting_exist.slot
        add_reservation.r_date = waiting_exist.r_date
        db.add(add_reservation) # Add into reservation table

        db.delete(waiting_exist) # Remove from waiting table
        db.commit()  
        db.refresh(add_reservation)
        return {"Reservation Cancelled"}

    db.commit()
    return {"Reservation Cancelled"} 


"""
    Waiting operation

"""


# Check customer waiting against deleting reservation
def validate_waiting(db : Session, waiting_data : schemas.Reservation):
    waiting_validate =  db.query(models.Waiting).filter(and_(
                models.Waiting.table_id == waiting_data.table_id,
                models.Waiting.slot == waiting_data.slot,
                models.Waiting.r_date == waiting_data.r_date)).first()
    if waiting_validate is None:
        return
    else:
        return waiting_validate


# Create waiting 
def create_waiting(db : Session, waiting_data : schemas.Waiting_data):
    validate_customer(db = db, customer_id = waiting_data.customer_id)
    validate_table(db = db, table_id = waiting_data.table_id)

    if (waiting_data.slot not in [1,2,3,4]) :
        raise HTTPException(status_code = 404, detail = "Wrong slot. Please enter correct slot.")

    add_waiting = models.Waiting(**waiting_data.dict())
    db.add(add_waiting)
    db.commit()
    db.refresh(add_waiting)
    return {"Waiting done"}
