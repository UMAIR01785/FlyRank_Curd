from fastapi import FastAPI, HTTPException

from .database import initialize_database
from .schemas import TaskCreate, TaskUpdate
from .crud import (
    get_all_tasks,
    get_task_by_id,
    create_task,
    update_task,
    delete_task
)


app = FastAPI()


initialize_database()


@app.get("/")
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.get("/tasks")
def get_tasks():
    return get_all_tasks()


@app.get("/tasks/{id}")
def get_task(id: int):

    task = get_task_by_id(id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task {id} not found"
        )

    return task


@app.post("/tasks", status_code=201)
def create_new_task(task: TaskCreate):

    return create_task(task.title)


@app.put("/tasks/{id}")
def update_existing_task(id: int, task_update: TaskUpdate):

    if (
        task_update.title is not None
        and not task_update.title.strip()
    ):
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )

    task = update_task(
        id,
        task_update.title,
        task_update.done
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task {id} not found"
        )

    return task


@app.delete("/tasks/{id}", status_code=204)
def delete_existing_task(id: int):

    deleted = delete_task(id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail=f"Task {id} not found"
        )

    return