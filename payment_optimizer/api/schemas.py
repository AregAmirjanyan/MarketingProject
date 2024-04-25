from pydantic import BaseModel, Field
from typing import Optional, TypeVar, Type,  Literal
import random
from datetime import date



class user(BaseModel):
    #user_id: int
    password: str
    first_name: str
    last_name:str
    email:str
    phone_number: Optional[str] = None
    db_view: str = Field(default="denied")


    
class rating(BaseModel):
    #rating_id: int
    description: Optional[str] = None


class payment_method(BaseModel):
    #payment_method_id: int
    method_name: str

class transactions(BaseModel):
    #transaction_id: int
    user_id: int
    payment_method_id: int
    rating_id : int
    status: str
    type: Optional[str] = None
    shipping_address: Optional[str] = None
    explored_bandit_type: Literal['bandit A', 'bandit B'] 


    

class product(BaseModel):
    #product_id: int
    product_name: str
    brand: Optional[str] = None
    price: float
    
TDate = TypeVar('TDate', bound=date)
class transaction_product(BaseModel):
    #transaction_id: int
    product_id: int
    quantity: Optional[int] = None ##??? AREG ???
    date: Optional[TDate] = None




class UserLogIn(BaseModel):
    email:str
    password: str


class SearchProductOut(BaseModel):
    #product_id: int
    product_name: Optional[str] = None
    brand: Optional[str] = None
    price: Optional[float] = None

    class Config:
        from_attributes = True



class Token(BaseModel):
    access_token: str
    token_type: str 

class TokenData(BaseModel):
    id: int
    privilege: str


class MyTransactionsOut(BaseModel):
    transaction_id: int
    payment_method_name: str # corresponding payment method name
    rating_description: Optional[str] = None # corresponding rating name 
    status: str
    type: Optional[str] = None
    shipping_address: Optional[str] = None
    
    class Config:
        from_attributes = True


class CreateTransactionOut(BaseModel):
    #transaction_id: int
    payment_method_name: Literal['Debit Card', 'PayPal', 'Cash', 'Credit Card']
    rating_description: Optional[Literal['bad', 'normal', 'good', 'perfect', 'terrible']] # corresponding rating name 
    status: Optional[Literal['returned', 'purchased', 'canceled']]
    type: Literal['pre-payment', 'post-payment']
    shipping_address: Optional[str] = None

        
    class Config:
        from_attributes = True
