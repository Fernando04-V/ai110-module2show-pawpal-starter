#file:test_pawpal.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from datetime import datetime
from pawpal_system import Pet, Task


def test_task_completion():
    task = Task(
        id="t1", title="Feed Buddy",
        type="feeding", due_date=datetime(2026, 3, 29, 8, 0)
    )
    assert task.is_completed is False
    task.complete()
    assert task.is_completed is True


def test_task_addition_increases_pet_task_count():
    pet = Pet(id="p1", name="Buddy", species="Dog", breed="Labrador", age=3)
    assert len(pet.tasks) == 0

    task = Task(
        id="t1", title="Morning Walk",
        type="exercise", due_date=datetime(2026, 3, 29, 9, 0)
    )
    pet.tasks.append(task)
    assert len(pet.tasks) == 1
