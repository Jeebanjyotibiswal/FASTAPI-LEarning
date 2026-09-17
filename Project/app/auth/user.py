from jose import JWTError, jwt
from datetime import datetime, timedelta ,timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from app.config import setting
expiration_time=30
#token creation
def create_access_token(data: dict):
    expire=datetime.now(timezone.utc)+timedelta(minutes=expiration_time)
    data['exp']=expire
    token=jwt.encode(data,setting.secret_key,algorithm=setting.algorithm)
    return token

##hash password
def hash_password(password:str):
    pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")
    return pwd_context.hash(password)
#verify password
def verify_password(plain_password,hashed_password):
    pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")
    return pwd_context.verify(plain_password,hashed_password)

#verify token
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)


def verify_token(
    token: str = Depends(oauth2_scheme)
):

    try:

        payload = jwt.decode(
            token,
            setting.secret_key,
            algorithms=[setting.algorithm]
        )

        username = payload.get("sub")

        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

        return username

    except jwt.JWTError:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )