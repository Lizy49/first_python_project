import json
from datetime import datetime
from pathlib import Path

class TodoManager:
    def __init__(self, filename="todos.json"):
        self.filename = Path(filename)
        self.todos = self.load_todos()
    
    def load_todos(self):
        """Загружает задачи из файла"""
        if self.filename.exists():
            with open(self.filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def save_todos(self):
        """Сохраняет задачи в файл"""
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.todos, f, ensure_ascii=False, indent=2)
    
    def add_task(self, task: str, priority: str = "medium"):
        """Добавляет новую задачу"""
        todo = {
            "id": len(self.todos) + 1,
            "task": task,
            "priority": priority,
            "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "done": False
        }
        self.todos.append(todo)
        self.save_todos()
        print(f"✅ Задача добавлена: {task}")
    
    def show_tasks(self):
        """Показывает все задачи"""
        if not self.todos:
            print("📋 Список задач пуст")
            return
        
        print("\n Твои задачи:")
        print("-" * 50)
        for todo in self.todos:
            status = "✅" if todo["done"] else "⬜"
            print(f"{status} [{todo['priority']}] {todo['task']}")
            print(f"   Создана: {todo['created']}")
        print("-" * 50)
    
    def complete_task(self, task_id: int):
        """Отмечает задачу как выполненную"""
        for todo in self.todos:
            if todo["id"] == task_id:
                todo["done"] = True
                self.save_todos()
                print(f"✅ Задача выполнена: {todo['task']}")
                return
        print("❌ Задача не найдена")

def main():
    manager = TodoManager()
    
    while True:
        print("\n МЕНЕДЖЕР ЗАДАЧ")
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
            task_id = int(input("ID задачи для выполнения: "))
            manager.complete_task(task_id)
        
        elif choice == "4":
            print("👋 До встречи!")
            break
        
        else:
            print("❌ Неверный выбор")

if __name__ == "__main__":
    main()