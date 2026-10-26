from flask import Flask, render_template_string, request, redirect, url_for
import sqlite3
from datetime import datetime
from pathlib import Path

app = Flask(__name__)
DB_PATH = Path("todos.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Создает таблицу, если её нет"""
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            priority TEXT DEFAULT 'medium',
            created TEXT NOT NULL,
            done INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()


HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Менеджер задач</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background: #f5f5f5;
        }
        h1 { color: #333; }
        .task {
            background: white;
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .task.done { opacity: 0.6; text-decoration: line-through; }
        .priority-high { border-left: 4px solid #e74c3c; }
        .priority-medium { border-left: 4px solid #f39c12; }
        .priority-low { border-left: 4px solid #27ae60; }
        form {
            background: white;
            padding: 20px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        input, select, button {
            padding: 10px;
            margin: 5px;
            border: 1px solid #ddd;
            border-radius: 3px;
        }
        button {
            background: #3498db;
            color: white;
            border: none;
            cursor: pointer;
        }
        button:hover { background: #2980b9; }
    </style>
</head>
<body>
    <h1>📋 Менеджер задач</h1>
    
    <form method="POST" action="/add">
        <input type="text" name="task" placeholder="Новая задача" required>
        <select name="priority">
            <option value="low">Низкий</option>
            <option value="medium" selected>Средний</option>
            <option value="high">Высокий</option>
        </select>
        <button type="submit">Добавить</button>
    </form>
    
    {% for task in tasks %}
    <div class="task {{ 'done' if task.done }} priority-{{ task.priority }}">
        <strong>{{ task.task }}</strong>
        <span style="color: #888;">[{{ task.priority }}]</span>
        <br>
        <small>Создана: {{ task.created }}</small>
        {% if not task.done %}
            <form method="POST" action="/complete/{{ task.id }}" style="display: inline; margin-left: 10px;">
                <button type="submit" style="background: #27ae60;">Выполнить</button>
            </form>
        {% endif %}
    </div>
    {% endfor %}
</body>
</html>
'''

@app.route('/')
def index():
    """Главная страница - показывает все задачи"""
    conn = get_db()
    tasks = conn.execute('SELECT * FROM tasks ORDER BY id DESC').fetchall()
    conn.close()
    return render_template_string(HTML_TEMPLATE, tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    """Добавляет новую задачу"""
    task = request.form['task']
    priority = request.form['priority']
    created = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    conn = get_db()
    # Параметризованный запрос - защита от SQL-инъекций
    conn.execute('INSERT INTO tasks (task, priority, created, done) VALUES (?, ?, ?, 0)',
                 (task, priority, created))
    conn.commit()
    conn.close()
    
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>', methods=['POST'])
def complete_task(task_id):
    """Отмечает задачу как выполненную"""
    conn = get_db()
    conn.execute('UPDATE tasks SET done = 1 WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    # Запускаем сервер на порту 5000
    # host='0.0.0.0' означает, что сервер доступен не только локально
    app.run(host='0.0.0.0', port=5000, debug=True)

