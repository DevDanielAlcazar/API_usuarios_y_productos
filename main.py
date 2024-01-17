from typing import Union

from fastapi import FastAPI

app = FastAPI()

#Documentacion oficial de FastAPI https://fastapi.tiangolo.com/es/

@app.get("/")
async def read_root():
    return {"Saludo": "Hola FastApi"}

@app.get("/links")
async def root_url():
    return {"url_github": "https://github.com/DevDanielAlcazar"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}