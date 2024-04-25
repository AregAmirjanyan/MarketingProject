from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import  OAuth2PasswordRequestForm
from typing import List
from fastapi.responses import HTMLResponse
from payment_optimizer.db.sql_interactions import SqlHandler, logger
#from passlib.context import CryptContext
from . import schemas
from typing import Optional
from . import utils as u
from . import granted_user_required
from . import auth_required




app = FastAPI(title = 'PayOpt')



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
            <h1>Welcome to My API</h1>
            <a href="/docs" class="secondary-button">Swagger UI</a>
            <a href="/redoc" class="secondary-button">ReDoc</a> <!-- Added Redoc button -->
        </body>
    </html>
    """









@app.post("/login", tags=['Default'])
def login(user_credentails: OAuth2PasswordRequestForm = Depends()):
    handler = SqlHandler('e_commerce', 'user')
    user = handler.select_row('email', user_credentails.username)
    logger.warning(user)
    logger.warning(user_credentails)

    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'Invalid email')
    
    if not user_credentails.password == user[0][1]:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'Invalid password')
    

    token = u.create_access_token({'user_id': user[0][0]})

    return {"access_token": token, "token_type": "bearer"}




# GET endpoint to search porducts
@app.get("/product/search", response_model=List[schemas.SearchProductOut], tags=['Default'])
def search_products(product_name: Optional[str] = None, 
                    brand: Optional[str] = None, 
                    price: Optional[float] = None):
    
    handler = SqlHandler('e_commerce', 'product')
    results = handler.search_products(product_name=product_name, 
                                      brand=brand, 
                                      price=price)
    return results










app.include_router(granted_user_required.router)
app.include_router(auth_required.router)