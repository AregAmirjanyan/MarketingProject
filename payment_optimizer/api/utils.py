from fastapi import HTTPException, status, Depends
from payment_optimizer.db.sql_interactions import SqlHandler, logger
from fastapi.security import OAuth2PasswordBearer
from jose import  jwt, JWTError
from datetime import datetime, timedelta
from . import schemas
import bcrypt

"""
    This module contains utility functions used for user 
    authentication and authorization within the PayOpt API.
"""



# Secret key for JWT encoding and decoding
SECRET_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'
ALGO = 'HS256'
ACCESS_TOKEN__EXPIRE_MINUTES = 30 


# OAuth2 password bearer for token URL
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")



def create_access_token(data: dict):
    """
    Create an access token with the provided data.

    Args:
        data (dict): Data to encode in the token.

    Returns:
        str: Encoded JWT access token.
    """

    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes = ACCESS_TOKEN__EXPIRE_MINUTES)
    to_encode.update({'exp': expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGO)

    return encoded_jwt



def verify_access_token(token: str, credentials_exception):
    """
    Verify and decode the access token.

    Args:
        token (str): JWT access token.
        credentials_exception (HTTPException): Exception to raise if credentials are invalid.

    Returns:
        schemas.TokenData: Decoded token data.
    """

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGO])
        id = payload['user_id']

        if id is None:
            raise credentials_exception
        
        privilege = SqlHandler('e_commerce', 'user').get_table_data(['db_view'], f'user_id = {id}').loc[0, 'db_view']
        logger.warning(privilege)
        token_data = schemas.TokenData(id = id, privilege=privilege)
    except JWTError:
        raise credentials_exception

    return token_data



def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Get the current user based on the provided access token.

    Args:
        token (str, optional): JWT access token. Defaults to Depends(oauth2_scheme).

    Returns:
        schemas.TokenData: Current user's token data.
    """

    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail = 'Could not validate the credentials',
                                          headers = {'WWW-Authenticate': 'Bearer'})
    
    return  verify_access_token(token, credentials_exception)




def check_privilege(token: str = Depends(get_current_user)):
    """
    Check the privilege level of the current user.

    Args:
        token (str, optional): JWT access token. Defaults to Depends(get_current_user).

    Returns:
        str: Privilege level of the current user.
    """

    if token.privilege != 'granted':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Insufficient privileges')
    return token.privilege




def hash_password(password: str) -> str:
    """
    Hashes the provided password using bcrypt.

    Args:
        password (str): The password to be hashed.

    Returns:
        str: The hashed password.
    """
    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password.decode('utf-8')



def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verifies if the provided password matches the hashed password.

    Args:
        password (str): The password to be verified.
        hashed_password (str): The hashed password to compare against.

    Returns:
        bool: True if the password matches the hashed password, False otherwise.
    """
    # Encode the password as bytes
    encoded_password = password.encode('utf-8')

    # Verify the password
    return bcrypt.checkpw(encoded_password, hashed_password.encode('utf-8'))
