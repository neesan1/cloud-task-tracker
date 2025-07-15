from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'tasks.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Task {self.id}>'

# Create DB tables
with app.app_context():
    db.create_all()

# Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/tasks")
def show_tasks():
    tasks = Task.query.all()
    return render_template("tasks.html", tasks=tasks)

@app.route("/add-task", methods=["POST"])
def add_task():
    content = request.form.get("task")
    if content:
        new_task = Task(content=content)
        db.session.add(new_task)
        db.session.commit()
    return redirect(url_for("show_tasks"))

@app.route("/delete-task/<int:id>")
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("show_tasks"))

if __name__ == "__main__":
    app.run(debug=True)
