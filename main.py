
from fastapi import FastAPI,Depends,HTTPException,status
import uvicorn
from source import models
from source.services.schemas import usuarios
from source.services.crud import crear_usuario 
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from source.services.auth import authenticate_user, create_access_token,ACCESS_TOKEN_EXPIRE_MINUTES,ALGORITHM
from source.routes import AuthRoutes# Importar la función desde el módulo
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
    allow_origins=["*"], 
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


@app.get("/")
def index():
    return {
        "message": "Hola a todos, Bienvenidos!"
    }

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

@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
  user = await authenticate_user(form_data.username, form_data.password)
  if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
  access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
  )
  return {"access_token": access_token, "token_type": "bearer"}   


@app.post("/usuarios/", response_model=usuarios)
async def crear_usuario(user: usuarios,db:Session = Depends(get_db)):
    return crear_usuario(db,user)


# Ruta para obtener todos los usuarios de la base de datos
@app.get("/usuarios",response_model=list[dict]) #Esta anotacion especifica que la ruta devuelve una lista de diccionarios como respuesta.
async def listar_usuarios():
    all_users = db_mysql.get_all_users()  
    return all_users

# Endpoint para obtener un usuario por su nombre de usuario
@app.get("/users/")
async def get_user(username: str, db: Session = Depends(get_db)):
    # Realiza la consulta SQL para obtener el usuario por su nombre de usuario
    query = "SELECT * FROM usuario WHERE usuario = %s"
    result = db.execute(query, (username,))
    user = result.fetchone()

    # Verificar si el usuario existe
    if user is None:
        # Si el usuario no existe, levanta una excepción HTTP 404 (Not Found)
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    # Si el usuario existe, devolverlo
    return user

if __name__ == "__main__":
    uvicorn.run("main:app",
                host="localhost",
                reload=True)