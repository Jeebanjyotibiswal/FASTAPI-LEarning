from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session

from datetime import datetime, timedelta, timezone


app = FastAPI()


# ================= DATABASE =================

DATABASE_URL = "sqlite:///./users.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# ================= JWT =================

secret_key = "jeebanjyoti"
Algorithm = "HS256"
Access_token_expire_minutes = 30


# ================= PASSWORD =================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(
        plain_password,
        hashed_password
    )


# ================= CREATE TOKEN =================

def create_token(data: dict):

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=Access_token_expire_minutes
    )

    data["exp"] = expire

    token = jwt.encode(
        data,
        secret_key,
        algorithm=Algorithm
    )

    return token


# ================= REGISTER =================

@app.post("/register")
def register(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    # Check user already exists
    existing_user = db.query(User).filter(
        User.username == form_data.username
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    # Hash password
    hashed_password = hash_password(
        form_data.password
    )

    # Create user
    new_user = User(
        username=form_data.username,
        hashed_password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully"
    }


# ================= LOGIN =================

@app.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    # Find user in database
    user = db.query(User).filter(
        User.username == form_data.username
    ).first()

    # Check username/password
    if not user or not verify_password(
        form_data.password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    # Create JWT
    access_token = create_token(
        data={"sub": user.username}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# ================= VERIFY TOKEN =================

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)


def verify_token(
    token: str = Depends(oauth2_scheme)
):

    try:

        payload = jwt.decode(
            token,
            secret_key,
            algorithms=[Algorithm]
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


# ================= PROTECTED ROUTE =================

@app.get("/protected")
def protected_route(
    username: str = Depends(verify_token)
):

    return {
        "message": f"Hello, {username}. You have access to this protected route."
    }     

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      