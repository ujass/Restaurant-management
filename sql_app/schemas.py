# from sql_app.models import Waiting
from typing import List, Optional
from datetime import date, datetime
from pydantic import BaseModel
from sqlalchemy.sql.sqltypes import DateTime
from enum import Enum


"""
    Food schema

"""

class Food_data(BaseModel):
    food_name : str
    food_category : str
    food_price : float
    food_quantity : int


class Food(Food_data):
    food_id : int
   
    class Config:
        orm_mode = True


"""
    Customer schema

"""


class Customer_data(BaseModel):
    name: str
    ref_code: str


class Customer(BaseModel):
    id : int
    name : str
    own_code: str
    # balance: int

    class Config:
        orm_mode = True


"""
    Order schema

"""


class Order(BaseModel):
    id : int
    food_id : int 
    customer_id : int  
    status : Optional[str] = "Order Created"

    class Config:
        orm_mode = True


"""
    Reservation schema

"""


class Check_reservation(BaseModel):
    slot : int
    r_date : date  # r_date represents Reservation date 


class Do_reservation(Check_reservation):
    customer_id : int
    table_id : int


class Reservation(Check_reservation):
    id : int
    
    class Config:
        orm_mode = True


"""
    Table schema

"""


class Add_table(BaseModel):
    name : str
    seat : int


class Table(Add_table):
    id: int

    class Config:
        orm_mode = True


"""
    Feedback schema

"""


class Feedback_data(BaseModel):
    customer_id : int
    order_id : int
    rate : int
    comment : str 


class Feedback(Feedback_data):
    id : int

    class Config:
        orm_mode = True


"""
    Customer schema

"""

# this is not table, this is used to show list selection like dropdown list
class Order_status(str, Enum):
    order_processed = "Order Processed"
    order_delivered ="Order Delivered"


"""
    Waiting schema

"""

class Waiting_data(BaseModel):
    customer_id: int
    table_id: int
    slot: int
    r_date: date  # r_date represents Reservation date 


class Waiting(Waiting_data):
    id: int

    class Config:
        orm_mode = True