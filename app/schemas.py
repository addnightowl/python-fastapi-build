"""
Why We Need Schemas!

- It's a pain to get all the values from the body.
- The client can send whatever data they want.
- The data isn't getting validated.
- We ultimately want to force the client to send data in a schema that we expect.
"""

# Use pydantic to define what the schema should look like and provides validation.
# Can use with any python application not just with FastAPI
# from pydantic import BaseModel
# we want to tell the front-end what a post should look like or what is required --> create a class.

from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional

# schema --> pydantic model for user requests
class PostRequest(BaseModel):
    title: str
    content: str
    published: bool = True
    

# use inheritence to extend PostRequest as shown below:
class PostCreate(PostRequest):
   pass
    
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    # converts the sqlalchemy model --> pydantic model
    class Config:
        orm_mode = True

# schema --> pydantic model for user response
class PostResponse(PostRequest):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    
    # converts the sqlalchemy model --> pydantic model
    class Config:
        orm_mode = True
        
class PostOut(BaseModel):
    Post: PostResponse
    likes: int
    
    # converts the sqlalchemy model --> pydantic model
    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr # validates the email is a valid email and not some random text
    password: str
    
        
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[str] = None
    
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1) # try to find another way to do this so user cant use negative numbers