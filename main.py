from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional


from database import engine, Base, get_db
import models
import schemas

app = FastAPI(title="TaskMetrics API")

#Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "TaskMetrics API corriendo dentro de Docker con DB conectada"}

@app.post("/tasks", response_model=schemas.TaskResponse, status_code=201)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    db_task = models.Task(
        title=task.title,
        description=task.description,
        priority=task.priority
    )
    db.add(db_task) 
    db.commit()     
    db.refresh(db_task) 
    return db_task

@app.get("/tasks", response_model=List[schemas.TaskResponse])
def get_tasks(
    completed: Optional[bool] = None, 
    priority: Optional[str] = None, 
    db: Session = Depends(get_db)
):
    query = db.query(models.Task)
    if completed is not None:
        query = query.filter(models.Task.completed == completed)
    if priority is not None:
        query = query.filter(models.Task.priority == priority)
    tasks = query.all()
    return tasks

@app.get("/tasks/metrics", response_model=schemas.TaskMetricsResponse)
def get_task_metrics(db: Session = Depends(get_db)):
    total = db.query(models.Task).count()
    if total == 0:
        return {
            "total_tasks": 0,
            "completed_tasks": 0,
            "pending_tasks": 0,
            "completion_percentage": 0.0,
            "by_priority": {"low": 0, "medium": 0, "high": 0}
        }

    completed = db.query(models.Task).filter(models.Task.completed == True).count()
    pending = total - completed
    percentage = round((completed / total) * 100, 2)
    priority_counts = db.query(
        models.Task.priority, 
        func.count(models.Task.id)
    ).group_by(models.Task.priority).all()
    by_priority = {"low": 0, "medium": 0, "high": 0}
    for priority, count in priority_counts:
        by_priority[priority] = count
        
    return {
        "total_tasks": total,
        "completed_tasks": completed,
        "pending_tasks": pending,
        "completion_percentage": percentage,
        "by_priority": by_priority
    }

@app.put("/tasks/{task_id}", response_model=schemas.TaskResponse)
def update_task(task_id: int, task_data: schemas.TaskUpdate, db: Session = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    
    if not db_task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    for key, value in task_data.model_dump(exclude_unset=True).items():
        setattr(db_task, key, value)
        
    db.commit()
    db.refresh(db_task)
    return db_task

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    
    if not db_task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")    
    db.delete(db_task) 
    db.commit()        
    return None        

