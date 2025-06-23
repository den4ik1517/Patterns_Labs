# app/models.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True)
    password = Column(String)

    apps = relationship("App", back_populates="owner")


class App(Base):
    __tablename__ = 'Apps'

    id = Column(Integer, primary_key=True, index=True)
    app_name = Column(String)
    user_id = Column(Integer, ForeignKey('Users.id'))

    owner = relationship("User", back_populates="apps")
