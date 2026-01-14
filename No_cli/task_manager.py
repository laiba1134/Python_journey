import json
import os

class taskmanager:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = []
        self.next_id = 1
        self.load_tasks()  # Load tasks from JSON file

    def save_tasks(self):
        with open(self.filename, "w") as f:
            json.dump(self.tasks, f, indent=4)

    def load_tasks(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                self.tasks = json.load(f)
            # Set next_id to one higher than the highest existing task id
            if self.tasks:
                self.next_id = max(task["id"] for task in self.tasks) + 1

    def add_task(self, task_name: str):
        task_item = {"id": self.next_id, "name": task_name, "completed": False}
        self.tasks.append(task_item)
        self.next_id += 1
        self.save_tasks()  # Save immediately
        return task_item

    def remove_task(self, task_id: int):
        for task in self.tasks:
            if task["id"] == task_id:
                self.tasks.remove(task)
                self.save_tasks()
                return {"status": "success", "message": f"Task {task_id} removed."}
        return {"status": "error", "message": f"Task {task_id} not found."}

    def list_tasks(self):
        return self.tasks

    def complete_task(self, task_id: int):
        for task in self.tasks:
            if task["id"] == task_id:
                task["completed"] = True
                self.save_tasks()
                return task
        return {"status": "error", "message": f"Task {task_id} not found."}