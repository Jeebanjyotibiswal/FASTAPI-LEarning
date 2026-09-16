import enum

from fastapi import FastAPI
from pydantic import BaseModel
app=FastAPI()
################### Curd operation  ###############
class Todo(BaseModel):
    id:int
    title:str
    completed:bool
todos=[]
#data create
@app.post("/todos")
def create_todos(todo:Todo):
    todos.append(todo)
    return {
        "message":"Todos created successfully",
        "data":todo
    }
#read based on id
@app.get("/todos{todo_id}")
def get_todo(todo_id:int):
    for i in todos:
        if i.id==todo_id:
            return i
    return {"error":"Todos Not found"}

#update
@app.put("/todos{todo_id}")
def todo_update(todo_id:int,update_todo:Todo):
    for i,j in enumerate(todos):
        if j.id==todo_id:
            todos[i]=update_todo
            return {
                "message":"todos updated sucessfully"
            }
    return {"error":"Todos Not Found"}

#partial upadte
@app.patch("/todos{todo_id}")
def todo_partial_update(todo_id:int,update_todo:Todo):
    for i,j in enumerate(todos):
        if j.id==todo_id:
            todos[i].title=update_todo.title
            todos[i].completed=update_todo.completed
            return {
                "message":"todos updated sucessfully"
            }
    return {"error":"Todos Not Found"}

#delete
@app.delete("/todos{todo_id}")
def remove_todo(todo_id:int):
    for i,j  in enumerate(todos):
        if j.id==todo_id:
            todos.pop(i)
            return {
                "mesage":"Deleted Suceswsfully"
            }
    return{
        "error":"Data not found"
    }
