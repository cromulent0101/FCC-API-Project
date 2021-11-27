from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:12345@localhost/fastapi'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:   
        db.close() 

# while True:
#     try: 
#         conn = psychpg2.connect(host="localhost", database = "fastapi", user="postgres",
#                                 password="password123",cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         break
#     except Exception as error:
#         print("connectiong to db failed")
#         print("error: ",error)
#         time.sleep(10)