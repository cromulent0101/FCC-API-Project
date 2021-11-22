from jose import JWTError, jwt 
from datetime import datetime, timedelta

#SECRET_KEY
#Algorithm
#Expiration Time

SECRET_KEY = 'FD0CCA14-D8A4-4B73-AE21-093C66D2D0AB'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30 

def create_access_token(data: dict):
    to_encode = data.copy()
    expire=datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)