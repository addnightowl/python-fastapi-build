# JWT means "JSON Web Tokens".
# It's a standard to codify a JSON object in a long dense string without spaces. It looks like this:
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c

# We need to install python-jose to generate and verify the JWT tokens in Python:
# pip install "python-jose[cryptography]"

from fastapi import Depends, status, HTTPException

from sqlalchemy.orm import Session

from fastapi.security import OAuth2PasswordBearer

from jose import JWTError, jwt

from datetime import datetime, timedelta

from . import schemas, database, models

from .config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login") # tokenUrl is out login endpoint in auth.py --> "login"


# For JWT Token:
# This sensitive data needs to be store as environment variables
# SECRET KEY
SECRET_KEY = settings.secret_key
# ALGORITHM HS256
ALGORITHM = settings.algorithm
# EXPRIATION TIME FOR TOKEN
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict): # payload passed in is data of type dict
    to_encode = data.copy() # make a copy of the data to ensure that we are not changing anything

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    
    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        #validate token data
        token_data = schemas.TokenData(id=id)
        
    except JWTError:
        raise credentials_exception
    
    return token_data
    

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                          detail=f"Could not validate credentials.", headers={"WWW-Authenticate": "Bearer"})
    
    # make request to our database
    token = verify_access_token(token, credentials_exception)
    
    user = db.query(models.User).filter(models.User.id == token.id).first()
    
    return user