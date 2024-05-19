
from fastapi import HTTPException,APIRouter,Depends,Request
from fastapi.security import HTTPAuthorizationCredentials,HTTPBearer
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from pydantic import BaseModel
from sqlalchemy.orm import Session # Session es una sesión de bd que proporciona SQLAlchemy para realizar consultas.
#from main import get_db
from source.models.models import usuarios # Importa los modelos
from source.database import SessionLocal
from dotenv import load_dotenv
import os

ACCESS_TOKEN_EXPIRE_MINUTES = 30 

# Configuración de JWT
load_dotenv
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token



def verify_token(token):
    isTokenValid: bool = False
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        session = SessionLocal()
        record = session.query(BaseModel).filter(BaseModel.usuario == payload['usuario']).first()

        if not record:
            isTokenValid = False
    except Exception as e:
        print(str(e))
        payload = None
    if payload:
        isTokenValid = True

    return isTokenValid

class MyHTTPBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(MyHTTPBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(MyHTTPBearer, self).__call__(request)

        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not verify_token(token=credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")


# Funciones para manejar la autenticación
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(contraseña):
    return pwd_context.hash(contraseña)

#Funcion de autenticacion de usuario
async def authenticate_user(db: Session,usuario: str, contraseña: str):
    print(f"Usuario recibido: {usuario}")  # Imprime el usuario recibido desde el formulario
    print(f"Contraseña recibida: {contraseña}")  # Imprime la contraseña recibida desde el formulario

    # Verificar credenciales en la base de datos
    user = get_user(db, usuario) # Llamada a la función get_user con la sesión de la base de datos
    print(f"Usuario de la base de datos: {user}")  # Imprime el usuario obtenido de la base de datos
    
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    if not verify_password(contraseña, user.contraseña): # Verificación de usuario y contraseña
         print("Contraseña incorrecta")
         raise HTTPException(status_code=401, detail="Contraseña incorrecta")
    print("Autenticación exitosa")  # Imprime si la autenticación fue exitosa
    return user

def get_user(db: Session, usuario: str):
    return db.query(usuarios).filter(usuarios.usuario == usuario).first()

