from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    is_active: bool = True

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool

    class Config:
        orm_mode = True