from typing import List, Optional
from datetime import datetime
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# &&&&&&&&&&&&&&&&&&&&& food menu api &&&&&&&&&&&&
@app.post("/food_menu/" , tags=["Food Menu"])
def creat_food(new_food : schemas.Food , db: Session = Depends(get_db)):
    return crud.create_food(db = db , new_food = new_food)

@app.get("/food_menu/", tags=["Food Menu"] )
def get_food(db : Session = Depends(get_db)):
    print("main working")
    return crud.get_food(db = db)

@app.get("/food_menu/{category}/", tags=["Food Menu"])
def get_food_category(category : str , db: Session = Depends(get_db)):
    db_category = crud.get_food_by_category(db = db , category = category )
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category


@app.put("/food_menu/{food_id}/", tags=["Food Menu"])
def update_food(food_id : int , food : schemas.Food , db: Session = Depends(get_db)):
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


# @app.post("/users/", response_model=schemas.User)
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     db_user = crud.get_user_by_email(db, email=user.email)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     return crud.create_user(db=db, user=user)


# @app.get("/users/", response_model=List[schemas.User])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = crud.get_users(db, skip=skip, limit=limit)
#     return users


# @app.get("/users/{user_id}", response_model=schemas.User)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user


# @app.post("/users/{user_id}/items/", response_model=schemas.Item)
# def create_item_for_user(
#     user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_user_item(db=db, item=item, user_id=user_id)


# @app.get("/items/", response_model=List[schemas.Item])
# def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     items = crud.get_items(db, skip=skip, limit=limit)
#     return items


# &&&&&&&&&&&&&&&&&& customer create and get api &&&&&&&&&&&&

@app.post("/customer/", tags=["Customer"])
def creat_customer(new_customer : schemas.Customer , db: Session = Depends(get_db)):
    return crud.create_customer(db = db , new_customer = new_customer)

@app.get("/customer/", tags=["Customer"])
def get_customer(db : Session = Depends(get_db)):
    return crud.get_customer(db = db)

# ******************** order apis will show here *********************

@app.post("/order/", tags=["Order"])
def creat_order(food_id : int , customer_id : int, db: Session = Depends(get_db)):
    food_available = crud.food_available(db = db , food_id = food_id)
    if food_available > 0:
        return crud.create_order(db = db, customer_id = customer_id , food_id = food_id)
    raise HTTPException(status_code=404, detail="Sorry! Food is not available")


@app.delete("/order/", tags=["Order"])
def delete_order(order_id : int , db: Session = Depends(get_db)):
    return crud.delete_order(db= db , order_id = order_id)

@app.get("/order/", tags=["Order"])
def show_order(db: Session = Depends(get_db)):
    return crud.show_order(db= db)


#&&&&&&&&&&&&&&&&& Fatch bill &&&&&&&&&&&&&&&&&&&&

@app.get("/bill/{customer_id}/", tags=["Bill"])
def fatch_bill(customer_id : int,  q: Optional[str] = None , db: Session = Depends(get_db)):
    if q == "DIWALI10" : 
        final_bill = crud.fatch_bill(db = db, customer_id = customer_id)
        print(type(final_bill))
        final_bill = (final_bill) - (final_bill* 0.1)
        return final_bill

    return crud.fatch_bill(db = db, customer_id = customer_id)


#&&&&&&&&&&&&&&&&&&&&&&&&&&&& Table Reservation &&&&&&&&&&&&&&&&&&&

@app.post("/tables/", tags=["Table"])
def creat_table(new_table : schemas.Table , db: Session = Depends(get_db)):
    return crud.create_table(db = db , new_table = new_table)

@app.get("/tables/", tags=["Table"])
def get_table(db: Session = Depends(get_db)):
    return crud.get_table(db=db)


#!!!!!!!!!!!!!!!!!!!!! Table reservation !!!!!!!!!!!!!!!!!!!!!!!!!

@app.post("/check_table/", tags=["Table Reservation"])
def check_table(  check_available :  schemas.Check_reservation , person : int , db: Session = Depends(get_db)):
    return crud.check_table(db= db, check_available= check_available , person = person)


# @app.get("/table reservation/", tags=["Table Reservation"])
# def check_table(people : int , slot: str,  r_date : datetime ,db: Session = Depends(get_db)):
#     return crud.check_table(db= db , people = people ,slot = slot)

@app.post("/create_reservation/", tags=["Table Reservation"])
def create_reservation(reservation_data : schemas.Do_reservation, db: Session = Depends(get_db)):
    return crud.create_reservation(reservation_data = reservation_data , db = db)

@app.get("/get_reservation/",  tags=["Table Reservation"])
def get_reservation(db: Session = Depends(get_db)):
    return crud.get_reservation(db = db)