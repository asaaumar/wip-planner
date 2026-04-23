# WIP Planner

## MVP statement
 A web-based Kanban board with enforced Work-In-Progress limits, built with FastAPI (Python) and a JavaScript frontend, including tests, CI/CD, and Kubernetes deployment.

## 1. Product proposal

### 1.1 Problem statement
Software delivery teams working in short, timeboxed cycles frequently encounter a predictable pattern: work is started quickly, but completion and validation lag behind. Under delivery pressure, teams may initiate multiple items in parallel to appear responsive, but this can be distracting and increase context switching. From a flow-based perspective, the result is often an accumulation of partially completed work in “in progress” states, while activities that prove completeness such as integration and end-to-end testing are deferred (Anderson, 2010). This creates a false positive of productivity which does not reflect the true completed tickets for the sprint. 

High work-in-progress (WIP) is problematic because it hides bottlenecks and makes it harder to identify the true constraint in the system or team. When WIP is unconstrained and unmonitored, delays are not made visible as a  problem as they appear in progress and not blocked. This increases lead times and creates uneven delivery between sprints where tasks remain partially complete across multiple cycles and must be re assessed repeatedly (Anderson, 2010). Agile methods aim to reduce waste and deliver working increments frequently, but these outcomes depend on disciplined work management; without explicit flow controls, teams can inadvertently optimise for starting rather than finishing (Beck et al., 2001). In addition, teams often lack a mechanism to signal when “in progress” is saturated and should not be expanded further-especially in environments where external stakeholders have visibility of wip and there may be a pressure to appear busy.

As mentioned above, this problem is amplified in client-facing or high-accountability contexts where delivery credibility depends not only on activity, but on demonstrable outcomes through playbacks. If work resource is spread too thin or an engineer is aligned to too many tickets due for completion, teams may miss opportunities to  demonstrate value, validate behaviour end-to-end (testing), and produce evidence that a feature is “done” in a meaningful sense in front of a client. Subsequently, stakeholders may request additional proof, rework, or changes late in the cycle, further increasing churn. A lightweight mechanism that improves flow discipline and makes constraints explicit can therefore support both delivery performance and stakeholder confidence.

### 1.2 Solution proposal and rationale
The proposed solution is a lightweight web-based WIP Planner: a minimal Kanban board that makes work state visible and enforces a Work-In-Progress limit to encourage completion before taking on more tasks. The application provides a three-column workflow (Backlog, In Progress, Done) and prevents users from having too many tickets in the “In Progress” column by enforcing a configurable WIP limit (default = 1). The proposal rationale follows modern Kanban practices: limiting WIP is a central mechanism for stabilising flow, reducing context switching, and surfacing bottlenecks early (Anderson, 2010). Rather than relying on informal self-control.

The design intentionally avoids complexity. Many task management tools similar to the proposed often focus on being feature-rich, but feature depth is not the primary requirement for improving flow and therefore ot the scope for the project. Instead, the WIP Planner focuses on a small set of actions that support the core behavioural change: capturing work clearly, starting only what can be completed (enforced by WIP), and making exceptions visible (ticket in progress for too long). This aligns with the Agile principle of prioritising working, inspectable outcomes and reducing process overhead that does not contribute to value (Beck et al., 2001). The solution also supports clear feedback at the point of action: when a user attempts to move an item into “In Progress” and the WIP limit has been reached, the system provides immediate feedback and blocks the move. This creates a consistent rule set that reduces ambiguity and helps users understand why flow discipline matters in practice.

Additionally, a minimal three-state (columns) workflow drives interpretability; users can quickly understand the meaning of each state/column and the expectations attached to it. This is particularly useful in short-cycle delivery (such as daily or weekly sprints) where teams need a common model of “what is happening” without investing time in maintaining process artefacts and admin. The proposal therefore prioritises usability and clarity over sophistication, while still providing enough structure to demonstrate professional advanced software engineering practice in implementation, testing, CI/CD, deployment and documentation.

### 1.3 Target users and value proposition
The primary target users for the project are small software delivery teams (or individuals) operating in short cycles (weekly or daily sprints) who need clearer visibility of progress and a simple way of preventing over burdoning engineers. A key point of note is that the value proposition is not that the tool replaces established enterprise platforms (such as monday.com), but that it provides an intentionally constrained workflow to reinforce good flow habits and can be used as an informal tracker/training tool. For teams, the tool offers: improved transparency of work state reduced hidden work caused by excessive parallelism (such as integration testing) and a clearer pathway to producing demonstrable increments with completed tickets tracked in "Done". For individuals, the tool acts as a self-management/training aid which enforces behaviour that aligns with the mentality that finishing tasks is often more valuable than starting additional ones (team culture).

