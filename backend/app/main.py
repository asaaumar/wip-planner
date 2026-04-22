"""
WIP Planner Backend API
A FastAPI application for managing Kanban boards with WIP limits.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime

from app.db.session import engine, Base, SessionLocal
from app.models import task, settings  # Import models to register them with Base
from app.models.settings import Settings
from app.routers import tasks, settings

app = FastAPI(
    title="WIP Planner API",
    description="Backend API for WIP Planner - A Kanban board with enforced Work-In-Progress limits",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(tasks.router)
app.include_router(settings.router)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    print("Starting WIP Planner API")
    print("Creating database tables")
    
    # Create all tables defined in models
    Base.metadata.create_all(bind=engine)
    
    # Initialize settings table with default values if it doesn't exist
    db = SessionLocal()
    try:
        existing_settings = db.query(Settings).filter(Settings.id == 1).first()
        if not existing_settings:
            default_settings = Settings(id=1, wip_limit=1)
            db.add(default_settings)
            db.commit()
            print("Initialized settings with default WIP limit = 1")
        else:
            print(f"Settings loaded: WIP limit = {existing_settings.wip_limit}")
    finally:
        db.close()
    
    print("Database initialized successfully")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("Shutting down WIP Planner API")


@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "name": "WIP Planner API",
        "version": "0.1.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint
    
    Returns the current health status of the API including:
    - Status: healthy/unhealthy
    - Timestamp: Current server time
    - Version: API version
    """
    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "version": "0.1.0",
            "service": "wip-planner-backend"
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


