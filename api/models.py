from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import date

Base = declarative_base()


class Expense(Base):
    """SQLAlchemy model for expenses table"""
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    category = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    notes = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # For Phase 4 (JWT)
    created_at = Column(DateTime, server_default=func.now())

    # Relationship (for Phase 4)
    user = relationship("User", back_populates="expenses")


class User(Base):
    """SQLAlchemy model for users table (Phase 4 - JWT)"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    # Relationship
    expenses = relationship("Expense", back_populates="user")
