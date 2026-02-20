from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class ExpenseBase(BaseModel):
    date: date = Field(..., description="Expense date in YYYY-MM-DD format")
    category: str = Field(..., min_length=1, description="Expense category")
    amount: float = Field(..., gt=0, description="Expense amount (must be positive)")
    notes: Optional[str] = Field(None, description="Additional notes")


class ExpenseCreate(ExpenseBase):
    """Schema for creating a new expense"""
    pass


class ExpenseUpdate(BaseModel):
    """Schema for updating an existing expense"""
    date: Optional[date] = None
    category: Optional[str] = Field(None, min_length=1)
    amount: Optional[float] = Field(None, gt=0)
    notes: Optional[str] = None


class ExpenseResponse(ExpenseBase):
    """Schema for expense response"""
    id: int

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    """Schema for user registration"""
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., regex=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    """Schema for user login"""
    username: str
    password: str


class Token(BaseModel):
    """Schema for JWT token response"""
    access_token: str
    token_type: str = "bearer"
