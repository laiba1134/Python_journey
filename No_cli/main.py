from fastapi import FastAPI
from pydantic import BaseModel
from task_manager import taskmanager

app = FastAPI()
manager = taskmanager()

# Pydantic schema for task creation
class TaskCreate(BaseModel):
    name: str
# --- Add a new task ---
@app.post("/tasks")
def add_task(task: TaskCreate):
    return manager.add_task(task.name)

# --- List all tasks ---
@app.get("/tasks")
def list_tasks():
    return manager.list_tasks()

# --- Mark a task as complete ---
@app.put("/tasks/{task_id}/complete")
def complete_task(task_id: int):
    return manager.complete_task(task_id)

# --- Delete a task ---
@app.delete("/tasks/{task_id}")
def remove_task(task_id: int):
    return manager.remove_task(task_id)
