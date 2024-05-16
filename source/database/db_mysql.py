from datetime import datetime, timedelta
import mysql.connector
from fastapi import FastAPI, Depends, HTTPException
from jose import JWTError, jwt
from passlib.context import CryptContext
from source.services.auth import SECRET_KEY, authenticate_user, create_access_token,ACCESS_TOKEN_EXPIRE_MINUTES,ALGORITHM
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import pymysql

#Conexion a la base de datos MySQL
def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host ="localhost",
            user ="root",
            passwd ="",
            database = "proyectoscul"
        )
        print ("Conexion exitosa a la base de datos")
        return connection
    except mysql.connector.Error as e:
        print (f"Error de conexion a la Base de Datos: {e}")
        raise

# Función para cerrar la conexión y el cursor
def close_connection(cursor, connection):
    cursor.close()
    connection.close()

# Contexto de hashing para las contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Función para verificar la contraseña
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Función para obtener todos los usuarios desde la base de datos
def get_all_users():
    connection = connect_to_db()
    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM usuarios"
        cursor.execute(query)
        users = cursor.fetchall()
        return users
    finally:
        close_connection(cursor, connection)


# Función para obtener los detalles del usuario desde la base de datos
def get_user(usuario: str):
    connection = connect_to_db()
    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM usuarios WHERE usuario = %s"
        cursor.execute(query, (usuario,))
        user = cursor.fetchone()
        return user
    finally:
        close_connection(cursor, connection)


# Función para verificar las credenciales del usuario en la base de datos MySQL
def credencial_user(usuario: str, contraseña: str):
    cursor = connect_to_db().cursor(dictionary=True)
    query = "SELECT * FROM usuarios WHERE usuario = %s"
    cursor.execute(query, (usuario,))
    user = cursor.fetchone()
    if not user:
        return False
    if not verify_password(contraseña, user["contraseña"]):
        return False
    return user

# Función para crear el token JWT
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

