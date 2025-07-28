from task import Task
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/tasks")
async def get_tasks():
    return {"data": Task.tasks}

@app.get("/tasks/{id}")
async def get_task_by_id(id):
    id = int(id)
    return {"data": Task.get_by_id(id)}

@app.post("/tasks")
async def post_task():
    t = Task()
    task = Task.get_by_id(t.id)
    return {"data": task}

@app.delete("/tasks/{id}")
async def delete_task_by_id(id: str):
    return {"message": Task.delete_by_id(id)}