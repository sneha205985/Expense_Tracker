from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router
from api.database import init_db

# Initialize FastAPI app
app = FastAPI(
    title="Expense Tracker API",
    description="REST API for Expense Tracker application with JWT authentication",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware (allow frontend to access API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router, prefix="/api", tags=["expenses"])

# Root endpoint
@app.get("/")
def root():
    return {
        "message": "Welcome to Expense Tracker API",
        "docs": "/docs",
        "redoc": "/redoc"
    }


# Initialize database on startup
@app.on_event("startup")
def startup_event():
    init_db()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
