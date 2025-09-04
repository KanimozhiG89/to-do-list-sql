from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from db import get_connection, init_db
import sqlite3

app = FastAPI()
init_db()

class TodoIn(BaseModel):
    title: str
    description: str

class TodoUpdate(TodoIn):
    done: bool  

class TodoOut(TodoIn):
    id: int
    done: bool

@app.post("/todos", response_model=TodoOut)
def add_todo(todo: TodoIn):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO todos (title, description) VALUES (?, ?)',
        (todo.title, todo.description)
    )
    conn.commit()
    todo_id = cursor.lastrowid
    conn.close()
    
    return {**todo.model_dump(), "id": todo_id, "done": False}

@app.get("/todos", response_model=list[TodoOut])
def list_todos():
    conn = get_connection()
    conn.row_factory = sqlite3.Row 
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM todos')
    rows = cursor.fetchall()
    conn.close()

    
    return [
        {
            "id": row["id"],
            "title": row["title"],
            "description": row["description"],
            "done": bool(row["done"])
        }
        for row in rows
    ]

@app.put("/todos/{todo_id}", response_model=TodoOut)
def update_todo(todo_id: int, todo: TodoUpdate):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE todos SET title=?, description=?, done=? WHERE id=?',
        (todo.title, todo.description, int(todo.done), todo_id)
    )
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Todo not found")
    conn.commit()
    conn.close()

    return {**todo.model_dump(), "id": todo_id}

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM todos WHERE id=?', (todo_id,))
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Todo not found")
    conn.commit()
    conn.close()
    return {"detail": "Todo deleted"}
