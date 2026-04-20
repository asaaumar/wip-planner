"""
WIP Planner Backend API
A FastAPI application for managing Kanban boards with WIP limits.
"""
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from datetime import datetime

from app.db.session import engine, Base
from app.models import task  # Import models to register them with Base
from app.routers import tasks

app = FastAPI(
    title="WIP Planner API",
    description="Backend API for WIP Planner - A Kanban board with enforced Work-In-Progress limits",
    version="0.1.0"
)

# Include routers
app.include_router(tasks.router)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    print("Starting WIP Planner API")
    print("Creating database tables")
    
    # Create all tables defined in models
    Base.metadata.create_all(bind=engine)
    
    print("Database tables created successfully")


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


