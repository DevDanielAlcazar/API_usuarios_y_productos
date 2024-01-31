from fastapi import APIRouter, Depends, HTTPException, status
import uvicorn
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta


ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 2
SECRET = "eIMT7B70vTA3AF95kMSuNOM5vOeRFabuk32pSqpfcTnCqGRrBuFMYb7TtRkulpmy"


router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])


class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str


users_db = {
    "DanielDev": {
        "username": "DanielDev",
        "full_name": "Jesus Daniel Nava",
        "email": "jdna@gmmail.com",
        "disabled": False,
        "password": "$2a$12$wvTp5hOYQcrUdS28i0K13elNYOFVku/PJEycV0nXheqVwKSVRgSXm" #Renata17
    },
    "MarthaDev": {
        "username": "MarthaDev",
        "full_name": "martha angelica martinez",
        "email": "pollita@gmmail.com",
        "disabled": False,
        "password": "$2a$12$Ls4a/D1l2SEqUDvLL55PdenT3G4bxOUpyaoy2cT9i/Ed.CAxDggEq" #Marmtz1
    },
    "RenataDev": {
        "username": "RenataDev",
        "full_name": "Renata Nava Martinez",
        "email": "kelis@gmmail.com",
        "disabled": False,
        "password": "$2a$12$r/jiSWCTMSZwXDcY0t99xuwZQu2uvM4noNkJHA9DYZvCcTd83QTwi" #kikillo1
    }
}




def search_user(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    
def search_user_not_db(username: str):
    if username in users_db:
        return User(**users_db[username])
    

exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                               detail="Credenciales de autenticacion invalidas",
                                 headers={"www-Autenticate": "Bearer"})


async def auth_user(token: str = Depends(oauth2)):
    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception
      
    except JWTError:
         raise exception
    
    return search_user_not_db(username)



async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Usuario inactivo")
    return user




@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise  HTTPException(status_code=400, detail="El usuario no existe")
    
    user = search_user(form.username)

    

    if not crypt.verify(form.password, user.password):
        raise  HTTPException(status_code=400, detail="La contraseña no es correcta")
    
        
    access_token = {"sub": user.username,
                    "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)}

    return {"access_token": jwt.encode(access_token,SECRET, algorithm=ALGORITHM), "token_type": "bearer"}


@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user



