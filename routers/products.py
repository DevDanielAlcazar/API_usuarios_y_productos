from fastapi import FastAPI, HTTPException

products = FastAPI()



@products.get("/products/")
async def products():