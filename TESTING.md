# API Testing Guide

This guide explains how to test the Expense Tracker REST API using Postman.

## Prerequisites

1. Start the API server:
   ```bash
   python run_api.py
   # or
   uvicorn api.app:app --reload
   ```

2. Import the Postman collection (optional):
   - Open Postman
   - Click "Import" → Select `POSTMAN_COLLECTION.json`
   - Set environment variable `base_url` to `http://localhost:8000`

## Testing Workflow

### Step 1: Register a User

**Endpoint:** `POST /api/auth/register`

**Request Body:**
```json
{
    "username": "testuser",
    "email": "test@example.com",
    "password": "test123"
}
```

**Expected Response:** `201 Created`
```json
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "token_type": "bearer"
}
```

**Note:** Save the `access_token` for subsequent requests.

### Step 2: Login (Alternative)

**Endpoint:** `POST /api/auth/login`

**Request Body:**
```json
{
    "username": "testuser",
    "password": "test123"
}
```

**Expected Response:** `200 OK` with access token

### Step 3: Create an Expense

**Endpoint:** `POST /api/expenses`

**Headers:**
```
Authorization: Bearer <your-access-token>
Content-Type: application/json
```

**Request Body:**
```json
{
    "date": "2026-02-20",
    "category": "Food",
    "amount": 150.50,
    "notes": "Lunch at restaurant"
}
```

**Expected Response:** `201 Created`
```json
{
    "id": 1,
    "date": "2026-02-20",
    "category": "Food",
    "amount": 150.50,
    "notes": "Lunch at restaurant"
}
```

### Step 4: Get All Expenses

**Endpoint:** `GET /api/expenses?skip=0&limit=100`

**Headers:**
```
Authorization: Bearer <your-access-token>
```

**Expected Response:** `200 OK`
```json
[
    {
        "id": 1,
        "date": "2026-02-20",
        "category": "Food",
        "amount": 150.50,
        "notes": "Lunch at restaurant"
    }
]
```

### Step 5: Get Expense by ID

**Endpoint:** `GET /api/expenses/{id}`

**Headers:**
```
Authorization: Bearer <your-access-token>
```

**Expected Response:** `200 OK` with expense object

### Step 6: Update Expense

**Endpoint:** `PUT /api/expenses/{id}`

**Headers:**
```
Authorization: Bearer <your-access-token>
Content-Type: application/json
```

**Request Body:**
```json
{
    "amount": 200.00,
    "notes": "Updated notes"
}
```

**Expected Response:** `200 OK` with updated expense

### Step 7: Delete Expense

**Endpoint:** `DELETE /api/expenses/{id}`

**Headers:**
```
Authorization: Bearer <your-access-token>
```

**Expected Response:** `204 No Content`

## Testing Error Cases

### Test 1: Unauthorized Access
- Try accessing `/api/expenses` without Authorization header
- **Expected:** `401 Unauthorized`

### Test 2: Invalid Token
- Use an invalid or expired token
- **Expected:** `401 Unauthorized`

### Test 3: Invalid Expense Data
- Try creating expense with negative amount
- **Expected:** `422 Unprocessable Entity` (validation error)

### Test 4: Non-existent Expense
- Try accessing `/api/expenses/999`
- **Expected:** `404 Not Found`

### Test 5: Duplicate Registration
- Try registering with existing username/email
- **Expected:** `400 Bad Request`

## Using Postman Collection

1. **Import Collection:**
   - File → Import → Select `POSTMAN_COLLECTION.json`

2. **Set Environment Variables:**
   - Create a new environment
   - Add variable `base_url` = `http://localhost:8000`
   - Add variable `access_token` = (will be auto-set after login/register)

3. **Auto Token Management:**
   - The collection includes test scripts that automatically save tokens
   - After Register/Login, token is saved to `access_token` variable
   - All expense endpoints use this token automatically

4. **Run Collection:**
   - Right-click collection → "Run collection"
   - Or run requests individually

## Using cURL

### Register
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "test123"
  }'
```

### Login
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "test123"
  }'
```

### Create Expense (replace TOKEN)
```bash
curl -X POST "http://localhost:8000/api/expenses" \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "date": "2026-02-20",
    "category": "Food",
    "amount": 150.50,
    "notes": "Lunch"
  }'
```

### Get All Expenses
```bash
curl -X GET "http://localhost:8000/api/expenses" \
  -H "Authorization: Bearer TOKEN"
```

## HTTP Status Codes Used

- `200 OK` - Successful GET/PUT request
- `201 Created` - Successful POST (create)
- `204 No Content` - Successful DELETE
- `400 Bad Request` - Invalid request (e.g., duplicate registration)
- `401 Unauthorized` - Missing or invalid authentication
- `404 Not Found` - Resource not found
- `422 Unprocessable Entity` - Validation error (Pydantic)

## Testing Checklist

- [ ] Register new user
- [ ] Login with credentials
- [ ] Create expense (with all fields)
- [ ] Create expense (with minimal fields)
- [ ] Get all expenses
- [ ] Get expense by ID
- [ ] Update expense (partial update)
- [ ] Update expense (full update)
- [ ] Delete expense
- [ ] Test unauthorized access
- [ ] Test invalid token
- [ ] Test validation errors
- [ ] Test non-existent resource
- [ ] Test user isolation (users can't see each other's expenses)

## Notes

- All expense endpoints require authentication
- Tokens expire after 30 minutes
- Users can only access their own expenses
- All requests/responses are validated using Pydantic
- Database uses SQLAlchemy ORM for all operations
