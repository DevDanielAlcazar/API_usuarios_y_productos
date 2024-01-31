from pydantic import BaseModel

#entidad usuario
class User(BaseModel):
    id: str | None = None
    username: str
    email: str
    disabled: bool
