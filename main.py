
from fastapi import FastAPI,Depends,HTTPException
from source.services.schemas import usuarios
from source.services.crud import crear_usuario 
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from source.services.auth import authenticate_user, create_access_token,ACCESS_TOKEN_EXPIRE_MINUTES,ALGORITHM
from source.routes import AuthRoutes# Importar la función desde el módulo
#from source import database

from typing import List
from source.database import db_mysql
from source.database.db_mysql import get_db
from sqlalchemy.orm import Session
from source.database import SessionLocal
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambia esto para restringir los orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Función para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Ruta para manejar las solicitudes de autenticación
@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["usuario"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# Ruta de prueba protegida que requiere token JWT
@app.get("/test")
async def test_protected_route(token: str = Depends(oauth2_scheme)):
    return {"message": "Hello, you have a valid token!"}


@app.post("/usuarios/", response_model=usuarios)
async def crear_usuario(user: usuarios,db:Session = Depends(get_db)):
    return crear_usuario(db,user)


# Ruta para obtener todos los usuarios de la base de datos
@app.get("/usuarios",response_model=list[dict]) #Esta anotacion especifica que la ruta devuelve una lista de diccionarios como respuesta.
async def listar_usuarios():
    all_users = db_mysql.get_all_users()  
    return all_users

# Ruta para obtener los detalles de 1 usuario de la base de datos
@app.get("/detalle_user")
async def get_user():
    detalles_user = get_user()  # Obtiene los detalles de 1 empleado de la base de datos
    return detalles_user