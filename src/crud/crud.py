from sqlalchemy.exc import ArgumentError
from sqlalchemy.orm import Session

from src.models.user import User
from src.schema.schema import UserCreate, UserBase
from src.security.security import get_password_hash, verify_password


def get_user(
        db: Session,
        id: int | None = None, 
        name: str | None = None,
):
    if not any([name, id]):
        raise ValueError("You must specify a name or id")
    query = db.query(User)

    if id:
        query = query.filter(User.id == id)
    if name:
        query = query.filter(User.name == name)
    return query.first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate):
    db_user = User(
        name=user.name,
        area=user.area,
        job_description=user.job_description,
        last_evaluation=user.last_evaluation,
        role=user.role,
        salary=user.salary,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user: UserBase):
    db.query(User).filter(User.id == user.id).update(user.model_dump())
    db.commit()
    return db.query(User).filter(User.id == user.id).first()

def authenticate(db: Session, email: str, password: str):
    db_user = get_user(db=db, email=email)
    if not db_user or not verify_password(password, db_user.hashed_password):
        return None
    return db_user
