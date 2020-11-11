from enum import unique
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean , DateTime
from sqlalchemy.orm import relationship, validates
from sqlalchemy.sql.sqltypes import Date

from database import Base


"""
    Food model

"""


class Food(Base):
    __tablename__ = "foods"

    food_id = Column(Integer, primary_key = True, index = True)
    food_name = Column(String, unique = True, index = True)
    food_category = Column(String)
    food_price = Column(Float)
    food_quantity = Column(Integer)

    orders = relationship("Order", backref= "food") 
    #we can access food's column by order like order.food.food_quantity


"""
    Customer model

"""


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key = True, index = True)
    name = Column(String, index = True)
    orders = relationship("Order", backref = "customer")
    reservations = relationship("Reservation", backref = "customer")  
    feedbacks = relationship("Feedback", backref = "customer")  


"""
    Order model

"""


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key = True,  index = True)
    food_id = Column(Integer, ForeignKey("foods.food_id"))
    customer_id = Column(Integer, ForeignKey("customers.id"))
    quantity = Column(Integer)
    status = Column(String)
    feedbacks = relationship("Feedback", backref="order")  


"""
    Table model

"""


class Table(Base):
    __tablename__ = "tables"

    id = Column(Integer, primary_key = True , index = True)
    name = Column(Integer, unique = True)
    seat = Column(Integer)
    reservations = relationship("Reservation", backref="table")   


"""
    Reservation model

"""


class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key = True, index = True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    table_id = Column(Integer, ForeignKey("tables.id"))
    slot = Column(Integer)
    r_date = Column(Date)  # r_date represents Reservation date 


"""
    Food model

"""


class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key = True, index = True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    order_id = Column(Integer, ForeignKey("orders.id"))
    rate = Column(Integer)
    comment = Column(String)  


 