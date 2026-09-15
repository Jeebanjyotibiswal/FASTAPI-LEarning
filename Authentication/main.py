from fastapi import FastAPI,HTTPException,Depends,Header
from jose import jwt
from datetime import datetime, time,timedelta, timezone

from regex import sub
app=FastAPI()
SECRET_KEY="jeeban"
ALGORTHIM="HS256"

# CREATE TOKEN
def create_token(data:dict):
    expire=datetime.now(timezone.utc)+timedelta(minutes=30)
    data["exp"]=expire
    token=jwt.encode(data,SECRET_KEY,algorithm=ALGORTHIM)
    return token

# LoginAPI
@app.post("/login")
def login(username:str,password:str):
    if username!="admin" or password !="1234":
        raise HTTPException(
            status_code=401,
            detail="Invalid User and Password"
        )
    token=create_token({"sub":username})
    return {
        "acc    ess_token":token
    }
def verify_token(token:str=Header(None)):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORTHIM])
        return payload
    except:
        raise HTTPException(
            status_code=401,
            detail="Invalid Token"
        )

#Protected Dashboad Route
@app.get("/dashboard")
def dashboard(user=Depends(verify_token)):
    return{
        "meassage":"dashboard is opened",
        "user":user
    }