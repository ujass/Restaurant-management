from enum import unique
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean , DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Date

from database import Base


class Food(Base):
    __tablename__ = "foods"

    food_id = Column(Integer, primary_key = True, index = True)
    food_name = Column(String, unique = True , index = True)
    food_category  = Column(String)
    food_price = Column(Float)
    food_quantity = Column(Integer)

    orders = relationship("Order", backref= "food")

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key = True , index = True)
    name = Column(String, index = True)

    orders = relationship("Order", backref="customer")
    reservations = relationship("Reservation", backref="customer")  
    feedbacks = relationship("Feedback", backref="customer")  


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key = True,  index = True)
    food_id = Column(Integer , ForeignKey("foods.food_id"))
    customer_id = Column(Integer , ForeignKey("customers.id"))
    status = Column(String)
    # status_id = Column(Integer , ForeignKey("statuses.id"))
    feedbacks = relationship("Feedback", backref="order")  

class Table(Base):
    __tablename__ = "tables"

    id = Column(Integer, primary_key = True , index = True)
    name = Column(Integer, unique = True)
    seat = Column(Integer)
    reservations = relationship("Reservation", backref="table")   


class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key = True , index = True)
    customer_id = Column(Integer , ForeignKey("customers.id"))
    table_id = Column(Integer , ForeignKey("tables.id"))
    slot = Column(Integer)
    r_date = Column(Date)  # r_date represents Reservation date 

class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key = True , index = True)
    customer_id = Column(Integer , ForeignKey("customers.id"))
    order_id = Column(Integer , ForeignKey("orders.id"))
    rate = Column(Integer)
    comment = Column(String)  


# class Status(Base):
#     __tablename__ = "statuses"

#     id = Column(Integer, primary_key = True, index = True)
#     name = Column(String, unique = True)
#     orders = relationship("Order", backref="status")



# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)
#     email = Column(String, unique=True, index=True)
#     hashed_password = Column(String)
#     is_active = Column(Boolean, default=True)

#     items = relationship("Item", back_populates="owner")


# class Item(Base):
#     __tablename__ = "items"

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, index=True)
#     description = Column(String, index=True)
#     owner_id = Column(Integer, ForeignKey("users.id"))

#     owner = relationship("User", back_populates="items")