# pylint: skip-file
from fastapi import APIRouter,Depends,status,HTTPException,Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.exc import UnknownHashError
from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags=['Authentication'])

@router.post("/login", response_model=schemas.Token)
def login(user_creds: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    user = db.query(models.User).filter(
        models.User.email==user_creds.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Invalid Credentials')
    
    try:
        if not utils.verify(user_creds.password, user.password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail=f'Invalid Credentials')

    except UnknownHashError as e:
        return {"message": "you chose a user without a hashed password"}

    access_token = oauth2.create_access_token(data = {"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}