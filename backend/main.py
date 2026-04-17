"""
WIP Planner Backend API
A FastAPI application for managing Kanban boards with WIP limits.
"""
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from datetime import datetime

app = FastAPI(
    title="WIP Planner API",
    description="Backend API for WIP Planner - A Kanban board with enforced Work-In-Progress limits",
    version="0.1.0"
)


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
