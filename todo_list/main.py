"""This project is a simple to-do list."""
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.sqlite3"

db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    task = db.Column(db.String(300))
    days = db.Column(db.Integer)

    def __int__(self, task, days):
        self.task = task
        self.days = days


@app.route('/')
def index():
    """
    Home page, here the user can see tasks.

    :return: index.html
    """
    todo = Todo.query.all()
    return render_template('index.html', todo=todo)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """
    Here the user can create tasks.

    :return: add.html or index function whit url_for.
    """

    if request.method == 'POST':
        if request.form['task'] == "":
            return redirect(url_for('index'))
        else:
            todo = Todo(task=request.form['task'], days=request.form['days'])
            db.session.add(todo)
            db.session.commit()
            return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<int:id>')
def delete(id):
    """
    In front is a button that deletes a task.

    param id: Task id to search in db and delete.
    :return: index function whit url_for.
    """
    todo = Todo.query.get(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    """
    Here the user can edit an existing  task.

    param id: Task id to search in db and edit.
    :return: edit.html or index function whit url_for.
    """
    todo = Todo.query.get(id)
    if request.method == 'POST':
        todo.task = request.form['task']
        todo.days = request.form['days']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', todo=todo)


# if __name__ == '__main__':
#     db.create_all()
#     app.run(debug=True)
