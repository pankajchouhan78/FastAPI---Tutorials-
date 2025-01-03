from fastapi import FastAPI
app = FastAPI()

from db_connect import session
from models import Todo

@app.get("/")
def home():
    return {"message": "First FastAPI app"}

@app.get('/greet/')
def greet():
    return {"message": "Hello, World!"}

@app.post("/create")
async def create_todo(text: str, is_complete: bool = False):
    todo = Todo(text=text, is_done=is_complete)
    session.add(todo)
    session.commit()
    return {"todo added": todo.text}

@app.get('/todos/')
async def get_all_todos():
    todos = session.query(Todo).all()
    return {"todos": todos}

@app.put('/update/{id}')
async def update_todo(id: int, newtext: str="", is_complete:bool=False):
    todo_query = session.query(Todo).filter(Todo.id==id)
    if todo_query.first():
        todo = todo_query.first()
        if newtext:
            todo.text = newtext
        todo.is_done=is_complete
        
        session.add(todo)
        session.commit()
        return {"todo updated": {'Text':todo.text , 'Is Completed': todo.is_done}}
    else:
        return {"error": "Todo not found"}
    
@app.delete('/delete/{id}')
async def delete_todo(id: int):
    todo_query = session.query(Todo).get(id)
    session.delete(todo_query)
    session.commit()
    return {"message": "Todo deleted"}
    