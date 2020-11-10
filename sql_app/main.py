from typing import  Optional , List
from datetime import datetime
from fastapi import Depends, FastAPI, HTTPException ,  Query
from sqlalchemy.orm import Session
import schemas

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/items/")
def read_items(q: List[int] = Query(None)):
    return {"q": q}

# &&&&&&&&&&&&&&&&&&&&& food menu api &&&&&&&&&&&&
@app.get("/food_menu/", tags=["Food Menu"] )
def get_food(db : Session = Depends(get_db)):
    return crud.get_food(db = db)


# Food by category will take list of category from user and return with match category.
# It will send empty list if no result is found.
@app.get("/food_menu_by_category/", tags=["Food Menu"])
def get_food_category(category : List[str] = Query(None) , db: Session = Depends(get_db)):
    result = []
    for each_category in category:
        db_category = crud.get_food_by_category(db = db , category = each_category )
        result = result + db_category
    return result


@app.post("/food_menu/" , tags=["Food Menu"])
def creat_food(new_food : schemas.Food_data , db: Session = Depends(get_db)):
    return crud.create_food(db = db , new_food = new_food)


@app.put("/food_menu/{food_id}/", tags=["Food Menu"])
def update_food(food_id : int , food : schemas.Food_data , db: Session = Depends(get_db)):
    db_food = crud.exist_food(db = db , food_id = food_id )
    if db_food:
        return crud.update_food(db = db , food = food , food_id = food_id )
    raise HTTPException(status_code=404, detail="Food not found")

@app.delete("/food_menu/{food_id}/", tags=["Food Menu"])
def delete_food(food_id : int, db: Session =Depends(get_db)):
    db_food = crud.exist_food(db = db , food_id = food_id )
    if db_food:
        return crud.delete_food(db=db, food_id = food_id)
    raise HTTPException(status_code=404, detail="Food not found")







# &&&&&&&&&&&&&&&&&& customer create and get api &&&&&&&&&&&&

@app.get("/customer/", tags=["Customer"])
def get_customer(db : Session = Depends(get_db)):
    return crud.get_customer(db = db)


@app.post("/customer/", tags=["Customer"])
def creat_customer(new_customer : str , db: Session = Depends(get_db)):
    return crud.create_customer(db = db , new_customer = new_customer)


# ******************** order apis will show here *********************

@app.get("/order/", tags=["Order"])
def show_order(db: Session = Depends(get_db)):
    return crud.show_order(db= db)

# add one more parameter of book number of dish in single order
@app.post("/order/", tags=["Order"])
def creat_order(food_id : int , customer_id : int, db: Session = Depends(get_db)):
    exist_food = crud.exist_food(db= db , food_id = food_id)
    if exist_food is None :
        raise HTTPException(status_code=404, detail="Sorry! Food is not available, Please order another food")

    food_available = crud.food_available(db = db , food_id = food_id)
    if food_available is None:
        raise HTTPException(status_code=404, detail="Sorry! Food is not available, Please order another food")

    validate_customer = crud.validate_customer(db=db, customer_id = customer_id)
    if validate_customer is None:
        raise HTTPException(status_code=404, detail="Sorry! Customer is not Registered. Please, make your acoount.")

    return crud.create_order(db = db, customer_id = customer_id , food_id = food_id)


@app.get("/order update/{order_id}", tags=["Order"])
def order_update( order_id: int , update_status : str   ,db: Session = Depends(get_db)):
    return crud.order_update(db = db, order_id = order_id , update_status = update_status)


@app.post("/order feedback/",  tags=["Order"])
def feedback_add(feedback_content : schemas.Feedback_data , db: Session = Depends(get_db)):
    return crud.feedback_add(db= db , feedback_content = feedback_content)


@app.delete("/order/", tags=["Order"])
def delete_order(order_id : int , db: Session = Depends(get_db)):
    return crud.delete_order(db= db , order_id = order_id)








#&&&&&&&&&&&&&&&&& Fatch bill &&&&&&&&&&&&&&&&&&&&

@app.get("/bill/{customer_id}/", tags=["Bill"])
def fatch_bill(customer_id : int,  q: Optional[str] = None , db: Session = Depends(get_db)):
    final_bill = crud.fatch_bill(db = db, customer_id = customer_id)

    if q == "DIWALI10" : 
        final_bill = (final_bill) - (final_bill* 0.1)
        return final_bill

    return final_bill




#&&&&&&&&&&&&&&&&&&&&&&&&&&&& Table Details &&&&&&&&&&&&&&&&&&&

@app.get("/tables/", tags=["Table"])
def get_table(db: Session = Depends(get_db)):
    return crud.get_table(db=db)

@app.post("/tables/", tags=["Table"])
def creat_table(new_table : schemas.Add_table , db: Session = Depends(get_db)):
    return crud.create_table(db = db , new_table = new_table)



#!!!!!!!!!!!!!!!!!!!!! Table reservation !!!!!!!!!!!!!!!!!!!!!!!!!

@app.post("/check_table/", tags=["Table Reservation"])
def check_table(  check_available :  schemas.Check_reservation , person : int , db: Session = Depends(get_db)):
    return crud.check_table(db= db, check_available= check_available , person = person)


@app.delete("/table reservation/", tags=["Table Reservation"])
def check_table(r_id: int  ,db: Session = Depends(get_db)):
    return crud.delete_reservation(db= db , r_id = r_id )

@app.post("/create_reservation/", tags=["Table Reservation"])
def create_reservation(reservation_data : schemas.Do_reservation, db: Session = Depends(get_db)):
    return crud.create_reservation(reservation_data = reservation_data , db = db)

@app.get("/get_reservation/",  tags=["Table Reservation"])
def get_reservation(db: Session = Depends(get_db)):
    return crud.get_reservation(db = db)