from pymongo.cursor import Cursor
from db.models.user import User

def user_schema(user) -> dict:
    return {
        "id": str(user["_id"]),
        "name": user["username"],  # Cambiado de "username" a "name" para coincidir con el modelo
        "email": user["email"],
        # Puedes mantener "disabled" si existe en tu modelo MongoDB o excluirlo si no está en el modelo Pydantic
        "disabled": user.get("disabled", False),
    }

from bson import json_util

def users_schema(users_cursor: Cursor) -> list[User]:
    user_list = [User(**json_util.loads(json_util.dumps(user))) for user in users_cursor]
    print(user_list)  # Agrega esta línea para imprimir la lista de usuarios
    return user_list



"""def users_schema(users_cursor: Cursor) -> list[User]:
    user_list = [User(**user) for user in users_cursor]
    return user_list"""
