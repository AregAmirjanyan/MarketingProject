############################################# GRANTED VIEW ###################################################

from fastapi import status, Depends, APIRouter
from payment_optimizer.db.sql_interactions import SqlHandler, logger
from . import schemas
from . import utils as u




router = APIRouter(tags = ['Granted User Access Required'])
tables = ['user', 'rating', 'payment_method', 'transactions', 'product', 'transaction_product']




# GET endpoint to retrieve n rows
def select_n_rows(table):

    @router.get(f"/{table}s",  response_model=dict)
    def select_n_rows(n: int, 
                      token : schemas.TokenData = Depends(u.get_current_user),
                      privilege = Depends(u.check_privilege)):
            
            #if token.privilege == 'granted':    
                instance = SqlHandler('e_commerce', table)
                data = instance.get_entries(n)
                return {'data': data.to_dict(orient="records")}
            # else to be implemented


# POST endpoint to create an entry
def create_entry(table:str, status_code = status.HTTP_201_CREATED):
    model_class = getattr(schemas, table)
    
    @router.post(f"/{table}/create", response_model=dict, status_code = status_code)
    def create_entry(new_entry: model_class,  
                     token : schemas.TokenData = Depends(u.get_current_user),
                     privilege = Depends(u.check_privilege)):

            #if token.privilege == 'granted':
                table_instance = SqlHandler('e_commerce', table)
                table_instance.insert_one(dict(new_entry))
                return {"data": "entry created successfully"} # raise to be implemented
            #else to be implemented        


# UPDATE endpoint to update a table
def update_table(table:str, status_code = status.HTTP_201_CREATED):
    model_class = getattr(schemas, table)

    @router.put(f"/{table}/update",  status_code = status_code)
    def update_table(condition_col:str, condition_val:str, 
                     new_values: model_class, 
                     token : schemas.TokenData = Depends(u.get_current_user),
                     privilege = Depends(u.check_privilege)):
            
            #if token.privilege == 'granted':
                condition = f'{condition_col} = {condition_val}'
                handler = SqlHandler('e_commerce', table)
                handler.update_table(condition, dict(new_values))
                return {"message": f"Table {table} updated successfully."}



for table in tables:
             select_n_rows(table)
             create_entry(table)
             update_table(table)



# outputs (data:..)
# login form
# add delte
# add more functionalities
# add results