The educational value of the tool is that it is designed to make flow concepts digestible. By enforcing a WIP limit and presenting clear feedback, it helps users connect abstract ideas such as WIP, bottleneck and throughput to behaviour. This provides a strong basis for evaluating whether WIP limits improve completion within time constraints and how different limits can affext sprint deliverables.

### 1.4 MVP scope
The MVP is deliberately scoped to address the issues in the problem statement while remaining deliverable within the assessment timeline.

1. A three-column board: Backlog, In Progress, Done
2. Task management: create, edit, delete tasks (title required; description optional)
3. Status transitions between columns (button-based movement)
4. WIP limit enforcement on “In Progress” (default limit = 1) with clear error feedback when exceeded
5. Persistence so tasks remain available between sessions (stored and reloaded automatically)

### 1.5 Non-MVP scope (stretch goals)
To prevent scope creep, the following features are explicitly out of scope for the MVP:
- Drag-and-drop interactions (buttons are sufficient and reduce accessibility risk)
- Authentication, user accounts, and multi-user permissions
- Advanced analytics (cycle time dashboards, forecasting)
- Integrations with external platforms (e.g., Jira/Slack)
- Complex workflow configurations beyond three core states

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

**Task Endpoints:**
- `GET /tasks` - List all tasks
- `POST /tasks` - Create a new task
- `GET /tasks/{id}` - Get a specific task
- `PUT /tasks/{id}` - Update a task
- `DELETE /tasks/{id}` - Delete a task
- `PATCH /tasks/{id}/status` - Update task status (with WIP limit enforcement)

**Settings Endpoints:**
- `GET /settings/` - Get current WIP limit settings
- `PUT /settings/` - Update WIP limit

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
 
#### Day 4 (WIP with TDD)**
- Added PATCH status endpoint with WIP enforcement and 409 error
- Added unit-tested WIP rule via TDD

#### Day 5 (Wed 22 Apr):**
- Implemented frontend Kanban board UI (3 columns).
- Connected frontend to backend API (load tasks + create tasks).
- Added status transition buttons and UI handling for WIP limit errors (409).
- Added settings to allow users to set WIP limit.
  
## 5. Pull requests and workflow evidence
- [PR #15: chore: day 1 scaffold backend/frontend and README](https://github.com/asaaumar/wip-planner/pull/15)
- [PR #19: feature: add SQLite persistence and task model](https://github.com/asaaumar/wip-planner/pull/19)
- [PR #20: feature: implement task CRUD endpoints](https://github.com/asaaumar/wip-planner/pull/20)
- [PR #21: Feature: added get specific task endpoint](https://github.com/asaaumar/wip-planner/pull/21)
- [PR #23: feature: add settings endpoints for WIP limit](https://github.com/asaaumar/wip-planner/pull/23)
- [PR #24: test: add pytest scaffold and health endpoint test](https://github.com/asaaumar/wip-planner/pull/24)
- [PR #26: test: add failing tests for WIP rule (TDD), feat: implement WIP rule to satisfy tests](https://github.com/asaaumar/wip-planner/pull/26)
- [PR #27: test: written tests for checking wip limit when changing status, feature: added patch endpoint to change status,wrote code to pass wip enforcement tests](https://github.com/asaaumar/wip-planner/pull/27)
- [PR #32:f eature: add frontend kanban board layout](https://github.com/asaaumar/wip-planner/pull/32)
- [PR #33: feature: connect frontend to backend (load and create tasks) with WIP enforcement](https://github.com/asaaumar/wip-planner/pull/33)
- [PR #35: feature: added settings modal to change WIP](https://github.com/asaaumar/wip-planner/pull/35)


## 6. UI implementation notes
## 7. Testing + accessibility evidence

- Pytest scaffold added: health check and init tests passing.

## 8. TDD example
## 9. CI/CD + production deployment (Kubernetes)
## 10. User guide + technical documentation

## How to run locally
## Deployment

## References
- Anderson, D.J. (2010) *Kanban: Successful evolutionary change for your technology business*. Sequim, WA: Blue Hole Press.  
- Beck, K. et al. (2001) *Manifesto for Agile Software Development*. Available at: https://agilemanifesto.org/