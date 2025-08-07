import uvicorn
from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager

from app.models import Task
from app.schemas import TaskCreate, TaskOptional, TaskOut, TaskUpdate


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tasks_table()
    yield


app = FastAPI(lifespan=lifespan)


def create_tasks_table(db: str = None):
    with Task.get_db(db) as cursor:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                completed BOOLEAN)
            """
        )


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
    return {"status": "ok", "data": new_task}


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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
