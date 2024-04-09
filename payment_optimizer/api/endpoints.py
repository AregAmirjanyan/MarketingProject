from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List
from fastapi.responses import HTMLResponse
from payment_optimizer.db.sql_interactions import SqlHandler
from typing import Optional, TypeVar, Type
from datetime import date
import logging


# using pydantic to extend BaseModel

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



tables = ['user', 'rating', 'payment_method', 'transactions', 'product', 'transaction_product']





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


# GET
def select_n_rows(table):

    @app.get(f"/{table}s",  response_model=dict)
    def select_n_rows(n: int):        
        instance = SqlHandler('e_commerce', table)
        data = instance.get_entries(n)
        return {'data': data.to_dict(orient="records")}




# POST
def create_entry(table:str):
    model_class = globals()[table]
    
    @app.post(f"/{table}s/create", response_model=dict)
    def create_entry(new_entry: model_class):

        table_instance = SqlHandler('e_commerce', table)
        table_instance.insert_one(dict(new_entry))
        return {"data": "user created successfully"} # raise to be implemented


# UPDATE

def update_table(table:str):
    model_class = globals()[table]

    @app.put(f"/{table}/update")
    def update_table(condition_col:str, condition_val:str, new_values: model_class):
        condition = f'{condition_col} = {condition_val}'

        handler = SqlHandler('e_commerce', table)
        handler.update_table(condition, dict(new_values))
        return {"message": f"Table {table} updated successfully."}



for table in tables:
    select_n_rows(table) 
    create_entry(table)
    update_table(table)


