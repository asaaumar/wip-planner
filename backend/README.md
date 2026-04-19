# WIP Planner Backend

FastAPI backend service for the WIP Planner application - a Kanban board with enforced Work-In-Progress limits.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Quick Start

Follow these steps to get the backend running in a virtual environment:

### 1. Navigate to the backend directory
```bash
cd backend
```

### 2. Create a virtual environment
```bash
python3 -m venv venv
```

### 3. Activate the virtual environment

**On macOS/Linux:**
```bash
source venv/bin/activate
```

**On Windows:**
```bash
venv\Scripts\activate
```

You should see `(venv)` appear in your terminal prompt, indicating the virtual environment is active.

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

This installs FastAPI, Uvicorn, and other required packages.

### 5. Run the application
```bash
python main.py
```

Or with auto-reload for development:
```bash
uvicorn main:app --reload
```

The API will be available at: `http://localhost:8000`

### 6. Test the health check endpoint
Open a new terminal and run:
```bash
curl http://localhost:8000/health
```

Or visit http://localhost:8000/docs in your browser to see the interactive API documentation.

### 7. Deactivate the virtual environment (when done)
```bash
deactivate
```

## API Documentation

For the complete API contract including the Task model, validation rules, error response format, and REST endpoints, see the [API Contract section in the main README](../README.md#15-data-modelapi-contract).

