from pydantic import BaseModel, Field
from typing import Optional, TypeVar, Type,  Literal
import random
from datetime import date

"""
    This module defines Pydantic models representing various entities in the system.
"""

class user(BaseModel):
    """
    Represents a user in the system.
    """
    password: str
    first_name: str
    last_name:str
    email:str
    phone_number: Optional[str] = None
    db_view: str = Field(default="denied")


    
class rating(BaseModel):
    """
    Represents a rating for a transaction.
    """
    description: Optional[str] = None


class payment_method(BaseModel):
    """
    Represents a payment method.
    """
    method_name: str


class transactions(BaseModel):
    """
    Represents a transaction in the system.
    """
    user_id: int
    payment_method_id: int
    rating_id : int
    status: str
    type: Optional[str] = None
    shipping_address: Optional[str] = None
    explored_bandit_type: Literal['bandit A', 'bandit B', 'bandit C'] 
    

class product(BaseModel):
    """
    Represents a product.
    """   
    product_name: str
    brand: Optional[str] = None
    price: float
    

TDate = TypeVar('TDate', bound=date)
class transaction_product(BaseModel):
    """
    Represents a product associated with a transaction.
    """
    transaction_id: int
    product_id: int
    quantity: Optional[int] = None 
    date: Optional[TDate] = None

 

class UserLogIn(BaseModel):
    """
    Represents user login credentials.
    """
    email:str
    password: str


class SearchProductOut(BaseModel):
    """
    Represents the output of a product search.
    """    
    product_name: Optional[str] = None
    brand: Optional[str] = None
    price: Optional[float] = None

    class Config:
        from_attributes = True



class Token(BaseModel):
    """
    Represents an authentication token.
    """
    access_token: str
    token_type: str 

class TokenData(BaseModel):
    """
    Represents token data.
    """
    id: int
    privilege: str


class MyTransactionsOut(BaseModel):
    """
    Represents transaction details for the current user.
    """
    transaction_id: int
    payment_method_name: str # corresponding payment method name
    rating_description: Optional[str] = None # corresponding rating name 
    status: str
    type: Optional[str] = None
    shipping_address: Optional[str] = None
    
    class Config:
        from_attributes = True


class CreateTransactionOut(BaseModel):
    """
    Represents the output of creating a transaction.
    """
    payment_method_name: Literal['Debit Card', 'PayPal', 'Cash', 'Credit Card']
    rating_description: Optional[Literal['bad', 'normal', 'good', 'perfect', 'terrible']] # corresponding rating name 
    status: Optional[Literal['returned', 'purchased', 'canceled']]
    type: Literal['pre-payment', 'post-payment']
    shipping_address: Optional[str] = None

        
    class Config:
        from_attributes = True
