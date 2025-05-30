from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    accounts = relationship("Account", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(username={self.username})>"