class Task():
    tasks = []
    max_id: int = 0

    def __init__(self):
        self.id: int = Task.max_id + 1
        Task.max_id += 1

        Task.tasks.append(self)

    def get_by_id(id: int):
        for task in Task.tasks:
            if task.id == id:
                return task
            
        return "Task not found"
    
    def delete_by_id(id):
        try:
            Task.tasks.remove(Task.get_by_id(id))
            return "Task deleted"
        except:
            return "Task not found"
