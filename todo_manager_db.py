import sqlite3
from datetime import datetime
from pathlib import Path

class TodoManagerDB:
    def __init__(self, db_name="todos.db"):
        self.db_path = Path(db_name)
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self._create_table()
    
    def _create_table(self):
        """Создает таблицу, если она еще не существует"""
        # SQL-запрос для создания таблицы
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL,
                priority TEXT DEFAULT 'medium',
                created TEXT NOT NULL,
                done INTEGER DEFAULT 0
            )
        ''')
        self.conn.commit()
    
    def add_task(self, task: str, priority: str = "medium"):
        """Добавляет новую задачу в БД"""
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # ВАЖНО: Мы используем (?, ?, ?) вместо f-строк!
        # Это защищает от SQL-инъекций. База данных сама экранирует значения.
        self.cursor.execute('''
            INSERT INTO tasks (task, priority, created, done)
            VALUES (?, ?, ?, 0)
        ''', (task, priority, created_at))
        
        self.conn.commit()
        print(f"✅ Задача добавлена в БД: {task}")
    
    def show_tasks(self):
        """Показывает все задачи из БД"""
        self.cursor.execute('SELECT id, task, priority, created, done FROM tasks')
        rows = self.cursor.fetchall()
        
        if not rows:
            print("📋 Список задач пуст")
            return
        
        print("\n Твои задачи (из БД):")
        print("-" * 50)
        for row in rows:
            task_id, task, priority, created, done = row
            status = "✅" if done else "⬜"
            print(f"{status} [ID:{task_id}] [{priority}] {task}")
            print(f"   Создана: {created}")
        print("-" * 50)
    
    def complete_task(self, task_id: int):
        """Отмечает задачу как выполненную через UPDATE"""
        self.cursor.execute('''
            UPDATE tasks SET done = 1 WHERE id = ?
        ''', (task_id,))
        
        if self.cursor.rowcount > 0:
            self.conn.commit()
            print(f"✅ Задача ID {task_id} выполнена!")
        else:
            print("❌ Задача с таким ID не найдена")

    def __del__(self):
        """Закрываем соединение при удалении объекта"""
        self.conn.close()

def main():
    manager = TodoManagerDB()
    
    while True:
        print("\n МЕНЕДЖЕР ЗАДАЧ (SQLite Edition)")
        print("1. Добавить задачу")
        print("2. Показать задачи")
        print("3. Выполнить задачу")
        print("4. Выход")
        
        choice = input("\nВыбери действие (1-4): ")
        
        if choice == "1":
            task = input("Введи задачу: ")
            priority = input("Приоритет (low/medium/high): ") or "medium"
            manager.add_task(task, priority)
        elif choice == "2":
            manager.show_tasks()
        elif choice == "3":
            try:
                task_id = int(input("ID задачи для выполнения: "))
                manager.complete_task(task_id)
            except ValueError:
                print("❌ ID должен быть числом!")
        elif choice == "4":
            print("👋 До встречи!")
            break
        else:
            print("❌ Неверный выбор")

if __name__ == "__main__":
    main()