class taskmanager:
    def __init__(self):
        self.task = []
        self.next_id = 1
    def add_task(self, task_name: str):
        task_item = {"id":self.next_id,"name":task_name,"completed":False}
        self.task.append(task_item)
        self.next_id += 1
        return task_item
    def remove_task(self, task_id: int):
        for task in self.task:
            if task["id"] == task_id:
                self.task.remove(task)
                return {"status": "Task removed successfully", "task": task}
        return {"error": f"Task ID {task_id} not found"}
    def list_tasks(self):
        return self.task
    def completed(self, task_id: int):
        for task in self.task:
            if task["id"] == task_id:
                task["completed"] = True
                return task
        return {"error": f"Task ID {task_id} not found"}


