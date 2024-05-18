from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from source.services import MyHTTPBearer
from source.services import get_db
from source.services import Response, internal_server_error
from source.services.schemas import usuarios
from source.services import crud

router = APIRouter()
bearer = MyHTTPBearer()


@router.get("/list", dependencies=[Depends(bearer)])
async def list_users(db: Session = Depends(get_db)):
    return Response(
        code='Ok',
        status='200',
        message='List of users',
        result=crud.list_users(db)
    )


@router.post("/create", dependencies=[Depends(bearer)])
async def create_user(request: usuarios, db: Session = Depends(get_db)):
    try:
        crud.create_user(db, user=request)
        print(request)

        return Response(
            code='Ok',
            status='200',
            message='User created successfully',
            result=request.dict()
        )
    except Exception as e:
        return internal_server_error(str(e))