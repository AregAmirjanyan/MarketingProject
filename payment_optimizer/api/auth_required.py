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


"""
     Endpoints specific to users who are not granted with special permission. 
     Permission is handled from user table db_view column
"""


router = APIRouter(tags=['Authentication Required'])




# GET endpoint to get the user's  transaction
@router.get("/mytransactions", response_model=list[schemas.MyTransactionsOut])
def get_user_transactions(current_user: schemas.TokenData = Depends(u.get_current_user)):
    """
    Retrieves the transactions associated with the current user.

    Args:
        current_user (schemas.TokenData, optional): The current authenticated user. Defaults to Depends(u.get_current_user).

    Returns:
        list[schemas.MyTransactionsOut]: A list of transactions associated with the current user.
    """

    
    mytransactions = []

    # Retrieve transactions associated with the current user
    transactions = SqlHandler('e_commerce', 'transactions').get_transactions_by_user_id(current_user.id).to_dict(orient='records')
    logger.warning(transactions)
    for i in transactions:
        # Retrieve payment method name 
        payment_method_name_data = SqlHandler('e_commerce', 'payment_method').get_table_data(['method_name'], f'payment_method_id = {i["payment_method_id"]}')
        payment_method_name = payment_method_name_data.iloc[0]['method_name'] if not payment_method_name_data.empty else None

        # Retrieve rating description 
        rating_description_data = SqlHandler('e_commerce', 'rating').get_table_data(['description'], f'rating_id = {i["rating_id"]}')
        rating_description = rating_description_data.iloc[0]['description'] if not rating_description_data.empty else None
        

        if not payment_method_name:
             payment_method_name= ''

        # Append transaction details to the list
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
@router.put("/mytransactions/update")
def update_transaction(transaction_id: int,
                            payment_method_name: Literal['Debit Card', 'PayPal', 'Cash', 'Credit Card'],
                            rating_description: Literal['bad', 'normal', 'good', 'perfect', 'terrible'], # corresponding rating name 
                            status: Literal['returned', 'purchased', 'canceled'],
                            type: Literal['pre-payment', 'post-payment'],
                            shipping_address: Optional[str] = None,
                            current_user: schemas.TokenData = Depends(u.get_current_user)
                            ):
          
     """
          Updates the details of a transaction associated with the current user.

          Args:
               transaction_id (int): The ID of the transaction to be updated.
               payment_method_name (Literal['Debit Card', 'PayPal', 'Cash', 'Credit Card']): The payment method name for the transaction.
               rating_description (Literal['bad', 'normal', 'good', 'perfect', 'terrible']): The rating description for the transaction.
               status (Literal['returned', 'purchased', 'canceled']): The status of the transaction.
               type (Literal['pre-payment', 'post-payment']): The type of transaction.
               shipping_address (str, optional): The shipping address for the transaction. Defaults to None.
               current_user (schemas.TokenData, optional): The current authenticated user. Defaults to Depends(u.get_current_user).

          Raises:
               HTTPException: If the user does not own the specified transaction.

          Returns:
               dict: A message indicating the success of the transaction update.
     """
     
     handler = SqlHandler('e_commerce', 'transactions')

     # Retrieve transactions associated with the current user
     ts = handler.get_transactions_by_user_id(current_user.id).to_dict(orient='records')
     

     # Check if the user owns the specified transaction
     flag = False
     if ts:
          for transaction in ts:
               logger.warning(transaction)
               if transaction['transaction_id'] == transaction_id:
                    flag = True
                    
                    
     if flag == False:
          raise HTTPException(status_code = s.HTTP_404_NOT_FOUND, detail = f'You do not own transaction {transaction_id}.')
     
                         
     # If status is not provided, retrieve the current status of the transaction
     if status == None:
          status = handler.get_table_data(['status'], f'transaction_id = {transaction_id}').loc[0, 'status']
          
     
     # Retrieve the current bandit type for the transaction
     bandit = handler.get_table_data(['explored_bandit_type'], f'transaction_id = {transaction_id}').loc[0, 'explored_bandit_type']
        
     # If bandit is not available, choose a random bandit type
     if not bandit:
          bandit = random.choice(['bandit A', 'bandit B', 'bandit C'])

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
     
     # Update the transaction details in the database
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
     
     """
     Creates a new transaction for the current user.

     Args:
          payment_method_name (Literal['Debit Card', 'PayPal', 'Cash', 'Credit Card']): The payment method name for the transaction.
          rating_description (Literal['bad', 'normal', 'good', 'perfect', 'terrible']): The rating description for the transaction.
          status (Literal['returned', 'purchased', 'canceled']): The status of the transaction.
          type (Literal['pre-payment', 'post-payment']): The type of transaction.
          shipping_address (str, optional): The shipping address for the transaction. Defaults to None.
          current_user (schemas.TokenData, optional): The current authenticated user. Defaults to Depends(u.get_current_user).

     Returns:
          schemas.CreateTransactionOut: Details of the newly created transaction.
     """

     handler = SqlHandler('e_commerce', 'transactions')

     # Choose a random bandit type
     bandit = random.choice(['bandit A', 'bandit B', 'bandit C'])

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
     
     # Insert the new transaction into the database
     handler.insert_one(tr)

     return schemas.CreateTransactionOut(payment_method_name=payment_method_name,
                                        rating_description=rating_description,
                                        status=status,
                                        type=type,
                                        shipping_address=shipping_address)
