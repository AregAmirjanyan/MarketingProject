from payment_optimizer.db.logger import CustomFormatter
import logging
import os
from sqlalchemy.exc import SQLAlchemyError
from pathlib import Path



# payment_optimizer/db/schema.py

from payment_optimizer.db.logger import CustomFormatter
import logging
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine,Column,Integer,String,Float, DATE, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship


def initialize_database(db_file_path):
    """
    Initializes the database.

    Args:
        db_file_path (str): The file path of the SQLite database.
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(CustomFormatter())
    logger.addHandler(ch)
    

    if not os.path.exists(db_file_path):   
        logger.warn(f"Database file does not exist, creating new database {db_file_path}")
        engine = create_engine(f'sqlite:///{db_file_path}')
        Base = declarative_base()
        
        try:
            class User(Base):
                """
                Represents the 'user' table in the database.
                """
                __tablename__ = "user"

                user_id = Column(Integer, primary_key=True)
                password = Column (String)
                first_name = Column(String)
                last_name = Column(String)
                email = Column(String) 
                phone_number = Column(String)
                db_view = Column(String)
                
                
            class Rating(Base):
                """
                Represents the 'rating' table in the database.
                """               
                
                __tablename__ = "rating"

                rating_id = Column(Integer, primary_key=True)
                description = Column(String)
                


            class PaymentMethod(Base):        
                """
                Represents the 'payment_method' table in the database.
                """        
                __tablename__ = "payment_method"

                payment_method_id = Column(Integer, primary_key=True)
                method_name = Column(String)


            class Transaction(Base):       
                """
                Represents the 'transactions' table in the database.
                """         
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
                """
                Represents the 'product' table in the database.
                """
                __tablename__ = "product"

                product_id = Column(Integer, primary_key=True)
                product_name = Column(String)
                brand = Column(String)
                price = Column(Float)
                

            class TransactionProduct(Base):
                """
                Represents the 'transaction_product' table in the database.
                """
                __tablename__ = "transaction_product"

                transaction_id = Column(Integer, ForeignKey('transactions.transaction_id'), primary_key=True)
                product_id = Column(Integer, ForeignKey('product.product_id'), primary_key=True)
                quantity = Column(Integer)
                date = Column(DATE)

                r_product = relationship("Product")
                r_transaction = relationship("Transaction")



            class ABTestingResults(Base): 
                """
                Represents the 'a_b_testing_results' table in the database.
                """
                __tablename__ = "a_b_testing_results" 
            
                result_id = Column(Integer, primary_key=True) 
                start_date = Column(DATE) 
                end_date = Column(DATE) 
                t_test_AB = Column(Float) 
                p_value_AB = Column(Float) 
                message_AB_comparison = Column(String) 
                t_test_BC = Column(Float) 
                p_value_BC = Column(Float)
                message_BC_comparison = Column(String) 
                test_date = Column(DATE)
            
            # Create a session
            Session = sessionmaker(bind=engine)
            session = Session()

            # Create all tables
            Base.metadata.create_all(engine)

            # Commit the changes
            session.commit()

            logger.warn("Database created successfully.")
            from payment_optimizer.db import basic_etl
            logger.warn("Database inserts were successful.")

        except SQLAlchemyError as e:
                logger.error(f"An error occurred: {e}")
    else:
            logger.warning("Database file already exists.")




# Get the current directory
current_dir = Path.cwd()

# Navigate up the directory tree until reaching "MarketingProject"
while current_dir.name != "MarketingProject" and current_dir.parent != current_dir:
    current_dir = current_dir.parent

# Check if "MarketingProject" is found
if current_dir.name == "MarketingProject":
    db_file_path = current_dir / "e_commerce.db"
    initialize_database(db_file_path)
else:
    print("Directory 'MarketingProject' not found in the directory tree.")

         
