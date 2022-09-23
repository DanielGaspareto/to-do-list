"""Code initialization."""
from todo_list.main import app, db

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
