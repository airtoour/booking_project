from sqlalchemy import Column, Integer, String

from app.database import Base

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email= Column(String, nullable=False)
    role = Column(String, nullable=True)
    hashed_password= Column(String, nullable=False)
