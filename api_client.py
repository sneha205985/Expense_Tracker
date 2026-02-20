"""
API Client for Expense Tracker
This module provides functions to interact with the FastAPI backend
"""
import requests
from typing import List, Dict, Optional
from datetime import date

# API base URL
API_BASE_URL = "http://localhost:8000/api"

# Global token storage
_token: Optional[str] = None


def set_auth_token(token: str):
    """Set the authentication token"""
    global _token
    _token = token


def get_headers() -> Dict[str, str]:
    """Get headers with authentication token"""
    headers = {"Content-Type": "application/json"}
    if _token:
        headers["Authorization"] = f"Bearer {_token}"
    return headers


def login(username: str, password: str) -> Dict:
    """Login and get access token"""
    response = requests.post(
        f"{API_BASE_URL}/auth/login",
        json={"username": username, "password": password}
    )
    response.raise_for_status()
    data = response.json()
    set_auth_token(data["access_token"])
    return data


def register(username: str, email: str, password: str) -> Dict:
    """Register a new user"""
    response = requests.post(
        f"{API_BASE_URL}/auth/register",
        json={"username": username, "email": email, "password": password}
    )
    response.raise_for_status()
    data = response.json()
    set_auth_token(data["access_token"])
    return data


def insert_expense(date_str: str, category: str, amount: float, notes: str = None):
    """Insert a new expense (backward compatible with old database.py)"""
    if not _token:
        raise Exception("Not authenticated. Please login first.")
    
    response = requests.post(
        f"{API_BASE_URL}/expenses",
        json={
            "date": date_str,
            "category": category,
            "amount": amount,
            "notes": notes
        },
        headers=get_headers()
    )
    response.raise_for_status()
    return response.json()


def get_all_expenses() -> List[tuple]:
    """Get all expenses (backward compatible - returns tuples like old database.py)"""
    if not _token:
        raise Exception("Not authenticated. Please login first.")
    
    response = requests.get(
        f"{API_BASE_URL}/expenses",
        headers=get_headers()
    )
    response.raise_for_status()
    expenses = response.json()
    # Convert to tuple format: (id, date, category, amount, notes)
    return [(e["id"], e["date"], e["category"], e["amount"], e.get("notes", "")) for e in expenses]


def delete_expense(expense_id: int):
    """Delete an expense by ID"""
    if not _token:
        raise Exception("Not authenticated. Please login first.")
    
    response = requests.delete(
        f"{API_BASE_URL}/expenses/{expense_id}",
        headers=get_headers()
    )
    response.raise_for_status()


def update_expense_by_id(expense_id: int, date_str: str, category: str, amount: float, notes: str = None):
    """Update an expense by ID"""
    if not _token:
        raise Exception("Not authenticated. Please login first.")
    
    response = requests.put(
        f"{API_BASE_URL}/expenses/{expense_id}",
        json={
            "date": date_str,
            "category": category,
            "amount": amount,
            "notes": notes
        },
        headers=get_headers()
    )
    response.raise_for_status()
    return response.json()


def init_db():
    """Dummy function for backward compatibility - database is initialized by FastAPI"""
    pass
