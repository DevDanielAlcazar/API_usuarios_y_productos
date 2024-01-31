from pydantic import BaseModel

from fastapi import APIRouter, HTTPException

users = APIRouter(tags= ["Users"])


#entidad usuario
class User(BaseModel):
    id: int
    name: str
    username: str
    email: str
    age: int
    disabled: bool


#db de prueba de modelado
users_db = [User(id=1, name="Daniel", username="DevDaniel", email="procudhem@gmail.com", age=29, disabled=False),
            User(id=2, name="Angelica", username="DevAngelica", email="cointegram@gmail.com", age=30, disabled=False),
            User(id=3, name="Renata", username="DevRenata", email="renata@gmail.com", age=6, disabled=False),
            User(id=4, name="Isabel", username="DevIsabel", email="isabel@gmail.com", age=30, disabled=False)]


#Obtiene todos los usuarios en db
@users.get("/users")
async def general_users():
    return users_db



#Path /user/1 (parametros obligatorios (convencion))
@users.get("/user/{id}")
async def user_path(id: int):
    return search_user(id)


#Query /userquery?id=1 (parametros opcionales (convencion))
@users.get("/userquery")
async def user_query(id: int):
    return search_user(id)


#Buscar usuario por id
def search_user(id: int):
    user = filter(lambda user: user.id == id, users_db)
    try:
        return list(user)[0]
    except:
        return HTTPException(status_code=404, detail="No se encuentra el usuario") 
    

#Inserta valores
@users.post("/user/", response_model= User, status_code=201)
async def user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=409, detail="El usuario ya existe")
       
    #Se elimina el else pero funciona igual
    users_db.append(user)
    return user

#Actualiza datos
@users.put("/user/", status_code=200, response_model= User)
async def user(user: User):
    found = False

    for index, saved_user in enumerate(users_db):
        if saved_user.id == user.id:
            users_db[index] = user
            found = True
    if not found:
            raise HTTPException(status_code=404, detail= "No se ha encontrado al usuario")
    #Se elimina el else pero funciona igual
    return user

#Elimina datos
@users.delete("/user/{id}", status_code=200)
async def user(id: int):
    found = False

    for index, saved_user in enumerate(users_db):
        if saved_user.id == id:
            del users_db[index]
            found = True
    if not found:
            raise HTTPException(status_code=404,detail="No se ha eliminado al usuario")
    