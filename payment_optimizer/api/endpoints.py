from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.responses import HTMLResponse
from payment_optimizer.db.sql_interactions import SqlHandler
from typing import Optional, TypeVar
from datetime import date



# using pydamic to extend BaseModel

class user(BaseModel):
    user_id: int
    password: str
    first_name: str
    last_name:str
    email:str
    phone_number: Optional[str] = None


    
class rating(BaseModel):
    rating_id: int
    description: Optional[str] = None


class payment_method(BaseModel):
    payment_method_id: int
    method_name: str


class transactions(BaseModel):
    transaction_id: int
    user_id: int
    payment_method_id: int
    rating_id : int
    status: str
    type: Optional[str] = None
    shipping_address: Optional[str] = None
    

class product(BaseModel):
    product_id: int
    product_name: str
    brand: Optional[str] = None
    price: float
    
TDate = TypeVar('TDate', bound=date)
class transaction_product(BaseModel):
    transaction_id: int
    product_id: int
    quantity: Optional[int] = None ##??? AREG ???
    date: Optional[TDate] = None




app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <html>
        <head>
            <title>Welcome to My API</title>
            <style>
                body {
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                    font-family: 'Montserrat', sans-serif;
                    text-align: center;
                }
                h1 {
                    color: #007bff;
                    margin-bottom: 20px;
                }
                .secondary-button {
                    background-color: #007bff;
                    color: #fff;
                    padding: 10px 20px;
                    border: none;
                    border-radius: 5px;
                    text-decoration: none;
                    transition: background-color 0.3s ease;
                    margin-top: 20px;
                }
                .secondary-button:hover {
                    background-color: #0056b3;
                }
            </style>
            <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap" rel="stylesheet">
        </head>
        <body>
            <h1>Welcome to My API</h1>
            <a href="/docs" class="secondary-button">Swagger</a>
        </body>
    </html>
    """



tables = ['user', 'rating', 'payment_method', 'transactions', 'product', 'transaction_product'] 

def select_n_rows(table):

    @app.get(f"/{table}s")
    def select_n_rows(n:int):        
        instance = SqlHandler('e_commerce', table)
        data = instance.get_entries(n)
        return {'data': data.to_dict(orient="records")}



#error here
@app.post("/users")
def create_user(new_user: user):
    instance = SqlHandler('e_commerce', 'user')
    instance.insert_one(new_user)
    return {"data": "user created successfully"} # raise to be implemented

""" 
for table in tables:
    select_n_rows(table) """



