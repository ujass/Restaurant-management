from typing import Optional , List
from fastapi import Depends, FastAPI, HTTPException,  Query
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)


app = FastAPI()


# Dependency session 
# function will stop where it will se yield
# Finally will call after sending the data in response
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


"""
 Food APIs are below here:

"""


# Show all food of food menu
@app.get("/food_menu/", tags = ["Food Menu"] )
def get_food(db : Session = Depends(get_db)):
    return crud.get_food(db = db)


# Show food by selected category
@app.get("/food_menu_by_category/", tags=["Food Menu"])
def get_food_category(category: List[str] = Query(None) , db: Session = Depends(get_db)):
    result = []
    for each_category in category:
        db_category = crud.get_food_by_category(db = db , category = each_category )
        result = result + db_category
    return result


# Add new food item 
@app.post("/food_menu/", tags = ["Food Menu"])
def creat_food(new_food: schemas.Food_data , db: Session = Depends(get_db)):
    return crud.create_food(db = db , new_food = new_food)


# Update food details
@app.put("/food_menu/{food_id}/", tags = ["Food Menu"])
def update_food(food_id: int, food: schemas.Food_data, db: Session = Depends(get_db)):
    return crud.update_food(db = db, food = food, food_id = food_id)
    

# Delete food
@app.delete("/food_menu/{food_id}/", tags = ["Food Menu"])
def delete_food(food_id : int, db : Session = Depends(get_db)):
    return crud.delete_food(db = db, food_id = food_id)
    


"""
    Customer APIs are below here:
    
"""


# Show all Customers 
@app.get("/customer/", tags = ["Customer"])
def get_customer(db : Session = Depends(get_db)):
    return crud.get_customer(db = db)


# Add new Customer
@app.post("/customer/", tags = ["Customer"])
def creat_customer(new_customer : str, db : Session = Depends(get_db)):
    return crud.create_customer(db = db, new_customer = new_customer)


"""
    Food order APIs are below here:
    
"""


# Show all Orders
@app.get("/order/", tags = ["Order"])
def show_order(db : Session = Depends(get_db)):
    return crud.show_order(db = db)


# Create new Order
# q = quantity
@app.post("/order/", tags = ["Order"])
def creat_order(food_id: int, customer_id: int, q: Optional[int] = 1, db: Session = Depends(get_db)):
    return crud.create_order(db = db, customer_id = customer_id , food_id = food_id, q = q)


# Update Order status
@app.get("/order update/{order_id}", tags = ["Order"])
def order_update( order_id: int, update_status : schemas.Order_status, db : Session = Depends(get_db)):
    return crud.order_update(db = db, order_id = order_id, update_status = update_status)


# Delete Order
@app.delete("/order/", tags = ["Order"])
def delete_order(order_id : int, db : Session = Depends(get_db)):
    return crud.delete_order(db = db, order_id = order_id)


# Add feedback
@app.post("/order feedback/", tags = ["Order"])
def feedback_add(feedback_content : schemas.Feedback_data, db: Session = Depends(get_db)):
    return crud.feedback_add(db = db, feedback_content = feedback_content)


"""
    Bill APIs are below here:
    
"""


# Get bill
# If copon code is valid then apply it.
@app.get("/bill/{customer_id}/", tags = ["Bill"])
def fatch_bill(customer_id : int,  coupon_code : Optional[str] = None, db : Session = Depends(get_db)):
    final_bill = crud.fatch_bill(db = db, customer_id = customer_id)

    if coupon_code == "DIWALI10" : 
        final_bill = (final_bill) - (final_bill* 0.1)
        return final_bill

    return final_bill


"""
    Table APIs are below here:
    
"""


# Show all Tables
@app.get("/tables/", tags = ["Table"])
def get_table(db: Session = Depends(get_db)):
    return crud.get_table(db = db)


# Add new Table
@app.post("/tables/", tags = ["Table"])
def creat_table(new_table: schemas.Add_table, db : Session = Depends(get_db)):
    return crud.create_table(db = db, new_table = new_table)


"""
    Reservation APIs are below here:
    
"""


# Show Reservation
@app.get("/table reservation/",  tags=["Table Reservation"])
def get_reservation(db: Session = Depends(get_db)):
    return crud.get_reservation(db = db)


# Check available table
@app.post("/check_table/", tags = ["Table Reservation"])
def check_table(check_available : schemas.Check_reservation, person : int, db : Session = Depends(get_db)):
    return crud.check_table(db = db, check_available = check_available, person = person)


# Add Reservation
@app.post("/table reservation/", tags = ["Table Reservation"])
def create_reservation(reservation_data : schemas.Do_reservation, db : Session = Depends(get_db)):
    return crud.create_reservation(reservation_data = reservation_data, db = db)


# Delete Reservation 
# Add reservation if any customer is waiting for same table for same slot & date.
@app.delete("/table reservation/", tags = ["Table Reservation"])
def delete_reservation(r_id : int, db : Session = Depends(get_db)):
    return crud.delete_reservation(db = db, r_id = r_id)


"""
    Waiting APIs are below here:
    
"""

# Add Waiting if table is already reserved.
@app.post("/waiting/", tags = ["Waiting"])
def create_waiting(waiting_data : schemas.Do_reservation, db : Session = Depends(get_db)):
    return crud.create_waiting(waiting_data = waiting_data, db = db)
