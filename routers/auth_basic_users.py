from fastapi import APIRouter, Depends, HTTPException, status
import uvicorn
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")


class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str


users_db = {
    "daniel": {
        "username": "DanielDev",
        "full_name": "Jesus Daniel Nava",
        "email": "jdna@gmmail.com",
        "disabled": False,
        "password": "Renata17"
    },
    "martha": {
        "username": "MarthaDev",
        "full_name": "martha angelica martinez",
        "email": "pollita@gmmail.com",
        "disabled": False,
        "password": "Marmtz1"
    },
    "Renata": {
        "username": "RenataDev",
        "full_name": "Renata Nava Martinez",
        "email": "kelis@gmmail.com",
        "disabled": False,
        "password": "kikillo1"
    }
}


def search_user(username: str):
    if username in users_db:
        return UserDB(**users_db[username])


def search_user_not_db(username: str):
    if username in users_db:
        return User(**users_db[username])


async def current_user(token: str = Depends(oauth2)):
    user = search_user_not_db(token)
    if not user:
         raise  HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                               detail="Credenciales de autenticacion invalidas",
                                 headers={"www-Autenticate": "Bearer"})
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
    if not form.password == user.password:
        raise  HTTPException(status_code=400, detail="La contraseña no es correcta")
    return {"access_token": user.username, "token_type": "bearer"}

@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user

