from fastapi import FastAPI, HTTPException
from pydantic import BaseModel,Field
app = FastAPI()


tasks = [
    {
        "id": 1,
        "title": "Learn FastAPI",
        "done": False
    },
    {
        "id": 2,
        "title": "Build CRUD API",
        "done": False
    },
    {
        "id": 3,
        "title": "Push project to GitHub",
        "done": False
    }
]
class Taskcreate(BaseModel):
    title:str = Field(min_length=1)
    
    
class TaskUpdate(BaseModel):
    title : str | None = None
    done : bool | None = None

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
    return tasks


@app.get("/tasks/{id}")
def get_task(id: int):
    for task in tasks:
        if task["id"] == id:
            return task

    raise HTTPException(
        status_code=404,
        detail=f"Task {id} not found"
    )
    
    
@app.post("/tasks",status_code=201)
def create_task(task:Taskcreate):
    new_id = max([task['id'] for task in tasks],default=0)+1
    
    new_task={
        "id":new_id,
        "title":task.title,
        "done":False
    }
    
    tasks.append(new_task)
    
    return new_task



@app.put("/tasks/{id}")
def update_task(id: int, task_update: TaskUpdate):
    for task in tasks:
        if task["id"] == id:

            if task_update.title is not None:
                if not task_update.title.strip():
                    raise HTTPException(
                        status_code=400,
                        detail="Title cannot be empty"
                    )

                task["title"] = task_update.title

            if task_update.done is not None:
                task["done"] = task_update.done

            return task

    raise HTTPException(
        status_code=404,
        detail=f"Task {id} not found"
    )


@app.delete("/tasks/{id}", status_code=204)
def delete_task(id: int):
    for index, task in enumerate(tasks):
        if task["id"] == id:
            tasks.pop(index)
            return

    raise HTTPException(
        status_code=404,
        detail=f"Task {id} not found"
    )