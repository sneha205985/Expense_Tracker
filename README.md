# Expense Tracker

A full-stack expense tracking application with a **FastAPI REST backend** and **Tkinter GUI frontend**. Features JWT authentication, SQLAlchemy ORM, PostgreSQL support, and comprehensive REST APIs.

## Features

### Backend (FastAPI)
- **REST API** with FastAPI framework
- **JWT Authentication** - Secure user authentication and authorization
- **SQLAlchemy ORM** - Database abstraction layer
- **PostgreSQL Support** - Production-ready database (SQLite for development)
- **Pydantic Validation** - Request/response validation
- **Swagger Documentation** - Interactive API docs at `/docs`
- **CRUD Operations** - Complete REST endpoints for expenses

### Frontend (Tkinter GUI)
- **Desktop Application** - User-friendly GUI
- **API Integration** - Consumes REST APIs
- **Expense Management** - Add, edit, delete expenses
- **Visualization** - Pie chart for category-wise expense distribution
- **Real-time Updates** - Auto-refresh expense list and totals

## Project Structure

```
ExpenseTracker/
│
├── api/                    # FastAPI backend
│   ├── __init__.py
│   ├── app.py             # FastAPI application entry point
│   ├── routes.py           # API endpoints
│   ├── schemas.py          # Pydantic models
│   ├── models.py           # SQLAlchemy models
│   ├── database.py         # Database configuration & CRUD
│   └── auth.py             # JWT authentication
│
├── main.py                 # Tkinter GUI application
├── api_client.py           # API client for GUI
├── visualizer.py           # Pie chart visualization
├── utils.py                # Utility functions
│
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## Prerequisites

- Python 3.8+
- PostgreSQL (optional, SQLite works for development)
- pip (Python package manager)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/sneha205985/Expense_Tracker.git
   cd Expense_Tracker
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables** (optional)
   ```bash
   cp .env.example .env
   # Edit .env and add your database URL and secret key
   ```

## 🗄️ Database Setup

### Option 1: SQLite (Default - No setup required)
The application uses SQLite by default. No additional configuration needed.

### Option 2: PostgreSQL (Production)
1. Install PostgreSQL and create a database:
   ```sql
   CREATE DATABASE expense_db;
   ```

2. Update `.env` file:
   ```env
   DATABASE_URL=postgresql+psycopg2://username:password@localhost:5432/expense_db
   SECRET_KEY=your-secret-key-here
   ```

3. The database tables will be created automatically on first run.

## Running the Application

### Start the API Server

```bash
# Using uvicorn directly
uvicorn api.app:app --reload

# Or run the app.py file
python api/app.py

# Or use the run script
python run_api.py
```

The API will be available at:
- **API Base URL**: `http://localhost:8000`
- **Swagger Docs**: `http://localhost:8000/docs`
- **ReDoc Docs**: `http://localhost:8000/redoc`

### Start the GUI Application

In a separate terminal:

```bash
python main.py
```

**Note**: The GUI requires the API server to be running. You'll be prompted to login/register when you start the GUI.

## 📡 API Endpoints

### Authentication

#### Register User
```http
POST /api/auth/register
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "username": "john_doe",
  "password": "password123"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

### Expenses (Requires Authentication)

All expense endpoints require a Bearer token in the Authorization header:
```http
Authorization: Bearer <your-access-token>
```

#### Create Expense
```http
POST /api/expenses
Authorization: Bearer <token>
Content-Type: application/json

{
  "date": "2026-02-20",
  "category": "Food",
  "amount": 150.50,
  "notes": "Lunch at restaurant"
}
```

#### Get All Expenses
```http
GET /api/expenses?skip=0&limit=100
Authorization: Bearer <token>
```

#### Get Expense by ID
```http
GET /api/expenses/{expense_id}
Authorization: Bearer <token>
```

#### Update Expense
```http
PUT /api/expenses/{expense_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "amount": 200.00,
  "notes": "Updated notes"
}
```

#### Delete Expense
```http
DELETE /api/expenses/{expense_id}
Authorization: Bearer <token>
```

## Testing the API

### Using Swagger UI
1. Start the API server
2. Open `http://localhost:8000/docs` in your browser
3. Click "Authorize" and enter your token
4. Test endpoints directly from the browser

