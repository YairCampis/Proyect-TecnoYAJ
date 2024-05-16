from fastapi import APIRouter, Depends, HTTPException
from main import get_user,SECRET_KEY,ALGORITHM,JWTError,jwt
#from main import oauth2_scheme
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


router = APIRouter()

# Ruta protegida que requiere token JWT
@router.get("/usuarios", tags=["users"])
async def read_users(token: str = Depends(oauth2_scheme)):
    # Decodificar el token y obtener el username
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Obtener los detalles del usuario desde la base de datos
    user = get_user(username)
    if user is None:
        raise credentials_exception
    return user
