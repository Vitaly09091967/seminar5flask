from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Модель задачи
class Task(BaseModel):
    title: str
    description: str
    status: bool

# База данных задач
tasks_db = []

# Получение списка всех задач
@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return tasks_db

# Получение задачи по ID
@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    task = next((task for task in tasks_db if task.get("id") == task_id), None)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task

# Добавление новой задачи
@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(task: Task):
    task_data = task.dict()
    task_data["id"] = len(tasks_db) + 1
    tasks_db.append(task_data)
    return task_data

# Обновление задачи по ID
@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task: Task):
    task_idx = next((idx for idx, t in enumerate(tasks_db) if t.get("id") == task_id), None)
    if task_idx is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    tasks_db[task_idx] = {"id": task_id, **task.dict()}
    return tasks_db[task_idx]

# Удаление задачи по ID
@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    task_idx = next((idx for idx, t in enumerate(tasks_db) if t.get("id") == task_id), None)
    if task_idx is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    del tasks_db[task_idx]

# Запуск сервера
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
