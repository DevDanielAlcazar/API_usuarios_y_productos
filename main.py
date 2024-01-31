from typing import Union
import uvicorn

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import products, users, auth_basic_users, auth_jwt_users, users_db

app = FastAPI()

#Routers
app.include_router(products.router)
app.include_router(users.users)
app.include_router(auth_jwt_users.router)
app.include_router(auth_basic_users.router)
app.include_router(users_db.users)

app.mount("/statics", StaticFiles(directory="statics"), name="statics")
#Documentacion oficial de FastAPI https://fastapi.tiangolo.com/es/

@app.get("/")
async def read_root():
    return {"Desarrollado by": "Jesús Daniel Nava Alcazar"}

@app.get("/links")
async def root_url():
    return {"url_github": "https://github.com/DevDanielAlcazar"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

if __name__=="__main__":
    uvicorn.run("main:app", port=8000, reload=True)