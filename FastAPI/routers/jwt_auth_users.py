from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone

ALGORITMO = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET = "529624250a24cc87f995b6548f518f070e22ec4430f34b1cb9aefd71542a6c7a"


router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])


class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool


class UserDB(User):
    password: str

users_db = {
    "mouredev": {
        "username": "mouredev",
        "full_name": "Brais Moure",
        "email": "braismoure@mouredev.com",
        "disabled": False,
        "password": "$2a$12$lfwuGDhBzZUZjQKKoDwYaeeL/CLeC2Hvjp37NBm1T7jHtndGuDPaO"
    },
    "mouredev2": {
        "username": "mouredev2",
        "full_name": "Brais Moure 2",
        "email": "braismoure2@mouredev.com",
        "disabled": True,
        "password": "$2a$12$QSBv1mQkZ40l9Ti71Bqzee0hb31AonhBOYzwu4jW7MX1Q4E.m0vYy"
    }
}


def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])
    
async def auth_user(token: str = Depends(oauth2)):
    
    credentials_exception = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="credenciales de autenticacion invalidas", 
                headers={"WWW-Authenticate": "Bearer"})

    try:
        username = jwt.decode(token, SECRET, algorithms=ALGORITMO).get("sub")
        if username is None:
            raise credentials_exception

    except InvalidTokenError:
        raise credentials_exception
    
    return search_user(username)


async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Ususario inactivo")
    
    return user

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")
    
    user = search_user_db(form.username)

    
    if not crypt.verify(form.password, user.password):
        raise HTTPException(
            status_code=400, detail="La contrasenya no es correcto")
    
    # Creamos el payload (contenido) para el token
    token_payload = {
        "sub": user.username, 
        "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_DURATION)
    }
    
    # Codificamos el token y lo devolvemos
    return {"access_token": jwt.encode(token_payload, SECRET, algorithm=ALGORITMO), "token_type": "bearer"}


@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user