#file:main.py
#codebase
from datetime import datetime
from pawpal_system import Owner, Pet, Task, Scheduler

# --- Setup ---
owner = Owner(id="o1", name="Alex Rivera", email="alex@email.com", phone="555-1234")

buddy = Pet(id="p1", name="Buddy",  species="Dog", breed="Labrador",   age=3)
luna  = Pet(id="p2", name="Luna",   species="Cat", breed="Siamese",    age=5)

owner.add_pet(buddy)
owner.add_pet(luna)

# --- Tasks added OUT OF ORDER intentionally ---
today = datetime.now().date()

tasks = [
    Task(
        id="t1", title="Evening Feed",
        type="feeding", due_date=datetime(today.year, today.month, today.day, 18, 0),
        description="Evening meal for both pets", frequency="daily"
    ),
    Task(
        id="t2", title="Morning Feed",
        type="feeding", due_date=datetime(today.year, today.month, today.day, 8, 0),
        description="Give Buddy his morning kibble", frequency="daily"
    ),
    Task(
        id="t3", title="Luna's Grooming",
        type="grooming", due_date=datetime(today.year, today.month, today.day, 15, 0),
        description="Brush Luna's coat and clean ears", frequency="weekly"
    ),
    Task(
        id="t4", title="Midday Walk",
        type="exercise", due_date=datetime(today.year, today.month, today.day, 12, 30),
        description="30-minute walk around the block", frequency="daily"
    ),
    # Conflict task: same time as Morning Feed (08:00) for Buddy
    Task(
        id="t5", title="Flea Treatment",
        type="grooming", due_date=datetime(today.year, today.month, today.day, 8, 0),
        description="Apply monthly flea treatment", frequency="monthly"
    ),
    # Near-conflict task: 10 min after Morning Feed, within the 15-min window
    Task(
        id="t6", title="Morning Weigh-In",
        type="other", due_date=datetime(today.year, today.month, today.day, 8, 10),
        description="Check Buddy's weight", frequency="weekly"
    ),
]

print("=" * 40)
print("    SCHEDULING TASKS")
print("    (conflicts print as warnings)")
print("=" * 40)

scheduler = Scheduler()
scheduler.schedule_task(buddy, tasks[0])  # Evening Feed   -> Buddy  (18:00) - no conflict
scheduler.schedule_task(buddy, tasks[1])  # Morning Feed   -> Buddy  (08:00) - no conflict yet
scheduler.schedule_task(luna,  tasks[2])  # Grooming       -> Luna   (15:00) - no conflict
scheduler.schedule_task(luna,  tasks[3])  # Midday Walk    -> Luna   (12:30) - no conflict
scheduler.schedule_task(buddy, tasks[4])  # Flea Treatment -> Buddy  (08:00) - EXACT conflict with t2
scheduler.schedule_task(buddy, tasks[5])  # Morning Weigh  -> Buddy  (08:10) - NEAR conflict with t2/t5

# Mark one task completed to test status filtering
tasks[1].complete()  # Morning Feed is done

# ── 1. Sorted Schedule ─────────────────────────────────────────────
print("\n" + "=" * 40)
print("    SORTED SCHEDULE (all tasks)")
print("=" * 40)
for task in scheduler.sort_by_time():
    status = "[x]" if task.is_completed else "[ ]"
    time_str = task.due_date.strftime("%I:%M %p")
    print(f"  {status}  {time_str}  |  {task.title} ({task.type})")

# ── 2. Filter: Pending tasks only ─────────────────────────────────
print("\n" + "=" * 40)
print("    FILTER: Pending tasks")
print("=" * 40)
for task in scheduler.filter_tasks(status="pending"):
    print(f"  [ ]  {task.due_date.strftime('%I:%M %p')}  |  {task.title}")

# ── 3. Filter: Completed tasks only ───────────────────────────────
print("\n" + "=" * 40)
print("    FILTER: Completed tasks")
print("=" * 40)
for task in scheduler.filter_tasks(status="completed"):
    print(f"  [x]  {task.due_date.strftime('%I:%M %p')}  |  {task.title}")

# ── 4. Filter: Buddy's tasks only (sorted) ────────────────────────
print("\n" + "=" * 40)
print("    FILTER: Buddy's tasks (sorted)")
print("=" * 40)
for task in scheduler.sort_by_time(scheduler.filter_tasks(pet_name="p1")):
    status = "[x]" if task.is_completed else "[ ]"
    print(f"  {status}  {task.due_date.strftime('%I:%M %p')}  |  {task.title}")

# ── 5. Filter: Luna's tasks only (sorted) ─────────────────────────
print("\n" + "=" * 40)
print("    FILTER: Luna's tasks (sorted)")
print("=" * 40)
for task in scheduler.sort_by_time(scheduler.filter_tasks(pet_name="p2")):
    status = "[x]" if task.is_completed else "[ ]"
    print(f"  {status}  {task.due_date.strftime('%I:%M %p')}  |  {task.title}")

print("=" * 40)
