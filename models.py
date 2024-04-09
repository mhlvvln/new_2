from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, func, ForeignKey
from sqlalchemy.orm import relationship

from database.database import Base, engine


class User(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String)
    files = relationship("File", back_populates="owner", lazy="selectin")


class File(Base):
    __tablename__ = "files"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    original_name = Column(String, nullable=False)
    extension = Column(String, nullable=True)
    hash_name = Column(String, nullable=False, index=True)
    disabled = Column(Boolean, default=False)
    type = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    owner = relationship("User", back_populates="files")


#Base.metadata.create_all(bind=engine)