#file:test_pawpal.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from datetime import datetime
from pawpal_system import Pet, Task, Scheduler


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


def test_sort_by_time_returns_chronological_order():
    scheduler = Scheduler()
    pet = Pet(id="p1", name="Buddy", species="Dog", breed="Labrador", age=3)

    t1 = Task(id="t1", title="Evening Walk", type="exercise", due_date=datetime(2026, 4, 1, 18, 0))
    t2 = Task(id="t2", title="Morning Feed", type="feeding",  due_date=datetime(2026, 4, 1,  7, 0))
    t3 = Task(id="t3", title="Noon Meds",   type="medicine", due_date=datetime(2026, 4, 1, 12, 0))

    scheduler.schedule_task(pet, t1)
    scheduler.schedule_task(pet, t2)
    scheduler.schedule_task(pet, t3)

    sorted_tasks = scheduler.sort_by_time()

    assert sorted_tasks[0].title == "Morning Feed"
    assert sorted_tasks[1].title == "Noon Meds"
    assert sorted_tasks[2].title == "Evening Walk"


def test_complete_and_recur_creates_next_day_task():
    scheduler = Scheduler()
    pet = Pet(id="p1", name="Buddy", species="Dog", breed="Labrador", age=3)

    task = Task(
        id="t1", title="Morning Feed", type="feeding",
        due_date=datetime(2026, 4, 1, 8, 0), frequency="daily"
    )
    scheduler.schedule_task(pet, task)
    scheduler.complete_and_recur(pet, task)

    assert task.is_completed is True

    next_tasks = [t for _, t in scheduler.task_queue if not t.is_completed]
    assert len(next_tasks) == 1
    assert next_tasks[0].due_date == datetime(2026, 4, 2, 8, 0)


def test_conflict_detection_flags_tasks_within_15_minutes():
    scheduler = Scheduler()
    pet = Pet(id="p1", name="Buddy", species="Dog", breed="Labrador", age=3)

    t1 = Task(id="t1", title="Bath Time", type="grooming", due_date=datetime(2026, 4, 1, 10, 0))
    t2 = Task(id="t2", title="Vet Visit",  type="vet",      due_date=datetime(2026, 4, 1, 10, 10))

    scheduler.schedule_task(pet, t1)
    warnings = scheduler.check_conflicts(t2, pet_id="p1")

    assert len(warnings) == 1
    assert "Vet Visit" in warnings[0]


def test_no_conflict_when_tasks_are_far_apart():
    scheduler = Scheduler()
    pet = Pet(id="p1", name="Buddy", species="Dog", breed="Labrador", age=3)

    t1 = Task(id="t1", title="Morning Feed", type="feeding", due_date=datetime(2026, 4, 1,  8, 0))
    t2 = Task(id="t2", title="Evening Walk", type="exercise", due_date=datetime(2026, 4, 1, 18, 0))

    scheduler.schedule_task(pet, t1)
    warnings = scheduler.check_conflicts(t2, pet_id="p1")

    assert warnings == []
