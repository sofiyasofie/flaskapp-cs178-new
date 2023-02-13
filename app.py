# Using this tutorial: https://dev.to/nditah/develop-a-simple-python-flask-todo-app-in-1-minute-2mjm

# Partner (for 2/13/23 helping w debugging in class): Sam Osa-Agbontaen
# Help with debugging in this file from Felix Perez Diener

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#https://flask.palletsprojects.com/en/2.2.x/appcontext/
with app.app_context():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)

    class Todo(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(100))
        complete = db.Column(db.Boolean)

    db.create_all()

# Concept #1: Routing
@app.get("/")
# Concept #3: Functions for different functionalities within app
def home():
    todo_list = db.session.query(Todo).all()
    # Concept #2: Render_template for an html file
    return render_template("base.html", todo_list=todo_list)

@app.post("/add")
def add():
    # Concept #1 similar: Javascript request form similarity
    title = request.form.get("title")
    new_todo = Todo(title=title, complete=False)
    # Concept #2 similar: database manipulation
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("home"))

@app.get("/update/<int:todo_id>")
def update(todo_id):
    # Concept #3 similar: SQL queries
    todo = db.session.query(Todo).filter(Todo.id == todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("home"))

@app.get("/delete/<int:todo_id>")
def delete(todo_id):
    todo = db.session.query(Todo).filter(Todo.id == todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))
