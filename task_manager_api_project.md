# The Project: Task Manager API

Build a task/todo manager. In-memory storage only — a Python dict keyed by ID. No database yet (that's Week 3).

## Required Data Model

```python
class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    done = "done"

class TaskIn(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str | None = None
    status: TaskStatus = TaskStatus.pending
    priority: int = Field(ge=1, le=5, default=3)

class TaskOut(BaseModel):
    id: int
    title: str
    description: str | None
    status: TaskStatus
    priority: int
```

You decide the exact fields, but it must include: at least one Enum, at least one `Field()` constraint, and a separate input vs output model (there should be a reason `TaskOut` differs from `TaskIn` — e.g. `id` is server-assigned, never client-provided).

## Required Endpoints

| Endpoint | Must demonstrate |
|---|---|
| `POST /tasks` | Body validation via `TaskIn`, `status_code=201`, `response_model=TaskOut` |
| `GET /tasks` | Query params `skip`/`limit` with `Query(ge=0)` constraints, filter by `status` (enum query param) |
| `GET /tasks/{task_id}` | Path param validation, `HTTPException(404)` if not found |
| `PATCH /tasks/{task_id}` | Partial update (only fields provided get changed), `response_model_exclude_unset=True` demonstrated somewhere |
| `DELETE /tasks/{task_id}` | `status_code=204`, `HTTPException(404)` if not found |

## Also Required

- **Custom exception:** One custom exception class (e.g. `TaskNotFoundError`) with a global `@app.exception_handler` — use it in at least the GET-by-id and DELETE routes instead of raw `HTTPException` in those two, so you're using both mechanisms from Day 4 for real, not just one.
- **Route ordering correctness:** Add a fixed route like `GET /tasks/stats` (returns count by status) *after* `GET /tasks/{task_id}` deliberately first, confirm it breaks (Day 2's shadowing bug, for real this time), then fix the ordering.
- **Sync functions only:** All functions `def`, not `async def` — no exceptions, this is still pre-Day-24.

## What "Done" Looks Like

Every endpoint tested manually through `/docs` — not just written, actually clicked "Try it out" on each one, including the failure paths (invalid body, missing task, invalid enum value, limit out of range). If you haven't seen a 422 and a 404 actually come back from your own code today, you haven't finished the day.
