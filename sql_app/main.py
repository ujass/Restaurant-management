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
def get_food_category(category : List[str] = Query(None) , db: Session = Depends(get_db)):
    result = []
    for each_category in category:
        db_category = crud.get_food_by_category(db = db , category = each_category )
        result = result + db_category
    return result


# Add new food item 
@app.post("/food_menu/", tags = ["Food Menu"])
def creat_food(new_food : schemas.Food_data , db: Session = Depends(get_db)):
    return crud.create_food(db = db , new_food = new_food)


# Update food details
@app.put("/food_menu/{food_id}/", tags = ["Food Menu"])
def update_food(food_id : int, food : schemas.Food_data, db : Session = Depends(get_db)):
    db_food = crud.exist_food(db = db, food_id = food_id )
    if db_food:
        return crud.update_food(db = db, food = food, food_id = food_id)
    raise HTTPException(status_code=404, detail = "Food not found")


# Delete food
@app.delete("/food_menu/{food_id}/", tags = ["Food Menu"])
def delete_food(food_id : int, db : Session = Depends(get_db)):
    db_food = crud.exist_food(db = db, food_id = food_id)
    if db_food:
        return crud.delete_food(db = db, food_id = food_id)
    raise HTTPException(status_code=404, detail = "Food not found")


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
@app.post("/order/", tags = ["Order"])
def creat_order(food_id : int, customer_id : int, q : Optional[int] = 1, db : Session = Depends(get_db)):
    food_available = crud.food_available(db = db, food_id = food_id, q = q)
    validate_customer = crud.validate_customer(db = db, customer_id = customer_id)
    
    if food_available is None and validate_customer is None:
        raise HTTPException(status_code = 404, 
            detail="Sorry! Food and Customer both are registered")

    if food_available is None:
        raise HTTPException(status_code = 404,
            detail = "Sorry! Food is not available, Please order another food")

    if validate_customer is None:
        raise HTTPException(status_code = 404, 
            detail = "Sorry! Customer is not Registered, Please make your acoount.")

    return crud.create_order(db = db, customer_id = customer_id , food_id = food_id, q = q)


# Update Order status
@app.get("/order update/{order_id}", tags = ["Order"])
def order_update( order_id: int, update_status : schemas.Order_status, db : Session = Depends(get_db)):
    print(update_status)
    return crud.order_update(db = db, order_id = order_id, update_status = update_status)


# Delete Order
@app.delete("/order/", tags = ["Order"])
def delete_order(order_id : int, db : Session = Depends(get_db)):
    return crud.delete_order(db = db, order_id = order_id)


# Add feedback
@app.post("/order feedback/", tags = ["Order"])
def feedback_add(feedback_content : schemas.Feedback_data, db: Session = Depends(get_db)):
    validate_customer = crud.validate_customer(db = db, customer_id = feedback_content.customer_id)
    validate_order = crud.validate_order(db = db, order_id = feedback_content.order_id)
    
    if validate_customer is None and validate_order is None:
        raise HTTPException(status_code = 404, detail = "Wrong customer ID and Order ID. Please enter correct IDs.")
   
    if validate_customer is None:
        raise HTTPException(status_code = 404, detail = "Wrong customer ID. Please enter correct customer ID.")

    if validate_order is None:
        raise HTTPException(status_code = 404, detail = "Wrong order ID. Please enter correct order ID.")

    return crud.feedback_add(db = db, feedback_content = feedback_content)


"""
    Bill APIs are below here:
    
"""


# Get bill
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
def get_table(db : Session = Depends(get_db)):
    return crud.get_table(db = db)


# Add new Table
@app.post("/tables/", tags = ["Table"])
def creat_table(new_table : schemas.Add_table, db : Session = Depends(get_db)):
    return crud.create_table(db = db, new_table = new_table)



"""
    Table APIs are below here:
    
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
@app.delete("/table reservation/", tags = ["Table Reservation"])
def delete_reservation(r_id : int, db : Session = Depends(get_db)):
    return crud.delete_reservation(db = db, r_id = r_id)
