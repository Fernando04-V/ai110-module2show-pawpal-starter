from dataclasses import dataclass, field
from datetime import datetime


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
        now = datetime.now()
        return [t for t in self.tasks if not t.is_completed and t.due_date >= now]

    def update_health_status(self, status: str):
        self.health_status = status


class Owner:
    def __init__(self, id: str, name: str, email: str, phone: str):
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone
        self.pets = []

    def add_pet(self, pet: Pet):
        self.pets.append(pet)

    def remove_pet(self, pet_id: str):
        self.pets = [p for p in self.pets if p.id != pet_id]

    def get_pets(self):
        return self.pets


@dataclass
class Task:
    id: str
    title: str
    type: str  # e.g. "feeding", "grooming", "vet visit"
    due_date: datetime
    notes: str = ""
    is_completed: bool = False

    def complete(self):
        self.is_completed = True

    def reschedule(self, new_date: datetime):
        self.due_date = new_date

    def is_overdue(self) -> bool:
        return not self.is_completed and datetime.now() > self.due_date


class Scheduler:
    def __init__(self):
        self.task_queue = []

    def schedule_task(self, pet: Pet, task: Task):
        pet.tasks.append(task)
        self.task_queue.append((pet.id, task))

    def cancel_task(self, task_id: str):
        self.task_queue = [(pid, t) for pid, t in self.task_queue if t.id != task_id]

    def get_tasks_due_today(self):
        today = datetime.now().date()
        return [t for _, t in self.task_queue if t.due_date.date() == today and not t.is_completed]

    def get_tasks_for_pet(self, pet_id: str):
        return [t for pid, t in self.task_queue if pid == pet_id]

    def send_reminder(self, task: Task):
        print(f"Reminder: '{task.title}' is due on {task.due_date.strftime('%Y-%m-%d %H:%M')}")
