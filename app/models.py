import os
import sqlite3
from contextlib import contextmanager

from dotenv import load_dotenv

load_dotenv()


class Task:
    DB_NAME = os.getenv("TASKS_DB_NAME")
    _max_id: int = 0

    def __init__(self, id: int, title: str, completed: bool):
        self.id = id
        self.title = title
        self.completed = completed

    @classmethod
    def create(cls, title: str):
        with cls.get_db() as cursor:
            cursor.execute(
                "INSERT INTO tasks (title, completed) VALUES (?, ?)", (title, False)
            )
            new_id = cursor.lastrowid
        return cls(new_id, title, False)

    @classmethod
    def set_db_name(cls, name):
        cls.DB_NAME = name

    @staticmethod
    @contextmanager
    def get_db():
        conn = sqlite3.connect(Task.DB_NAME)
        cursor = conn.cursor()
        try:
            yield cursor
            conn.commit()
        except:
            conn.rollback()
            raise
        finally:
            conn.close()

    @classmethod
    def get_by_id(cls, id: int):
        with cls.get_db() as cursor:
            cursor.execute("SELECT * FROM tasks WHERE id = ?", (id,))
            row = cursor.fetchone()

        if row is None:
            return None
        task = cls(row[0], row[1], row[2])

        return task

    @classmethod
    def update(cls, id: int, title: str = None, completed: bool = None):
        with cls.get_db() as cursor:
            if title is not None:
                cursor.execute("UPDATE tasks SET title = ? WHERE id = ?", (title, id))
            if completed is not None:
                cursor.execute(
                    "UPDATE tasks SET completed = ? WHERE id = ?", (completed, id)
                )

        task = cls.get_by_id(id)

        return task

    @classmethod
    def delete_by_id(cls, id: int):
        task = cls.get_by_id(id)

        if task:
            with cls.get_db() as cursor:
                cursor.execute("DELETE FROM tasks WHERE id = ?", (task.id,))

            return True
        else:
            return False

    @classmethod
    def get_all(cls):
        with cls.get_db() as cursor:
            cursor.execute("SELECT * FROM tasks")
            tasks = cursor.fetchall()

        if tasks is None:
            return None

        res = []
        for row in tasks:
            res.append(cls(row[0], row[1], row[2]))

        return res
