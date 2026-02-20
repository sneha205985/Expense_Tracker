from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
import os
from dotenv import load_dotenv
from api.models import Base, Expense, User

# Load environment variables
load_dotenv()

# Get database URL from environment or default to SQLite
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    # PostgreSQL or other database
    engine = create_engine(DATABASE_URL)
else:
    # SQLite (default for Phase 1 & 2)
    engine = create_engine(
        "sqlite:///./expenses.db",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# CRUD functions using SQLAlchemy ORM
def create_expense(db: Session, expense_data: dict, user_id: int = None):
    """Create a new expense"""
    expense = Expense(**expense_data, user_id=user_id)
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense


def get_expense(db: Session, expense_id: int, user_id: int = None):
    """Get expense by ID"""
    query = db.query(Expense).filter(Expense.id == expense_id)
    if user_id:
        query = query.filter(Expense.user_id == user_id)
    return query.first()


def get_all_expenses(db: Session, user_id: int = None, skip: int = 0, limit: int = 100):
    """Get all expenses with optional pagination"""
    query = db.query(Expense)
    if user_id:
        query = query.filter(Expense.user_id == user_id)
    return query.order_by(Expense.date.desc()).offset(skip).limit(limit).all()


def update_expense(db: Session, expense_id: int, expense_data: dict, user_id: int = None):
    """Update an expense"""
    query = db.query(Expense).filter(Expense.id == expense_id)
    if user_id:
        query = query.filter(Expense.user_id == user_id)
    expense = query.first()
    if expense:
        for key, value in expense_data.items():
            if value is not None:
                setattr(expense, key, value)
        db.commit()
        db.refresh(expense)
    return expense


def delete_expense(db: Session, expense_id: int, user_id: int = None):
    """Delete an expense"""
    query = db.query(Expense).filter(Expense.id == expense_id)
    if user_id:
        query = query.filter(Expense.user_id == user_id)
    expense = query.first()
    if expense:
        db.delete(expense)
        db.commit()
    return expense


# User CRUD functions (Phase 4 - JWT)
def get_user_by_username(db: Session, username: str):
    """Get user by username"""
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str):
    """Get user by email"""
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, username: str, email: str, hashed_password: str):
    """Create a new user"""
    user = User(username=username, email=email, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
