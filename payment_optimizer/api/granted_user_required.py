############################################# GRANTED VIEW ###################################################

from fastapi import status, Depends, APIRouter
from payment_optimizer.db.sql_interactions import SqlHandler, logger
from . import schemas
from . import utils as u
import os
from pathlib import Path
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse



"""
     Endpoints specific to users who are granted with special permission. 
     Permission is handled from user table db_view column
"""
 

router = APIRouter(tags = ['Granted User Access Required'])
tables = ['user', 'rating', 'payment_method', 'transactions', 'product', 'transaction_product']



# GET endpoint to retrieve n rows
def select_n_rows(table):
    """
    GET endpoint to retrieve n rows from the specified table.

    Args:
        table (str): Name of the table to retrieve data from.

    Returns:
        dict: Dictionary containing the retrieved data.
    """

    @router.get(f"/{table}s",  response_model=dict)
    def select_n_rows(n: int, 
                      token : schemas.TokenData = Depends(u.get_current_user),
                      privilege = Depends(u.check_privilege)):
            
                instance = SqlHandler('e_commerce', table)
                data = instance.get_entries(n)
                return {'data': data.to_dict(orient="records")}



# POST endpoint to create an entry
def create_entry(table:str, status_code = status.HTTP_201_CREATED):
    """
    POST endpoint to create an entry in the specified table.

    Args:
        table (str): Name of the table to create an entry in.
        status_code (int, optional): HTTP status code to return upon success. Defaults to status.HTTP_201_CREATED.

    Returns:
        dict: Dictionary indicating the success of the operation.
    """
    model_class = getattr(schemas, table)
    
    @router.post(f"/{table}/create", response_model=dict, status_code = status_code)
    def create_entry(new_entry: model_class,  
                     token : schemas.TokenData = Depends(u.get_current_user),
                     privilege = Depends(u.check_privilege)):

                table_instance = SqlHandler('e_commerce', table)
                table_instance.insert_one(dict(new_entry))
                return {"data": "Entry created successfully"} # raise to be implemented


# UPDATE endpoint to update a table
def update_table(table:str, status_code = status.HTTP_201_CREATED):
    """
    UPDATE endpoint to update a table.

    Args:
        table (str): Name of the table to update.
        status_code (int, optional): HTTP status code to return upon success. Defaults to status.HTTP_201_CREATED.

    Returns:
        dict: Dictionary indicating the success of the operation.
    """
    model_class = getattr(schemas, table)

    @router.put(f"/{table}/update",  status_code = status_code)
    def update_table(condition_col:str, condition_val:str, 
                     new_values: model_class, 
                     token : schemas.TokenData = Depends(u.get_current_user),
                     privilege = Depends(u.check_privilege)):
            
                condition = f'{condition_col} = {condition_val}'
                handler = SqlHandler('e_commerce', table)
                handler.update_table(condition, dict(new_values))
                return {"message": f"Table {table} updated successfully."}



for table in tables:
             select_n_rows(table)
             create_entry(table)
             update_table(table)
