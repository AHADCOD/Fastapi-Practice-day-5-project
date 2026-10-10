from fastapi import FastAPI, status, Query, status, Request
from fastapi.responses import JSONResponse
from typing import Annotated
from pydantic import BaseModel, Field
from enum import Enum

app = FastAPI()

tasks = {

}
class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    done = "done"

class TaskBase(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str | None = None
    status: TaskStatus = TaskStatus.pending
    priority: int = Field(ge=1, le=5, default=3)

class TaskIn(TaskBase):
    pass

class TaskOut(TaskBase):
    id: int

class TaskUpdate(BaseModel):
    title: str|None = Field(min_length=1, max_length=100, default=None)
    description: str|None = None
    status: TaskStatus |None = None
    priority: int|None = Field(ge=1, le=5, default=None)


@app.get("/")
def home():
    return {"Message": "Welcome to the first small project of APIs."}

@app.post("/tasks", status_code=status.HTTP_201_CREATED, response_model=TaskOut)
def add_tasks(task: TaskIn):
    user_task = task.model_dump()
    task_id = max(list(tasks.keys())) + 1 if tasks else 1
    tasks[task_id] = user_task
    return {"id": task_id, **user_task}

@app.get("/tasks")
def get_tasks(skip: Annotated[int, Query(ge=0)], limit: Annotated[int|None, Query(gt=0)] = None,  task_status: TaskStatus | None = None):
    filtered_tasks = []
    for key in tasks:
        if(task_status is None or tasks[key]["status"] == task_status):
            filtered_tasks.append({**tasks[key], "id": key})

    if(len(filtered_tasks) == 0):
        return []
    else:
        if limit is None:
            return filtered_tasks[skip:]
        return filtered_tasks[skip: skip + limit]

@app.get("/tasks/stats")
def get_stats():
    stats = {
        "pending": 0,
        "in_progress": 0,
        "done": 0
    }

    for key in tasks:
        stats[tasks[key]["status"]] += 1

    return stats


@app.get("/tasks/{task_id}", response_model=TaskOut)
def get_task(task_id: int):
    if task_id not in tasks:
        raise TaskNotFoundError(task_id)

    return {**tasks[task_id], "id": task_id}

@app.patch("/tasks/{task_id}", response_model_exclude_unset=True, response_model=TaskOut)
def update_task(task_id: int, task: TaskUpdate):
    if task_id not in tasks.keys():
        raise TaskNotFoundError(task_id)

    updated_task = task.model_dump(exclude_unset=True)

    for key, value in updated_task.items():
        if(value != None):
            tasks[task_id][key] = value

    return {**tasks[task_id], "id": task_id}


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def del_task(task_id: int):
    if task_id not in tasks:
            raise TaskNotFoundError(task_id)

    del tasks[task_id]
    return 


class TaskNotFoundError(Exception):
    def __init__(self, task_id):
        self.task_id = task_id


@app.exception_handler(TaskNotFoundError)
def Tasknotfound(request: Request, exc: TaskNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"error": f"Task of ID '{exc.task_id}' was not found"}
    )