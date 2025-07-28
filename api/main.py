from task import Task
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/tasks")
async def get_tasks():
    return Task.tasks

@app.get("/tasks/{id}")
async def get_task_by_id(id):
    return Task.search_by_id(id)

@app.post("/tasks")
async def post_task():
    return Task()

@app.delete("/tasks/{id}")
async def delete_task(id):
    Task.delete_task_by_id(id)
    return {"message": "Task Deleted"}