### Using Postman/curl

**Example: Create Expense**
```bash
curl -X POST "http://localhost:8000/api/expenses" \
  -H "Authorization: Bearer <your-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "date": "2026-02-20",
    "category": "Food",
    "amount": 150.50,
    "notes": "Lunch"
  }'
```

**Example: Get All Expenses**
```bash
curl -X GET "http://localhost:8000/api/expenses" \
  -H "Authorization: Bearer <your-token>"
```

See `TESTING.md` for comprehensive testing guide and `POSTMAN_COLLECTION.json` for Postman collection.

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern, fast web framework for building APIs
- **SQLAlchemy** - SQL toolkit and ORM
- **Pydantic** - Data validation using Python type annotations
- **JWT** - JSON Web Tokens for authentication
- **PostgreSQL/SQLite** - Database

### Frontend
- **Tkinter** - Python GUI framework
- **Matplotlib** - Data visualization
- **Requests** - HTTP library for API calls

## 📝 Key Features Implementation

### Phase 1: FastAPI REST API 
- Created REST endpoints for all CRUD operations
- Implemented Pydantic models for request/response validation
- Added Swagger documentation

### Phase 2: SQLAlchemy ORM 
- Replaced raw SQLite queries with SQLAlchemy ORM
- Created database models and CRUD functions
- Maintained backward compatibility

### Phase 3: PostgreSQL Support 
- Added environment variable configuration
- Support for both SQLite and PostgreSQL
- Database URL configuration via `.env`

### Phase 4: JWT Authentication 
- User registration and login endpoints
- JWT token generation and validation
- Protected expense endpoints
- User-specific expense isolation

## Security Features

- **JWT Authentication** - Secure token-based authentication
- **Password Hashing** - Bcrypt password hashing
- **User Isolation** - Users can only access their own expenses
- **Input Validation** - Pydantic models validate all inputs
- **CORS Support** - Configurable CORS middleware

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username VARCHAR UNIQUE NOT NULL,
    email VARCHAR UNIQUE NOT NULL,
    hashed_password VARCHAR NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Expenses Table
```sql
CREATE TABLE expenses (
    id INTEGER PRIMARY KEY,
    date DATE NOT NULL,
    category VARCHAR NOT NULL,
    amount REAL NOT NULL,
    notes VARCHAR,
    user_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Usage Example

1. **Start API Server**
   ```bash
   uvicorn api.app:app --reload
   ```

2. **Start GUI**
   ```bash
   python main.py
   ```

3. **Register/Login** - Use the login dialog in the GUI

4. **Add Expenses** - Fill in the form and click "Add Expense"

5. **View Expenses** - See all expenses in the table

6. **Visualize** - Click "Show Pie Chart" to see category distribution

## Troubleshooting

### API Server Won't Start
- Check if port 8000 is available
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check database connection if using PostgreSQL

### GUI Can't Connect to API
- Ensure API server is running on `http://localhost:8000`
- Check firewall settings
- Verify API_BASE_URL in `api_client.py`

### Authentication Errors
- Make sure you're logged in through the GUI
- Token expires after 30 minutes - login again if needed
- Check token format in Authorization header

## API Documentation

Full interactive API documentation is available at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Learning Resources

This project demonstrates:
- REST API design with FastAPI
- Database ORM with SQLAlchemy
- JWT authentication implementation
- Frontend-backend separation
- API client patterns
- Environment-based configuration

## Author

Built by SNEHA GUPTA

## License

This project is open source and available for learning purposes.

---

## 🎉 Project Highlights

**FastAPI Backend** - Modern REST API framework  
**SQLAlchemy ORM** - Database abstraction  
**JWT Authentication** - Secure user authentication  
**PostgreSQL Support** - Production-ready database  
**Pydantic Validation** - Request/response validation  
**Swagger Documentation** - Interactive API docs  
**GUI Frontend** - Tkinter desktop application  
**API Integration** - GUI consumes REST APIs  

This project is now aligned with backend developer requirements and demonstrates full-stack development skills!
