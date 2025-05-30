from sqlalchemy import Column, Integer, String, Boolean, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
import enum

# Define roles
class Role(str, enum.Enum):
    client = "client"
    ops = "ops"

# User table
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_verified = Column(Boolean, default=False)
    role = Column(Enum(Role), nullable=False)

    # One-to-many: one user uploads many files
    files = relationship("File", back_populates="uploader")

# File table
class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    path = Column(String, nullable=False)
    uploader_id = Column(Integer, ForeignKey("users.id"))

    # Relationship to user
    uploader = relationship("User", back_populates="files")
