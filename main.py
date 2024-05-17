
from fastapi import FastAPI,Depends,HTTPException, Request
from source.services.schemas import usuarios, pedidos, detalle_pedidos, productos, pagos, facturacion
from source.services.crud import crear_usuario,obtener_usuario_por_id,actualizar_usuario,eliminar_usuario, crear_pedido, crear_detalle_pedido, crear_producto, crear_pago, crear_factura 
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from source.services.auth import authenticate_user, create_access_token,ACCESS_TOKEN_EXPIRE_MINUTES,ALGORITHM, get_user
from source import database
from source.routes import AuthRoutes# Importar la función desde el módulo
from typing import List
from source.database import db_mysql
from sqlalchemy.orm import Session
from source.database import SessionLocal


app = FastAPI()

# Función para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Ruta para probar la autenticación
@app.get("/test-auth")
def test_auth(db: Session = Depends(get_db)):
    username = "Liam"  # Nombre de usuario válido
    password = "5678"  # Contraseña válida
    try:
        authenticated_user = authenticate_user(db, username, password)
        return {"message": "Autenticación exitosa", "authenticated_user": authenticated_user}
    except HTTPException as e:
        return {"error": f"Error de autenticación: {e.detail}"}
    

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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Ruta para manejar las solicitudes de autenticación
@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.usuario, form_data.contraseña)
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


# Lógica de autenticación

@app.post("/login")
async def login(request: Request):
    form_data = await request.form()
    usuario = form_data.get("usuario")
    contraseña = form_data.get("contraseña")

    user = authenticate_user(usuario, contraseña)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


#Rutas


@app.post("/usuarios/", response_model=usuarios)
async def crear_usuario(user: usuarios):
    return crear_usuario(user)

@app.post("/productos/", response_model=productos)
async def crear_producto(prod:productos):
    return crear_producto(prod)

@app.post("/pedidos/", response_model=pedidos)
async def crear_pedido(ped:pedidos):
    return crear_pedido(ped)

#@app.post("/pagos/", response_model=pagos)
#async def crear_pago_api(pag:pagos):
 #   return crear_pago(pag)

