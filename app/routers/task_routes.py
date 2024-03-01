from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session as DBSession
from app.models.task import Session as TaskSession
from app.schemas.validation import Task
from app.repos.task_crud import create_task, get_all_tasks, get_task, update_task, delete_task

task_router = APIRouter()

def get_db():
    db = TaskSession()
    try:
        yield db
    finally:
        db.close()

@task_router.post("/task/create_task")
def create_task_endpoint(task_data: Task, db: DBSession = Depends(get_db)):
    try:
        return create_task(session=db, task_data=task_data)
    except Exception as e:
        print(e)

        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")


@task_router.get("/task/get_task/{task_id}")
def get_task_endpoint(task_id: int, db: DBSession = Depends(get_db)):
    try:
        return get_task(session=db, task_id=task_id)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    

@task_router.get("/task/get_all_tasks/{user_id}")
def get_task_endpoint(user_id: int, db: DBSession = Depends(get_db)):
    try:
        return get_all_tasks(session=db, user_id=user_id)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@task_router.put("/task/update_task/{task_id}")
def update_task_endpoint(task_id: int, task_data: dict, db: DBSession = Depends(get_db)):
    try:
        updated_task = update_task(session=db, task_id=task_id, task_data=task_data)
        if updated_task:
            return {"message": "Task updated successfully", "updated_task": updated_task}
        else:
            raise HTTPException(status_code=404, detail="Task not found")
    except Exception as e:
        print(e)

        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")

    

@task_router.delete("/task/delete_task/{task_id}")
def delete_task_endpoint(task_id: int, db: DBSession = Depends(get_db)):
    try:
        return delete_task(session=db, task_id=task_id)
    except Exception as e:
        print(e)
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")