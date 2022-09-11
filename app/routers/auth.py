from fastapi import APIRouter, Depends, status, HTTPException, Response

from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from .. import database, schemas, models, utils, oauth2

router = APIRouter(
    tags=["Authentication"]
)

# User Login referencing the User Table for Email
# Use form-data in postman to input username & password
@router.post("/login")
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    query_user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    
    if not query_user:
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    # verify credential
    if not utils.verify(user_credentials.password, query_user.password):
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    # create token
    access_token = oauth2.create_access_token(data={"user_id": query_user.id})
    
    # return token
    return {"access_token": access_token, "token_type": "bearer"}
    