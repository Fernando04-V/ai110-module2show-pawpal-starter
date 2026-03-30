from dataclasses import dataclass, field
from datetime import datetime, timedelta

# Maps a task's frequency string to the timedelta until its next occurrence.
# timedelta(days=1)  -> adds exactly 24 hours (one calendar day)
# timedelta(weeks=1) -> adds exactly 7 days
# timedelta(days=30) -> approximation for monthly recurrence
FREQUENCY_DELTAS = {
    "daily":   timedelta(days=1),
    "weekly":  timedelta(weeks=1),
    "monthly": timedelta(days=30),
}


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

    def check_conflicts(self, task: Task, pet_id: str = None, window_minutes: int = 15) -> list[str]:
        """Check whether a task overlaps with already-scheduled tasks and return warnings.

        Lightweight and non-blocking — always returns a list of strings rather
        than raising an exception, so callers decide how to handle conflicts.
        Completed tasks are ignored since they no longer occupy time slots.

        Args:
            task:           The new Task being evaluated before scheduling.
            pet_id:         Scope the check to a single pet by passing their ID
                            (e.g. "p1"). Pass None to check across ALL pets,
                            which is useful for shared-resource conflicts.
            window_minutes: Minimum required gap in minutes between any two tasks
                            (default 15). Tasks closer than this threshold trigger
                            a warning.

        Returns:
            A list of human-readable warning strings describing each conflict.
            Returns an empty list when no conflicts are found.

        Example:
            warnings = scheduler.check_conflicts(new_task, pet_id="p1")
            warnings = scheduler.check_conflicts(new_task, pet_id=None)  # cross-pet
        """
        warnings = []
        window = timedelta(minutes=window_minutes)

        for pid, existing in self.task_queue:
            if existing.is_completed:
                continue
            if pet_id is not None and pid != pet_id:
                continue

            gap = abs(existing.due_date - task.due_date)
            if gap < window:
                warnings.append(
                    f"WARNING: '{task.title}' ({task.due_date.strftime('%I:%M %p')}) "
                    f"conflicts with '{existing.title}' ({existing.due_date.strftime('%I:%M %p')}) "
                    f"— only {int(gap.total_seconds() // 60)} min apart."
                )

        return warnings

    def schedule_task(self, pet: Pet, task: Task):
        """Add a task to a pet and register it in the scheduler queue.

        Runs a conflict check first and prints any warnings, but always
        proceeds with scheduling so the program never crashes.
        """
        conflicts = self.check_conflicts(task, pet_id=pet.id)
        for warning in conflicts:
            print(warning)

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

    def sort_by_time(self, tasks: list = None) -> list:
        """Return a new list of tasks sorted ascending by due_date.

        Non-destructive — the original list or queue is never modified.

        Args:
            tasks: An optional list of Task objects to sort. When omitted,
                   sorts every task currently in the scheduler queue.

        Returns:
            A new list of Task objects ordered earliest to latest by due_date.

        Example:
            scheduler.sort_by_time()
            scheduler.sort_by_time(scheduler.filter_tasks(pet_name="p1"))
        """
        source = tasks if tasks is not None else [t for _, t in self.task_queue]
        return sorted(source, key=lambda t: t.due_date)

    def filter_tasks(self, pet_name: str = None, status: str = None) -> list:
        """Filter the task queue by pet ID and/or completion status.

        Both parameters are optional and combinable. When both are provided,
        only tasks matching both criteria are returned.

        Args:
            pet_name: The pet's ID string (e.g. "p1") to scope results to one
                      pet. Case-insensitive. Pass None to include all pets.
            status:   Completion filter — one of:
                        "pending"   — incomplete, not yet overdue or still future
                        "completed" — marked done via task.complete()
                        "overdue"   — incomplete and past their due_date
                      Pass None to skip status filtering entirely.

        Returns:
            A flat list of Task objects matching all provided criteria.
            Returns all tasks when both arguments are None.

        Example:
            scheduler.filter_tasks(status="pending")
            scheduler.filter_tasks(pet_name="p2", status="overdue")
        """
        result = self.task_queue

        if pet_name is not None:
            result = [(pid, t) for pid, t in result if pid.lower() == pet_name.lower()]

        if status == "completed":
            result = [(pid, t) for pid, t in result if t.is_completed]
        elif status == "pending":
            result = [(pid, t) for pid, t in result if not t.is_completed]
        elif status == "overdue":
            result = [(pid, t) for pid, t in result if t.is_overdue()]

        return [t for _, t in result]

    def complete_and_recur(self, pet: Pet, task: Task):
        """Mark a task complete and auto-schedule its next occurrence for recurring tasks.

        Uses Python's timedelta to calculate the next due date from the current
        due_date (not from "now"), so timing stays consistent even if called late:
          - "daily"   -> due_date + timedelta(days=1)
          - "weekly"  -> due_date + timedelta(weeks=1)
          - "monthly" -> due_date + timedelta(days=30)
          - "once"    -> marked complete only, no follow-up task created

        The generated next task inherits all fields (title, type, description,
        notes, frequency) from the original and is immediately added to the
        scheduler queue via schedule_task(), which also runs conflict detection.

        Args:
            pet:  The Pet the task belongs to. Required so the new occurrence
                  can be registered against the same pet in the queue.
            task: The Task to complete. Must already exist in the scheduler queue.

        Example:
            scheduler.complete_and_recur(buddy, morning_feed)
        """
        task.complete()

        delta = FREQUENCY_DELTAS.get(task.frequency)
        if delta is None:
            return  # 'once' tasks — nothing to recur

        next_due = task.due_date + delta
        next_task = Task(
            id=f"{task.id}_next",
            title=task.title,
            type=task.type,
            due_date=next_due,
            description=task.description,
            frequency=task.frequency,
            notes=task.notes,
        )
        self.schedule_task(pet, next_task)

    def send_reminder(self, task: Task):
        """Print a reminder message for the given task."""
        print(f"Reminder: '{task.title}' is due on {task.due_date.strftime('%Y-%m-%d %H:%M')}")
