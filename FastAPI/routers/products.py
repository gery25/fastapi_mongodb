from fastapi import APIRouter


router = APIRouter(prefix="/products", 
                    tags=["products"] ,
                    responses={404: {"message" : " No trobat"}}) # Si el anyadimos el prefix podemos substituir el /producs por / en los gets...
# /products pasa a ser el /

products_list = ["producto 1", "producto 2", "producto 3", "producto 4", "producto 5", "producto 6"]

@router.get("/")
async def products():
    return products_list

@router.get("/{id}")
async def products(id: int):
    return products_list[id]