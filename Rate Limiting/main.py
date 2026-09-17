from fastapi import FastAPI,Request
from sympy import limit
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
app=FastAPI()
#limit setup
limiter=Limiter(key_func=get_remote_address)
app.state.limiter=limiter
# Error handle
@app.exception_handler(RateLimitExceeded)
def rare_limit_handler(request:Request,exc:RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content="Limit Exceed"
    )

@app.get("/data")
@limiter.limit("10/minutes")
def get_data(request:Request):
    return{
        "message":"API is working"
    }

