# Response for HTTP status codes | Status for HTTP status codes dynamic approach | HTTPException for raising an HTTP Exception
# Body, Response, status, HTTPException, Depends <-- if needed
from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware


# using the APIRouter to reference our other code in different files --> our post and user code, etc.
from .routers import post, user, auth, vote

# from . import  models
# from .database import engine


# models.Base.metadata.create_all(bind=engine) # when using alembic we don't need this engine

app = FastAPI()

# cors middleware
# origins = ["https://www.google.com", "https://www.youtube.com"]
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # what domains/methods/headers can talk to our api
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# using the import from routers
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


# to start our server --> uvicorn app.main:app --reload
# in browser --> http://127.0.0.1:8000


# @decerator.http_method(PATH after specific domain name ex: http://127.0.0.1:8000--> is the PATH --> "/")
@app.get("/")
# function --> root --> contains all the logic to perform some type of task, as seen below with a return statement
def root():
    # returns data that's converted into JSON and returned to the user
    return {"message": "Hello World! Welcome to my API!!!!!!"}
