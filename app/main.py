import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI(
    title="Todo REST API",
    description="DevOps Lab Assignment REST API - Course 25CIAEC59",
    version="1.0.0"
)

class TodoItem(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = ""
    completed: bool = False

todos_db: List[TodoItem] = []

@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    """Health check endpoint for Kubernetes probes and monitoring."""
    return {"status": "healthy", "service": "todo-api", "version": "1.0.0"}

@app.get("/todos", response_model=List[TodoItem], status_code=status.HTTP_200_OK)
def get_todos():
    """Retrieve all todo items."""
    return todos_db

@app.post("/todos", response_model=TodoItem, status_code=status.HTTP_201_CREATED)
def create_todo(todo: TodoItem):
    """Create a new todo item."""
    next_id = len(todos_db) + 1
    new_todo = TodoItem(
        id=next_id,
        title=todo.title,
        description=todo.description,
        completed=todo.completed
    )
    todos_db.append(new_todo)
    return new_todo

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", os.getenv("APP_PORT", "8000")))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=False)
