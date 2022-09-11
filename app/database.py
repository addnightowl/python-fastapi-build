# orm (sqlalchemy) --> instead of defining tables in postgres, we can define our tables as python models
# pip install sqlalchemy

# pip install psycopg2-binary && pip install psycopg for MAC Intel

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings

# sqlalchemy needs a connection to talk to postgres or any database, it needs psycopg but we have already installed it

# connection string --> SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db_name"
# This sensitive data needs to be store as environment variables
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

# engine --> responsible to connecting to our postgres database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

"""
Each instance of the SessionLocal class will be a database session. The class itself is not a database session yet.

But once we create an instance of the SessionLocal class, this instance will be the actual database session.

We name it SessionLocal to distinguish it from the Session we are importing from SQLAlchemy.

We will use Session (the one imported from SQLAlchemy) later.

To create the SessionLocal class, use the function sessionmaker:

"""
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# use this base class to extend all of our python models
Base = declarative_base()

# Dependency --> create a session for our request, then closes the session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        

"""
# reference for connecting to our database and running raw postgres sql | import psycopg # pip install "psycopg[binary]" | import time


while True:  
    try:
        # Connect to an existing database
        conn = psycopg.connect(host='localhost', port=5432, dbname='fastapi', user='postgres', password='0222190220')

        # Open a cursor to perform database operations
        cur = conn.cursor()
            
        # Execute a command: this creates a new table
        # cur.execute()
        
        print("Database connection was successful!")
        break
        
    except Exception as error:
        print("Connection to database failed!")
        print(f"Error is: {error}")
        time.sleep(3)
        
"""