# pylint: skip-file
from fastapi import APIRouter,Depends,status,HTTPException,Response
from sqlalchemy.orm import Session
from passlib.exc import UnknownHashError
from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags=['Authentication'])

@router.post("/login")
def login(user_creds: schemas.UserLogin, db: Session = Depends(database.get_db)):

    user = db.query(models.User).filter(
        models.User.email==user_creds.email).first()
    print("this is the user", user)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Invalid Credentials')
    print("this is the user_creds password: ", user_creds.password)
    print("this is the user password: ", user.password)

    try:
        if not utils.verify(user_creds.password, user.password):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'Invalid Credentials')
    except UnknownHashError as e:
        return {"message": "you chose a user without a hashed password"}
        

    # create token
    access_token = oauth2.create_access_token(data = {"user_id": user.id})
    # return token

    return {"access_token": "blah"}