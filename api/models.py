class Task():
    _tasks = []
    _max_id: int = 0

    def __init__(self, title: str):
        self.id: int = Task._max_id + 1
        self.title: str = title
        self.completed: bool = False

        Task._max_id += 1
        Task._tasks.append(self)

    @classmethod
    def get_by_id(cls, id: int):
        for task in cls._tasks:
            if task.id == id:
                return task
            
        return None
    
    @classmethod
    def update(cls, id: int, title: str, completed: bool):
        old_task = cls.get_by_id(id)
        if not old_task:
            return None
       
        return old_task.change_attr(title,completed)

    @classmethod
    def delete_by_id(cls, id: int):
        task = Task.get_by_id(id)
        if task:
            cls._tasks.remove(task)
            return True
        else:
            return False

    @classmethod
    def get_all(cls):
        return cls._tasks
    
    def change_attr(self, title: str, completed: bool):
        self.title = title if title != None else self.title
        self.completed = completed if completed != None else self.completed

        return self