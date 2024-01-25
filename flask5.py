# Необходимо создать API для управления списком задач. Каждая задача должна содержать заголовок и описание. Для каждой задачи должна быть возможность указать статус (выполнена/не выполнена).
#
# API должен содержать следующие конечные точки:
# — GET /tasks — возвращает список всех задач.
# — GET /tasks/{id} — возвращает задачу с указанным идентификатором.
# — POST /tasks — добавляет новую задачу.
# — PUT /tasks/{id} — обновляет задачу с указанным идентификатором.
# — DELETE /tasks/{id} — удаляет задачу с указанным идентификатором.
#
# Для каждой конечной точки необходимо проводить валидацию данных запроса и ответа. Для этого использовать библиотеку Pydantic.

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict

app = FastAPI()


# Модель для описания задачи
class Task(BaseModel):
    title: str
    description: str
    status: bool


# База данных для хранения задач
db: Dict[int, Task] = {}


# Генератор идентификатора задачи
def get_next_task_id() -> int:
    return max(db.keys(), default=0) + 1


# Получение списка всех задач
@app.get("/tasks")
def get_tasks():
    return db.values()


# Получение задачи по идентификатору
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    if task_id not in db:
        raise HTTPException(status_code=404, detail="Task not found")
    return db[task_id]


# Добавление новой задачи
@app.post("/tasks")
def create_task(task: Task):
    task_id = get_next_task_id()
    db[task_id] = task
    return {"task_id": task_id}


# Обновление задачи по идентификатору
@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task):
    if task_id not in db:
        raise HTTPException(status_code=404, detail="Task not found")
    db[task_id] = task
    return {"task_id": task_id}


# Удаление задачи по идентификатору
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    if task_id not in db:
        raise HTTPException(status_code=404, detail="Task not found")
    del db[task_id]
    return {"message": "Task deleted"}
