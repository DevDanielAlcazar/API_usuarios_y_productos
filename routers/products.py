from fastapi import APIRouter, HTTPException

router = APIRouter(prefix= "/products",tags= ["Products"], responses= {404: {"message": "Usuario no encontrado"}})
# inicia el server uvicorn users:users --reload 

products_list = ["producto 1", "producto 2", "producto 3"]


# Retorna todos los productos de la lista
@router.get("/")
async def get_all_products():
    """
    Obtiene todos los productos.
    """
    return products_list

# Busqueda por id
@router.get("/{product_id}")
async def get_product_by_id(product_id: int):
    """
    Obtiene un producto por su ID.
    """
    if 0 <= product_id < len(products_list):
        return products_list[product_id]
    else:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
