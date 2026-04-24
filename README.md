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

The UX prototype was designed to validate the core interaction model of the WIP Planner and is designed to allow users users to be able to: View work state through a single pane of glass, create and maintain tasks with minimal friction and effort and receive immediate, understandable feedback when attempting to exceed the Work-In-Progress (WIP) limit in line with the mvp scope and problem statement. The design uses a single primary screen which is the Kanban board and a set of modal dialogues for secondary actions (create, edit, delete confirmation, settings, and WIP error)(figure 1). This pattern reduces navigation complexity and keeps users anchored in the board context, which supports task management workflows and lowers cognitive load (Nielsen, 1994; Shneiderman et al., 2016).

![figma-board](./docs/screenshots/day-2-figma.png "figma-designs")

### 2.1 Prototype structure and interaction model
The Kanban board is the main workspace and is organised into three columns: Backlog, In Progress, and Done. This supports the findings of modern research around recognition over recall by making state visible and reducing the need for users to remember where work “should be” (Nielsen, 1994) with the board acting as the source of truth. Task cards display the task title and task description, with action buttons on each card to reduce interaction effort.

All secondary actions are implemented as pop up modals, which ensure users do not lose context or need to navigate away from the board (to other screens) to perform actions (Shneiderman et al., 2016). The modals are context-specific and appear only when needed, minimizing cognitive load. The Modals are as follows:
- Create Task: opens the create modal from the “New Task” button.
- Edit Task: opens the edit modal from the task's edit control.
- Delete Task triggers a delete confirmation modal to prevent accidental destructive actions within the edit modal.
- Settings opens a settings modal to modify the WIP limit.
- WIP Limit Exceeded opens an error modal when the user attempts to move a task into In Progress and the WIP rule would be breached.

This modal-based pattern provides clear interaction boundaries and supports safe task completion by reducing the number of screens the user must traverse (Nielsen, 1994). To ensure the interaction was well defined, prototyping was used in Figma to test the design layout (figure 2)

![Figure 2: Figma prototype of the Kanban board with modals](./docs/videos/figma-prototype.gif)

### 2.2 Key UX decisions and justification
#### Three column structure
The three column workflow has been designed intentionally to promiote interpretability and speed over configurability. For an MVP, this reduces the effort required for onboarding/upskilling and therefore supports rapid adoption by aligning the interface with a familiar mental model of "to do / doing / done" (Shneiderman et al., 2016). The In Progress column explicitly displays the WIP limit, reinforcing the system’s primary goal.

#### WIP limit enforcement 
When a user attempts to move a task into "In Progress" and it exceeds the limit defined for that column, the prototype presents a dedicated “WIP Limit Exceeded” warning. This supports visibility of system status and error prevention by explaining why the action cannot be completed and what the user should do next through an eror message (complete a task before starting another) (Nielsen, 1994). Presenting this feedback immediately reduces ambiguity and discourages workarounds that would undermine flow discipline such as moving a task to backlog to start another.

#### Task creation and editing
The create and edit modals use a minimal set of fields (title required; description optional). This supports research into the area of project management that overly complex capture forms reduce compliance and increase the likelihood of informal “shadow tracking” outside the tool (Ries, 2011).

#### Destructive action protection
Deletion functionality is designed to be completed through a dedicated confirmation modal, reducing the risk of accidental data loss. This reflects a defensive design approach and supports error prevention principles (Shneiderman et al., 2016).

#### Interaction choices (buttons vs drag-and-drop)
Status/column transitions are designed as button actions rather than drag-and-drop. While drag-and-drop can feel intuitive, it is often harder to implement accessibly and reliably across devices without additional design and engineering effort. Button-based transitions provide clearer usability and can be labelled explicitly, the intial design of this project featured one button but future implementation led to 2 buttons (one right and one left), supporting accessibility expectations around operable interfaces and clear controls (W3C, 2023). This decision also reduces engineering risk within a short delivery window, while maintaining functional clarity.

Overall, the prototype is minimal and designed to prove value and feasbility as it demonstrates the end-to-end user journey, makes the WIP constraint visible and enforceable, and keeps interaction cost low. This provides a strong harness for evaluating whether the WIP enforcement design achieves the desired behavioural outcome while remaining usable in delivery contexts (Anderson, 2010).

