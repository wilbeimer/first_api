class Task():
    tasks = []
    max_id = 0

    def __init__(self):
        self.id = Task.max_id + 1

        Task.tasks.append(self)

    def get_task_by_id(id):
        for task in Task.tasks:
            if task.id == id:
                return task

        return LookupError("Task not found")
    
    def delete_task_by_id(id):
        try:
            Task.tasks.remove(id)
        except:
            return LookupError("Task not found")
