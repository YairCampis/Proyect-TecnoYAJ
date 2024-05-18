from fastapi import FastAPI, HTTPException, Response,Depends, APIRouter
from source.database import db_mysql
from sqlalchemy.orm import Session
from source.services.auth import create_access_token
from source.services.auth_validation import authenticate
from source.services.schemas import usuarios


router = APIRouter()

# Lógica de autenticación

@router.post("/login")
async def login(request: usuarios, db: Session = Depends(db_mysql.get_db)):
    _authentication = authenticate(db=db, user=request)

    if _authentication is not None:
        token = create_access_token(_authentication)
        return Response(
            code='Ok',
            status='200',
            message='Login exitoso',
            result={'access_token': token, 'token_type': 'bearer'}
        )
    
    raise HTTPException(
        status_code=401,
        detail='Credencial incorrecta',
    )