## 3. Project planning (Kanban board + tickets)

Project planning for the WIP Planner was managed using a Kanban-style workflow in GitHub Projects to support visibility and traceability. Kanban was selected as the project tasks are a set of small, testable work items (created as issues). The board functions as a planning tool and an execution tool.

### 3.1 Board structure and workflow states
The project board uses five columns: Backlog, Ready, In Progress, In Review, and Done.

- Backlog contains tasks that are not yet ready to start.
- Ready acts as a preparation zone for tasks that are ready to be worked on. This allows me to review and refine tasks before they enter development and plan what is to be done next.
- In Progress contains tasks actively being implemented. Work is intentionally kept low in this column to reduce context switching and increase the probability that tasks reach a demonstrable “done” state within the timebox (Anderson, 2010). To match the short timeframe of this build related tickets were allowed to be in progress at once.  
- In Review is used for work that is implemented but awaiting verification. This column was intended to be used for merge requests before they are merged to main however due to me being the only member of the team this was seen as redundant. 
- Done represents work that is merged into `main` and completes the issue.

### 3.2 Ticketing approach and traceability
Work was deconstructued into small issues mapped to the MVP scope: backend persistence and CRUD, WIP settings, WIP enforcement on status transitions, frontend board UI and API integration testing, k8s, ci and docs.

Execution evidence is captured through a PR-first workflow. Each feature was implemented on a branch and merged via a pull request linked to the relevant issue(s). PR descriptions include a summary of changes. This approach also supports the Agile tenat incremental integration which states smaller PRs reduce merge risk and make it easier to identify regressions compared with large changes (Beck et al., 2001).

