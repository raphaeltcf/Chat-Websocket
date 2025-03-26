from sqlalchemy import Column, Integer, String, UUID
from database import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    credits = Column(Integer)
    