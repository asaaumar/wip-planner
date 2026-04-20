# WIP Planner

## MVP statement
 A web-based Kanban board with enforced Work-In-Progress limits, built with FastAPI (Python) and a JavaScript frontend, including tests, CI/CD, and Kubernetes deployment.

## 1. Product proposal

### 1.1. Problem statement
  - In short timeboxed delivery environments, work often gets started but not finished, creating high work-in-progress (WIP), context switching, and reduced visibility of true progress.
  - Too many items in prohress causes bottlenecks.

### 1.2. Solution proposal and rationale
  - Small software delivery teams or individuals working in short cycles (e.g., weekly sprints) who need clearer visibility of progress and stronger flow discipline.
  - Users who want simple guidance to avoid overloading the “In Progress” column and to finish work before starting new tasks.
  - Web-based Kanban board with strict wip enforcement to prevent overloading and improve flow.

### 1.3. MVP Scope
  1. Board with three columns: Backlog, In Progress, Done
  2. Task management (create, edit, delete) with title and optional description
  3. Ability to move tasks between columns (status transitions)
  4. WIP limit enforcement on the “In Progress” column (default limit = 1) with a clear warning/error when exceeded
  5. Persistence so tasks remain available between sessions (stored and reloaded automatically)

### 1.4. Non-MVP Scope (Stretch Goals)
  - Drag-and-drop interaction (button-based movement is sufficient)
  - User accounts, authentication, or multi-user permissions
  - Advanced analytics (e.g., cycle time dashboards, forecasting) beyond simple visibility
  - Integrations with external tools (e.g., Jira/Slack) in the MVP phase

### 1.5. Data Model/API Contract
The core data model for functionality in the WIP Planner is as follows:

```json
{
  "id": "string (UUID)",
  "title": "string",
  "description": "string (optional)",
  "status": "string (enum: 'todo', 'in-progress', 'done')",
  "created_at": "string (ISO 8601 datetime)",
  "updated_at": "string (ISO 8601 datetime)"
}
```

#### Field Descriptions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string (UUID) | Yes | Unique identifier for the task |
| `title` | string | Yes | Task title (max 200 characters) |
| `description` | string | No | Detailed task description |
| `status` | enum | Yes | Current status: `todo`, `in-progress`, or `done` |
| `created_at` | ISO 8601 datetime | Yes | Timestamp when task was created |
| `updated_at` | ISO 8601 datetime | Yes | Timestamp when task was last updated |

#### Validation Rules

- `title`: Required, non-empty, max 200 characters
- `status`: Must be one of: `todo`, `in-progress`, `done`
- `description`: Optional, max 2000 characters

#### Error Response Format

All API errors return a consistent format that maps to UI error toasts/modals:

```json
{
  "error": {
    "code": "string",
    "message": "string",
    "field": "string (optional)",
    "details": "object (optional)"
  }
}
```

**Example Error Response:**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Task title is required",
    "field": "title"
  }
}
```

#### Common Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `VALIDATION_ERROR` | 400 | Invalid input data |
| `NOT_FOUND` | 404 | Task not found |
| `WIP_LIMIT_EXCEEDED` | 409 | Work-in-progress limit reached |
| `INTERNAL_ERROR` | 500 | Server error |

#### REST API Endpoints

- `GET /tasks` - List all tasks
- `POST /tasks` - Create a new task
- `GET /tasks/{id}` - Get a specific task
- `PUT /tasks/{id}` - Update a task
- `DELETE /tasks/{id}` - Delete a task
- `PATCH /tasks/{id}/status` - Update task status

## 2. UX prototype (Figma)
## 3. Project planning (Kanban board + tickets)
## 4. MVP implementation overview

### Build log

#### Day 1 (Setup & scaffolding)**
- Created repository structure for `backend/`, `frontend/`, `docs/`, `k8s/`.
- Bootstrapped the backend with a FastAPI skeleton and a `/health` endpoint for smoke-checking the API.
- Bootstrapped the frontend using a vanilla JavaScript template to establish the UI build.
- Added the README structure aligned to the assessment deliverables and documented the MVP statement.
- Set up the GitHub Project board (Kanban) and created initial issues/milestones to track MVP, testing, CI/CD, and deployment work.

#### Day 2 (Proposal, UX prototype, and API contract)**
- Documented the product proposal (problem, target users, MVP features, and non-goals) in the root README.
- Created a clickable UX prototype (Figma) covering the main screens: board, create/edit task, settings (WIP limit), and error state.
- Defined the MVP API contract (tasks + settings endpoints) including the expected WIP limit error response (409 conflict with a clear message).
- Added UX screenshots to `docs/screenshots/` and a UX video in `docs/videos/` for later use in the README.

#### Day 3 (Backend persistence and CRUD)**
- Implemented SQLite persistence and added a Task data model to support stored tasks across sessions.
- Added backend CRUD endpoints for tasks (create/list/update/delete) and verified behaviour using FastAPI interactive docs.
- Captured evidence for documentation (FastAPI `/docs` screenshot showing task endpoints) and updated build log
- Added settings endpoints to get and put wip limit settings and defined associated model
- Added a test harness and simple test to setup for tdd work

## 5. Pull requests and workflow evidence
- [PR #15: chore: day 1 scaffold backend/frontend and README](https://github.com/asaaumar/wip-planner/pull/15)
- [PR #19: feature: add SQLite persistence and task model](https://github.com/asaaumar/wip-planner/pull/19)
- [PR #20: feature: implement task CRUD endpoints](https://github.com/asaaumar/wip-planner/pull/20)
- [PR #21: Feature: added get specific task endpoint](https://github.com/asaaumar/wip-planner/pull/21)
- [PR #23: feature: add settings endpoints for WIP limit](https://github.com/asaaumar/wip-planner/pull/23)
- [PR #24: test: add pytest scaffold and health endpoint test](https://github.com/asaaumar/wip-planner/pull/24)
## 6. UI implementation notes
## 7. Testing + accessibility evidence

- Pytest scaffold added: health check and init tests passing.

## 8. TDD example
## 9. CI/CD + production deployment (Kubernetes)
## 10. User guide + technical documentation

## How to run locally
## Deployment