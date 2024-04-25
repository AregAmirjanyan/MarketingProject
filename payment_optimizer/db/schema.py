from payment_optimizer.db.logger import CustomFormatter
import logging
import os



logger = logging.getLogger(os.path.basename(__file__))
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(CustomFormatter())
logger.addHandler(ch)


from sqlalchemy import create_engine,Column,Integer,String,Float, DATE, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

engine=create_engine('sqlite:///e_commerce.db')

Base= declarative_base()

class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True)
    password = Column (String)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String) 
    phone_number = Column(String)
    db_view = Column(String)
    
    
class Rating(Base):
    __tablename__ = "rating"

    rating_id = Column(Integer, primary_key=True)
    description = Column(String)


class PaymentMethod(Base):
    __tablename__ = "payment_method"

    payment_method_id = Column(Integer, primary_key=True)
    method_name = Column(String)


class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.user_id") )
    payment_method_id = Column(Integer, ForeignKey("payment_method.payment_method_id"))
    rating_id = Column(Integer, ForeignKey("rating.rating_id"))
    status = Column(String) ####????????
    type = Column(String)
    shipping_address = Column(String)
    explored_bandit_type = Column(String)

    r_user = relationship("User")
    r_paymentmethod = relationship("PaymentMethod")
    r_rating = relationship("Rating")

class Product(Base):
    __tablename__ = "product"

    product_id = Column(Integer, primary_key=True)
    product_name = Column(String)
    brand = Column(String)
    price = Column(Float)
    

class TransactionProduct(Base):
    __tablename__ = "transaction_product"

    transaction_id = Column(Integer, ForeignKey('transactions.transaction_id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('product.product_id'), primary_key=True)
    quantity = Column(Integer)
    date = Column(DATE)

    r_product = relationship("Product")
    r_transaction = relationship("Transaction")



class ABTestingResults(Base):
    tablename = "a_b_testing_results"

    result_id = Column(Integer, primary_key=True)
    start_date = Column(DATE)
    end_date = Column(DATE)
    t_test = Column(Float)
    p_value = Column(Float)
    message = Column(String)
    test_date = Column(DateTime, default=datetime.now)
    
"""     
if __name__ == "__main__":
    Base.metadata.create_all(engine) """

Base.metadata.create_all(engine)