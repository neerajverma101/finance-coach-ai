"""
FastAPI application entry point.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.models.database import init_db
from backend.api import auth
from backend.config import settings

# Initialize FastAPI app
app = FastAPI(
    title="Personal Finance Coach API",
    description="Privacy-first personal finance coaching with deterministic rules and explainable AI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)

# TODO: Add more routers as they are created
# app.include_router(profile.router)
# app.include_router(snapshot.router)
# app.include_router(plan.router)


@app.on_event("startup")
def startup_event():
    """Initialize database on startup."""
    init_db()
    print(f"✅ Database initialized ({settings.ENV} mode)")
    print(f"📊 Database URL: {settings.DATABASE_URL}")


@app.get("/")
def root():
    """API root endpoint."""
    return {
        "message": "Personal Finance Coach API",
        "version": "1.0.0",
        "status": "running",
        "environment": settings.ENV,
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "environment": settings.ENV
    }
