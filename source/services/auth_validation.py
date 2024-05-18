from sqlalchemy.orm import Session

from source.services.schemas import usuarios
from source.services.crud import get_user


def authenticate(db: Session, user: usuarios):
    _user = get_user(db=db, usuarios=user.usuario)

    if _user is None:
        return None

    if _user.password == user.password:
        return _user