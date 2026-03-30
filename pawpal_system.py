from dataclasses import dataclass, field
from datetime import datetime


#file:pawpal_system.py

@dataclass
class Pet:
    id: str
    name: str
    species: str
    breed: str
    age: int
    health_status: str = "healthy"
    tasks: list = field(default_factory=list)

    def get_upcoming_tasks(self):
        """Return all incomplete tasks with a future due date."""
        now = datetime.now()
        return [t for t in self.tasks if not t.is_completed and t.due_date >= now]

    def update_health_status(self, status: str):
        """Update the pet's current health status."""
        self.health_status = status


class Owner:
    def __init__(self, id: str, name: str, email: str, phone: str):
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone
        self.pets = []

    def add_pet(self, pet: Pet):
        """Add a pet to this owner's list."""
        self.pets.append(pet)

    def remove_pet(self, pet_id: str):
        """Remove a pet from this owner's list by id."""
        self.pets = [p for p in self.pets if p.id != pet_id]

    def get_pets(self):
        """Return all pets belonging to this owner."""
        return self.pets

    def get_all_tasks(self):
        """Return a flat list of every task across all owned pets."""
        return [task for pet in self.pets for task in pet.tasks]


@dataclass
class Task:
    id: str
    title: str
    type: str  # e.g. "feeding", "grooming", "vet visit"
    due_date: datetime
    description: str = ""
    frequency: str = "once"  # e.g. "once", "daily", "weekly", "monthly"
    notes: str = ""
    is_completed: bool = False

    def complete(self):
        """Mark this task as completed."""
        self.is_completed = True

    def reschedule(self, new_date: datetime):
        """Update the task's due date to a new datetime."""
        self.due_date = new_date

    def is_overdue(self) -> bool:
        """Return True if the task is past due and not yet completed."""
        return not self.is_completed and datetime.now() > self.due_date


class Scheduler:
    def __init__(self):
        self.task_queue = []

    def schedule_task(self, pet: Pet, task: Task):
        """Add a task to a pet and register it in the scheduler queue."""
        pet.tasks.append(task)
        self.task_queue.append((pet.id, task))

    def cancel_task(self, task_id: str):
        """Remove a task from the scheduler queue by task id."""
        self.task_queue = [(pid, t) for pid, t in self.task_queue if t.id != task_id]

    def get_tasks_due_today(self):
        """Return all incomplete tasks scheduled for today."""
        today = datetime.now().date()
        return [t for _, t in self.task_queue if t.due_date.date() == today and not t.is_completed]

    def get_tasks_for_pet(self, pet_id: str):
        """Return all tasks in the queue belonging to a specific pet."""
        return [t for pid, t in self.task_queue if pid == pet_id]

    def get_overdue_tasks(self):
        """Return all tasks that are past due and not completed."""
        return [t for _, t in self.task_queue if t.is_overdue()]

    def get_tasks_by_frequency(self, frequency: str):
        """Return all tasks matching a given frequency (e.g. 'daily')."""
        return [t for _, t in self.task_queue if t.frequency == frequency]

    def send_reminder(self, task: Task):
        """Print a reminder message for the given task."""
        print(f"Reminder: '{task.title}' is due on {task.due_date.strftime('%Y-%m-%d %H:%M')}")
