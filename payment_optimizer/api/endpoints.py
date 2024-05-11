#################################### DENIED AND GRANTED VIEW ##########################################

from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import  OAuth2PasswordRequestForm
from typing import List
from fastapi.responses import HTMLResponse
from payment_optimizer.db.sql_interactions import SqlHandler, logger
from . import schemas
from typing import Optional
from . import utils as u
from . import granted_user_required
from . import auth_required


"""
     Shared endpoints for users granted and not grantedusers with special permission. 
     Permission is handled from user table db_view column
"""
 


app = FastAPI(title = 'PayOpt')

# root 
@app.get("/", response_class=HTMLResponse, tags=["Root"])
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
                    margin-right: 10px; /* Added margin to separate buttons */
                }
                .secondary-button:hover {
                    background-color: #0056b3;
                }
            </style>
            <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap" rel="stylesheet">
        </head>
        <body>
            <h1>Welcome to PayOpt API</h1>
            <a href="/docs" class="secondary-button">Swagger UI</a>
            <a href="/redoc" class="secondary-button">ReDoc</a> 
            <a href="
https://app.powerbi.com/reportEmbed?reportId=1733eb14-e25c-482e-8d8a-6f7172727743&autoAuth=true&ctid=4c0b7b5b-f6ee-4e4e-b961-0512d8fcb5f2" target="_blank" class="secondary-button">Report</a> 
        </body>
    </html>
    """




# POST endpoint for LogIn 
@app.post("/login", tags=['Default'])
def login(user_credentails: OAuth2PasswordRequestForm = Depends()):
    """
    Endpoint for user login. Validates user credentials and 
    returns an access token upon successful authentication.

    Args:
        user_credentials (OAuth2PasswordRequestForm): User's login credentials.

    Returns:
        dict: Access token and token type.
    """

    handler = SqlHandler('e_commerce', 'user')
    user = handler.select_row('email', user_credentails.username)

    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'Invalid email')
    
    logger.warn(user_credentails.password)
    logger.warn(user)
    logger.warn(user[0])
    logger.warn(type(user[0][1]))
    logger.warn(user[0][1])
    pass_in_db =  bytes(user[0][1], encoding='utf-8')
    if not u.verify_password(user_credentails.password, pass_in_db.decode('utf-8')):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'Invalid password')
    

    token = u.create_access_token({'user_id': user[0][0]})

    return {"access_token": token, "token_type": "bearer"}




# GET endpoint to search porducts
@app.get("/product/search", response_model=List[schemas.SearchProductOut], tags=['Default'])
def search_products(product_name: Optional[str] = None, 
                    brand: Optional[str] = None, 
                    price: Optional[float] = None):
    
    """
    Endpoint to search for products based on product name, brand, and price.

    Args:
        product_name (str, optional): Name of the product to search for.
        brand (str, optional): Brand of the product to search for.
        price (float, optional): Maximum price of the product to search for.

    Returns:
        List[schemas.SearchProductOut]: List of products matching the search criteria.
    """
     
    handler = SqlHandler('e_commerce', 'product')
    results = handler.search_products(product_name=product_name, 
                                      brand=brand, 
                                      price=price)
    return results










app.include_router(granted_user_required.router)
app.include_router(auth_required.router)