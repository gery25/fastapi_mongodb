from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

## uvicorn users:app --reload

router = APIRouter(tags=["user"])

# Entitat user
class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int

users_list = [User(id=1,name="Gerard",surname="safont",url="https://gerardmapes.com",age=20),
                User(id=2,name="brais",surname="moure",url="https://mouredev.dev",age=35),
                User(id=3,name="hola",surname="mundo",url="https://www.holamundo.com",age=40)]

@router.get("/usersjson")
async def usersjson():
    return [{"name": "Gerard" , "surname": "safont", "url":"https://gerardmapes.com", "age": 20},
            {"name": "brais" , "surname": "moure", "url": "https://mouredev.dev", "age": 35},
            {"name": "hola" , "surname": "mundo", "url": "https://www.holamundo.com", "age": 40}]


@router.get("/users")
async def users():
    return users_list

#path

@router.get("/users/{id}")
async def user(id: int):
    return search_user(id)
    

# Query

@router.get("/userquery/")
async def user(id: int):
    return search_user(id)


@router.post("/user/", response_model=User,status_code=201)
async def adduser(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=204, detail="L'usuari ja existeix")
        
    
    users_list.append(user)
    return user

@router.put("/user/", response_model= User)
async def modifyuser(user: User):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
    if not found:
        raise HTTPException(status_code=304, detail="l'ususri no sa actualitzat")


@router.delete("/user/{id}")
async def deleteuser(id : int):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True

    if not found:
        raise HTTPException(status_code=204, detail="l'usuari no s'ha eliminat")


def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error": "No se ha encontrado el usuario"}





