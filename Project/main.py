from fastapi import FastAPI,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import engine,Base,get_db
from app.models.user import User
from app.auth.user import hash_password,verify_password,create_access_token
Base.metadata.create_all(bind=engine)
app=FastAPI()
from app.schemas.user import UserCreate 
##############################
@app.get("/")
def home():
    return {"message":"Hello World"}


@app.post("/register")
def register(
    user:UserCreate,
    
    db: Session = Depends(get_db),
):



    # Check user already exists
    existing_user = db.query(User).filter(
        User.name == user.name
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    # Hash password
    hashed_password = hash_password(
        user.password
    )

    # Create user
    new_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        is_active=True,
    )
    token = create_access_token(data={"sub": new_user.name})
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully",
        "access_token": token,
        "token_type": "bearer",
        "data": new_user
    }




@app.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    # Find user in database
    user = db.query(User).filter(
        User.name == form_data.username
    ).first()

    # Check username/password
    if not user or not verify_password(
        form_data.password,
        user.password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    # Create JWT
    access_token = create_access_token(
        data={"sub": user.name}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }



