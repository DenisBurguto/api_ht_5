import datetime
from fastapi import FastAPI
from pydantic import BaseModel


class Task(BaseModel):
    task_id: int
    task_name: str
    description: str
    performed: bool = False
    created_at: datetime.datetime = datetime.datetime.now()


tasks = []

app = FastAPI()


@app.get('/tasks/')
async def return_tasks():
    return tasks


@app.get('/tasks/{task_id}')
async def return_tasks_id(task_id: int):
    for task in tasks:
        if task_id == task.task_id:
            return task
    return {'detail': f'Task with id {task_id} not found'}, 404


"""
curl -X 'POST' 'http://127.0.0.1:8000/tasks/1' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{"task_id": 1 ,"task_name": "FirsTask", "description": "Complete home task #4"}'
"""


@app.post('/tasks/')
async def create_task(task: Task):
    for old_task in tasks:
        if task.task_id == old_task.task_id:
            return {f'{task.task_id} already exists, use PUT to update it'}, 409
    tasks.append(task)
    return {f'{task.task_name} successfully created'}


"""
curl -X 'PUT' 'http://127.0.0.1:8000/tasks/1' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{"task_id": 1 ,"task_name": "FirsTask", "description": "Complete home task #4", "performed": true}'
"""


@app.put('/tasks/{task_id}')
async def update_task(task_id: int, new_task: Task):
    for i, task in enumerate(tasks):
        if task_id == task.task_id:
            tasks[i] = new_task
            return {f'{new_task.task_name} successfully updated'}
    return {'detail': f'Task with id {task_id} not found'}, 404


"""
curl -X 'DELETE' 'http://127.0.0.1:8000/tasks/1' -H 'accept: application/json'
"""


@app.delete('/tasks/{task_id}')
async def delete_task(task_id: int):
    for task in tasks:
        if task_id == task.task_id:
            tasks.remove(task)
            return {f'{task.task_name} successfully deleted'}
    return {'detail': f'Task with id {task_id} not found'}, 404
