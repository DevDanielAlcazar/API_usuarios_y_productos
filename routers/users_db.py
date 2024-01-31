from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from db.models.user import User
from db.schemas.user import user_schema, users_schema
from db.client import db_client
from bson import ObjectId
from pymongo.errors import DuplicateKeyError


users = APIRouter(prefix="/userdb",tags= ["Usersdb"])





#Obtiene todos los usuarios en db
@users.get("/", response_model=list[User])
async def general_users():
    users_cursor = list(db_client.users_db_load.users.find())
    for user in users_cursor:
        print(user)
    return users_schema(users_cursor)






# Crear índice único en el campo "email" al iniciar la aplicación
db_client.local.users_db_load.users.create_index("email", unique=True)


# Crea User en db
@users.post("/", response_model=User, status_code=201)
async def create_user(user: User):
    # Validar los datos del usuario aquí antes de proceder
    if not user.username or not user.email:
        raise HTTPException(status_code=400, detail="Nombre de usuario y correo electrónico son obligatorios.")

    user_dict = user.dict(exclude={"id"})

    try:
        # Obtener la base de datos
        db = db_client.get_database()
        
        # Obtener la colección de usuarios
        users_collection = db.users

        # Asignar el ID al usuario en el diccionario antes de insertarlo en la base de datos
        user_dict["_id"] = ObjectId()

        # Insertar el usuario en la base de datos
        users_collection.insert_one(user_dict)
    except DuplicateKeyError:
        # Manejar el caso de correo electrónico duplicado
        raise HTTPException(status_code=400, detail="El correo electrónico ya está registrado.")
    except Exception as e:
        # Manejar otros errores de la base de datos
        return JSONResponse(status_code=500, content={"error": f"Error en la base de datos: {str(e)}"})

    return User(**user_dict)




# Actualiza datos
@users.put("/{user_id}", status_code=200, response_model=User)
async def update_user(user_id: str, updated_user: User):
    # Validar si el usuario existe
    existing_user = db_client.users_db_load.users.find_one({"_id": ObjectId(user_id)})

    if existing_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Excluir el campo 'id' si se proporciona
    updated_user_dict = updated_user.dict(exclude={"id"})

    # Actualizar los campos del usuario existente
    result = db_client.users_db_load.users.replace_one(
        {"_id": ObjectId(user_id)},
        updated_user_dict
    )

    if result.modified_count == 0:
        # Si no se realizan modificaciones, lanzar una excepción
        raise HTTPException(status_code=304, detail="No se realizó ninguna actualización")

    # Recuperar y devolver el usuario actualizado excluyendo '_id'
    updated_user_db = db_client.users_db_load.users.find_one({"_id": ObjectId(user_id)}, {"_id": 0})
    return User(**updated_user_db)




# Elimina datos
@users.delete("/{id}", status_code=200)
async def delete_user(id: str):
    # Verificar si el usuario existe
    existing_user = db_client.users_db_load.users.find_one({"_id": ObjectId(id)})

    if existing_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Eliminar el usuario
    result = db_client.users_db_load.users.delete_one({"_id": ObjectId(id)})

    if result.deleted_count == 0:
        # Si no se elimina ningún usuario, lanzar una excepción
        raise HTTPException(status_code=304, detail="No se eliminó ningún usuario")

    return {"message": "Usuario eliminado exitosamente"}