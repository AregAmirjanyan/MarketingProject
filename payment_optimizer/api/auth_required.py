############################################ DENIED VIEW ###################################################

from fastapi import  Depends, APIRouter
from payment_optimizer.db.sql_interactions import SqlHandler, logger
from . import schemas
from . import utils as u
from typing import Literal, Optional
from fastapi import  HTTPException
from fastapi import status as s
import random
from fastapi import Query





router = APIRouter(tags=['Authentication Required'])

@router.get("/mytransactions", response_model=list[schemas.MyTransactionsOut])
def get_user_transactions(current_user: schemas.TokenData = Depends(u.get_current_user)):
    mytransactions = []

    transactions = SqlHandler('e_commerce', 'transactions').get_transactions_by_user_id(current_user.id).to_dict(orient='records')
    logger.warning(transactions)
    for i in transactions:
        # payment 
        payment_method_name_data = SqlHandler('e_commerce', 'payment_method').get_table_data(['method_name'], f'payment_method_id = {i["payment_method_id"]}')
        payment_method_name = payment_method_name_data.iloc[0]['method_name'] if not payment_method_name_data.empty else None

        # rating 
        rating_description_data = SqlHandler('e_commerce', 'rating').get_table_data(['description'], f'rating_id = {i["rating_id"]}')
        rating_description = rating_description_data.iloc[0]['description'] if not rating_description_data.empty else None
        

        if not payment_method_name:
             payment_method_name= ''

      
        mytransactions.append(schemas.MyTransactionsOut(
            transaction_id=i['transaction_id'],
            payment_method_name=payment_method_name,
            rating_description=rating_description,
            status=i['status'],
            type=i['type'],
            shipping_address=i['shipping_address']
        ))

    return mytransactions




# PUT endpoint to update the user's  transaction
@router.put("/transactions/update", response_model=dict)
def create_transaction(transaction_id: int,
                            payment_method_name: Literal['Debit Card', 'PayPal', 'Cash', 'Credit Card'],
                            rating_description: Literal['bad', 'normal', 'good', 'perfect', 'terrible'], # corresponding rating name 
                            status: Literal['returned', 'purchased', 'canceled'],
                            type: Literal['pre-payment', 'post-payment'],
                            shipping_address: Optional[str] = None,
                            current_user: schemas.TokenData = Depends(u.get_current_user)
                            ):
        
        handler = SqlHandler('e_commerce', 'transactions')

        
        ts = handler.get_transactions_by_user_id(current_user.id).to_dict(orient='records')
        flag = False

        logger.warning(ts)

        if ts:
             for transaction in ts:
                  logger.warning(transaction)
                  if transaction['transaction_id'] == transaction_id:
                       flag = True
                       
                       
        if flag == False:
             raise HTTPException(status_code = s.HTTP_404_NOT_FOUND, detail = f'You do not own transaction {transaction_id}.')
        
                              

        if status == None:
             status = handler.get_table_data(['status'], f'transaction_id = {transaction_id}').loc[0, 'status']
             
        bandit = handler.get_table_data(['explored_bandit_type'], f'transaction_id = {transaction_id}').loc[0, 'explored_bandit_type']
        
        if not bandit:
             bandit = random.choice(['bandit A', 'bandit B'])

        payment_methods = ['Debit Card', 'PayPal', 'Cash', 'Credit Card']
        ratings = ['bad', 'normal', 'good', 'perfect', 'terrible']

        condition = f'transaction_id = {transaction_id}'
        values = {
                    'user_id' : current_user.id,
                    'payment_method_id' : payment_methods.index(payment_method_name),
                    'rating_id' : ratings.index(rating_description),
                    'status' : status,
                    'type' : type,
                    'shipping_address' : shipping_address,
                    'explored_bandit_type' : bandit


        }
        
        
        handler.update_table(condition, values)

    
        return {'message' : f'Transaction {transaction_id} updated successfully.'}



# POST endpoint to create a transaction
@router.post("/transactions/new", response_model = schemas.CreateTransactionOut)
def create_transaction(
                            payment_method_name: Literal['Debit Card', 'PayPal', 'Cash', 'Credit Card'],
                            rating_description: Literal['bad', 'normal', 'good', 'perfect', 'terrible'], # corresponding rating name 
                            status: Literal['returned', 'purchased', 'canceled'],
                            type: Literal['pre-payment', 'post-payment'],
                            shipping_address: Optional[str] = None,
                            current_user: schemas.TokenData = Depends(u.get_current_user),
                            ):
        
        handler = SqlHandler('e_commerce', 'transactions')

        
        bandit = random.choice(['bandit A', 'bandit B'])

        payment_methods = ['Debit Card', 'PayPal', 'Cash', 'Credit Card']
        ratings = ['bad', 'normal', 'good', 'perfect', 'terrible']

        tr = {
                    'user_id' : current_user.id,
                    'payment_method_id' : payment_methods.index(payment_method_name),
                    'rating_id' : ratings.index(rating_description),
                    'status' : status,
                    'type' : type,
                    'shipping_address' : shipping_address,
                    'explored_bandit_type' : bandit


        }

        handler.insert_one(tr)

        return schemas.CreateTransactionOut(payment_method_name=payment_method_name,
                                            rating_description=rating_description,
                                            status=status,
                                            type=type,
                                            shipping_address=shipping_address)







# create transactionm
# search for my transactions
