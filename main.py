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
    
    new_id={
        "id":new_id,
        "title":task.title,
        "done":False
    }
    
    tasks.append(new_id)
    
    return new_id