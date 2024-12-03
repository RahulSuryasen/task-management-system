from flask import Flask, request, jsonify, render_template
from flask_cors import CORS  # To handle CORS issues
import sqlite3

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend-backend communication

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        due_date TEXT,
        status TEXT
    )
    ''')
    conn.commit()
    conn.close()

# Serve the frontend
@app.route('/')
def index():
    return render_template('index.html')  # Ensure this file exists in the `templates` folder

# Create a new task
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    if not all(k in data for k in ('title', 'description', 'due_date', 'status')):
        return jsonify({'message': 'Missing required fields'}), 400

    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("INSERT INTO tasks (title, description, due_date, status) VALUES (?, ?, ?, ?)",
              (data['title'], data['description'], data['due_date'], data['status']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Task created successfully'}), 201

# Get all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    conn = sqlite3.connect('tasks.db')
    conn.row_factory = sqlite3.Row  # Convert rows to dictionary format
    c = conn.cursor()
    c.execute("SELECT * FROM tasks")
    tasks = [dict(row) for row in c.fetchall()]
    conn.close()
    return jsonify({'tasks': tasks})

# Update a task
@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    data = request.get_json()
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("UPDATE tasks SET title=?, description=?, due_date=?, status=? WHERE id=?",
              (data['title'], data['description'], data['due_date'], data['status'], id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Task updated successfully'})

# Delete a task
@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Task deleted successfully'})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
