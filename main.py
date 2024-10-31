import time
from datetime import timedelta
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm

from src.crud import crud
from src.models import models
from src.schema import schemas
from src.security import security
from src.core.config import settings
from src.db.connection import engine
from src.deps.deps import CurrentUser, SessionDep
from src.schema.schema import Token, UserCreate

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/login/access-token/")
async def login(
    session: SessionDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:

    user = crud.authenticate(
        db=session, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    return Token(
        access_token=security.create_access_token(
            user.id, expires_delta=access_token_expires
        )
    )


@app.post("/singup", response_model=schemas.User)
async def create_user(session: SessionDep, user: UserCreate):
    db_user = crud.get_user(db=session, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=session, user=user)


@app.get("/users/me/", response_model=schemas.User)
async def read_users_me(current_user: CurrentUser, session: SessionDep):
    db_user = crud.get_user(db=session, user_id=current_user.id)
    return db_user

