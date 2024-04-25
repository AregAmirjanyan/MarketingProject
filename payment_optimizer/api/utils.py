from fastapi import HTTPException, status, Depends
from payment_optimizer.db.sql_interactions import SqlHandler, logger
from fastapi.security import OAuth2PasswordBearer
#from . import endpoints as e
#from . import app
from jose import  jwt, JWTError
from datetime import datetime, timedelta
from . import schemas


SECRET_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'
ALGO = 'HS256'
ACCESS_TOKEN__EXPIRE_MINUTES = 30 



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")



def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes = ACCESS_TOKEN__EXPIRE_MINUTES)
    to_encode.update({'exp': expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGO)

    return encoded_jwt



def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGO])
        id: str = payload['user_id']

        if id is None:
            raise credentials_exception
        
        privilege = SqlHandler('e_commerce', 'user').get_table_data(['db_view'], f'user_id = {id}').loc[0, 'db_view']
        logger.warning(privilege)
        token_data = schemas.TokenData(id = id, privilege=privilege)
    except JWTError:
        raise credentials_exception

    return token_data

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail = 'Could not validate the credentials',
                                          headers = {'WWW-Authenticate': 'Bearer'})
    
    return  verify_access_token(token, credentials_exception)


def check_privilege(token: str = Depends(get_current_user)):
    if token.privilege != 'granted':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Insufficient privileges')
    return token.privilege