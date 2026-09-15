from fastapi import Depends, FastAPI,HTTPException, Header,Depends
from sqlalchemy.orm import Session, sessionmaker, declarative_base
from sqlalchemy import create_engine


DATABASE_URL = "sqlite:///./test.db"
app = FastAPI()

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

from model import Todos, User

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#################################  Curd Operation #########################
# Todos Create API
@app.post("/todos")
def todo_create(name: str, db: Session = Depends(get_db)):
    todo = Todos(name=name, completed="False")
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return {
        "message": "Todo Created",
        "data":todo
    }

# read all data API
@app.get("/todos")
def get_todos(db:Session=Depends(get_db)):
    todos=db.query(Todos).all()
    return{
        "Total":len(todos),
        "data":todos
    }

#read data by ID API
@app.get("/todos{todo_id}")
def get_todo(todo_id:int,db:Session=Depends(get_db)):
    todo=db.query(Todos).filter(Todos.id==todo_id).first()
    if not todo:
        raise HTTPException(
            status_code=404,
            detail="Todo Not Found"
        )
    return{
        "data":todo
    }

#update API
@app.put("/todos{todo_id}")
def update_todo(name:str,todo_id:int,db:Session=Depends(get_db)):
    todo=db.query(Todos).filter(Todos.id==todo_id).first()
    if not todo:
            raise HTTPException(
                status_code=404,
                detail="Todo Not Found"
            )
    todo.name=name
    db.commit()
    db.refresh(todo)
    return todo
# delete API
@app.delete("/todos{todo_id}")
def delete_todo(todo_id:int,db:Session=Depends(get_db)):
    todo=db.query(Todos).filter(Todos.id==todo_id).first()
    if not todo:
                raise HTTPException(
                    status_code=404,
                    detail="Todo Not Found"
                )
    db.delete(todo)
    db.commit()
    return {
         "message":"Todo Deleted Successfully"
    }

############################## Authentication ###############################
#create user data API
@app.post("/users")
def create_user(username:str,password:str,name:str,age:int,db:Session=Depends(get_db)):
    user=User(username=username,password=password,name=name,age=age)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {
        "message":"User Created Successfully",
        "data":user
    }
##### Login section ###############
SECRET_KEY="jeebanjyoti"
ALGORTHIM="HS256"
from datetime import datetime ,timezone,timedelta
from jose import jwt
def create_token(data:dict):
     expire=datetime.now(timezone.utc)+timedelta(minutes=30)
     data["exp"]=expire
     token=jwt.encode(data,SECRET_KEY,algorithm=ALGORTHIM)
     return token

@app.post("/login")
def login(username:str,password:str,db:Session=Depends(get_db)):
     user=db.query(User).filter(User.username==username,User.password==password).first()
     if not user:
        raise HTTPException(
            status_code=404,
            detail="Invalid Username or Password"
        )
     token=create_token({"sub":user.username})
     return {
        "message":"Login Successfully",
        "access_token":token
     }
def verify_token(token:str=Header(None)):
     try:
          payload=jwt.decode(token, SECRET_KEY, algorithms=[ALGORTHIM])
          return payload
     except:
              raise HTTPException(
                status_code=401,
                detail="Invalid Token"
            )
@app.get("/profile")
def profile(profile_data:dict=Depends(verify_token),db:Session=Depends(get_db)):
    
     return {
          
        "message":"Profile Retrieved Successfully",
        "data":profile_data
     }