Links and evidence:
- See [section 4](#4-mvp-implementation-overview) for a list of features, PRs and evidence of the kanban board state associated with these PRs.

## 4. MVP implementation overview

### Build log (academic implementation narrative)

The implementation of this project was delivered iteratively over a 1 week sprint. The following log captures the tangible outcomes of each day:

#### Day 1 (Setup & scaffolding)
- Created repo structure (`backend/`, `frontend/`, `docs/`, `k8s/`) and initial README headings for traceability.
- Bootstrapped FastAPI with `/health` for smoke checks and early verification.
- Bootstrapped frontend (react JS)
![frontend-basic](docs/screenshots/front-end-basic.png)
- Created GitHub Projects board and initial issues to track delivery.
- [PR #15: chore: day 1 scaffold backend/frontend and README](https://github.com/asaaumar/wip-planner/pull/15)
- Kanban board state: 
- ![screenshot](docs/screenshots/day-1-board.png)

#### Day 2 (UX prototype & API Contract)
- Produced a clickable Figma prototype using a single-board view with pop up modals (create/edit/delete/settings/WIP error).
- Defined the MVP API contract (tasks + settings endpoints)
- Figma evidence in: screenshots (`docs/screenshots/`) and prototype video (`docs/videos/`).
- [PR #19: feature: add SQLite persistence and task model](https://github.com/asaaumar/wip-planner/pull/19)
- Kanban board state: 
- ![screenshot](docs/screenshots/day-2-board.png)

#### Day 3 (Backend persistence + CRUD + test harness)
- Implemented SQLite persistence and Task model to store tasks across sessions.
- Added CRUD endpoints: `GET/POST/PUT/DELETE /tasks` and verified via FastAPI interactive docs.
![CRUD endpoints](docs/screenshots/task-crud-endpoints.png)
- Added `GET/PUT /settings` for WIP limit configuration.
![Settings Get](docs/screenshots/settings-get.png)
![Settings Get](docs/screenshots/settings-put.png)
- Added pytest harness + initial smoke test to support tdd work.
- [PR #19: feature: add SQLite persistence and task model](https://github.com/asaaumar/wip-planner/pull/19)
- [PR #20: feature: implement task CRUD endpoints](https://github.com/asaaumar/wip-planner/pull/20)
- [PR #21: Feature: added get specific task endpoint](https://github.com/asaaumar/wip-planner/pull/21)
- [PR #23: feature: add settings endpoints for WIP limit](https://github.com/asaaumar/wip-planner/pull/23)
- [PR #24: test: add pytest scaffold and health endpoint test](https://github.com/asaaumar/wip-planner/pull/24)
- Kanban board state: 
- ![screenshot](docs/screenshots/day-3-board.png)


#### Day 4 (WIP rule + status transitions with TDD)
- Added `PATCH /tasks/{id}/status`.
- ![endpoint-screenshot](docs/screenshots/day-4-endpoints.png)
- Implemented WIP enforcement when moving to `IN_PROGRESS`; returns `409` with structured error when limit exceeded.
![patch-status-screenshot](docs/screenshots/patch-success.png)
![patch-409-screenshot](docs/screenshots/patch-409.png)
- Added unit tests using a TDD sequence (write test, watch test fail, write code to pass test, watch test pass) for the WIP rule enforcement.
- [PR #26: test: add failing tests for WIP rule (TDD), feat: implement WIP rule to satisfy tests](https://github.com/asaaumar/wip-planner/pull/26)
- [PR #27: test: written tests for checking wip limit when changing status, feature: added patch endpoint to change status,wrote code to pass wip enforcement tests](https://github.com/asaaumar/wip-planner/pull/27)
- Kanban board state: 
- ![screenshot](docs/screenshots/day-4-board.png)

#### Day 5 (Frontend integration + error UX + containerisation)
- Implemented 3-column Kanban UI and connected to backend (load + create tasks).
- ![frontend-with-tickets](docs/screenshots/frontend-with-tickets.png)
-![frontend-create-task](docs/screenshots/frontend-create-task.png)
- Added button-based status transitions and UI handling for `409 WIP_LIMIT_EXCEEDED` responses.
![frontend-wip-enforcement-warning](docs/screenshots/frontend-wip-enforcement-warning.png)
- Added settings modal to update WIP limit via `/settings`.
![frontend-settings](docs/screenshots/frontend-settings.png)
![front-end-2wip](docs/screenshots/front-end-2wip.png)
- Added edit task modal
![frontend-edit](docs/screenshots/frontend-edit.png)
- Added Dockerfiles for backend and frontend to enable reproducible builds and deployment.
- [PR #32:feature: add frontend kanban board layout](https://github.com/asaaumar/wip-planner/pull/32)
- [PR #33: feature: connect frontend to backend (load and create tasks) with WIP enforcement](https://github.com/asaaumar/wip-planner/pull/33)
- [PR #35: feature: added settings modal to change WIP](https://github.com/asaaumar/wip-planner/pull/35)
- [PR #36: k8s: added Dockerfile and dockerignore](https://github.com/asaaumar/wip-planner/pull/36)
- ![screenshot](docs/screenshots/day-5-board.png)
- ![screenshot](docs/screenshots/day-52-board.png)
- ![screenshot](docs/screenshots/day-53-board.png)

#### Day 6 (Documentation)
- Expanded README sections to document UX decisions, API contract, implemented features, and evidence (PRs, screenshots).

#### Day 7 (Deployment yamls + OpenShift)
- Wrote Kubernetes/OpenShift manifest YAMLs and deployed the final version to OpenShift.
- [PR #41: k8s: added deployment manifests for front end, k8s: added deployment manifests for backend, fix: made changes to apps to work with eachother ink8s env](https://github.com/asaaumar/wip-planner/pull/41)
- Added CI through github actions to redploy on PR merge.
- [PR #42: ci: add GitHub Actions workflows, test: trigger backend deployment, ci: changed files to watch main after testing](https://github.com/asaaumar/wip-planner/pull/42)
- Completed user and technical documentation (local run + deployment steps).
- ![screenshot](docs/screenshots/day-7-board.png)
- ![screenshot](docs/screenshots/day-72-board.png)


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
- Nielsen, J. (1994) *Usability engineering*. San Francisco, CA: Morgan Kaufmann.  
- Ries, E. (2011) *The Lean Startup: How today’s entrepreneurs use continuous innovation to create radically successful businesses*. New York: Crown Business.  
- Shneiderman, B. et al. (2016) *Designing the user interface: Strategies for effective human-computer interaction*. 6th edn. Boston, MA: Pearson.  
- W3C (2023) *Web Content Accessibility Guidelines (WCAG) 2.2*. Available at: https://www.w3.org/TR/WCAG22/