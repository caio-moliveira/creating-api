from sqlalchemy import Boolean, Column, Integer, String, Float
from sqlalchemy.orm import relationship

from src.schema.schema import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    area = Column(String)   
    job_description = Column(String)
    role = Column(Integer)
    salary = Column(Float)
    is_active = Column(Boolean, default=True)
    last_evaluation = Column(String)

    items = relationship("Item", back_populates="owner")