from api.models import Task
from api.schemas import *
from fastapi import FastAPI
from fastapi import HTTPException
import sqlite3

app = FastAPI()

def create_tasks_table():
    with Task.get_db() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                completed BOOLEAN)
            """)
        
@app.on_event("startup")
def startup_event():
    create_tasks_table()

@app.get("/")
async def root():
    return {"status": "ok"}

@app.get("/tasks")
async def get_tasks():
    return Task.get_all()

@app.get("/tasks/{id}", response_model=TaskOut)
async def get_task_by_id(id: int):
    task = Task.get_by_id(id)
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.post("/tasks", response_model=TaskOut)
async def post_task(task: TaskCreate):
    new_task = Task.create(title=task.title)
    return new_task

@app.put("/tasks/{id}", response_model=TaskOut)
async def put_task(id: int, task: TaskUpdate):
    updated = Task.update(id, task.title, task.completed)
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return updated

@app.patch("/tasks/{id}", response_model=TaskOut)
async def patch_task(id: int, task: TaskOptional):
    updated = Task.update(id, task.title, task.completed)
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return updated

@app.delete("/tasks/{id}")
async def delete_task_by_id(id: int):
    task = Task.get_by_id(id)
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    deleted = Task.delete_by_id(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not deleted")
    return {"status": "ok"}