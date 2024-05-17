
from fastapi import HTTPException
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session # Session es una sesión de bd que proporciona SQLAlchemy para realizar consultas.
from source.models.models import usuarios # Importa los modelos
from source.database import SessionLocal

# Configuración de JWT
SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Funciones para manejar la autenticación
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(contraseña):
    return pwd_context.hash(contraseña)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def authenticate_user(db: Session,usuario: str, contraseña: str):
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
