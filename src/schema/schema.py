from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    name: str
    area: str
    job_description: str
    last_evaluation: str


class UserCreate(UserBase):
    password: str
    role: int
    salary: float


class User(UserBase):
    id: int
    is_active: bool


    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: int | None = None