#file:main.py
from datetime import datetime
from pawpal_system import Owner, Pet, Task, Scheduler

# --- Setup ---
owner = Owner(id="o1", name="Alex Rivera", email="alex@email.com", phone="555-1234")

buddy = Pet(id="p1", name="Buddy",  species="Dog", breed="Labrador",   age=3)
luna  = Pet(id="p2", name="Luna",   species="Cat", breed="Siamese",    age=5)

owner.add_pet(buddy)
owner.add_pet(luna)

# --- Tasks (using today's date with different times) ---
today = datetime.now().date()

tasks = [
    Task(
        id="t1", title="Morning Feed",
        type="feeding", due_date=datetime(today.year, today.month, today.day, 8, 0),
        description="Give Buddy his morning kibble", frequency="daily"
    ),
    Task(
        id="t2", title="Midday Walk",
        type="exercise", due_date=datetime(today.year, today.month, today.day, 12, 30),
        description="30-minute walk around the block", frequency="daily"
    ),
    Task(
        id="t3", title="Luna's Grooming",
        type="grooming", due_date=datetime(today.year, today.month, today.day, 15, 0),
        description="Brush Luna's coat and clean ears", frequency="weekly"
    ),
    Task(
        id="t4", title="Evening Feed",
        type="feeding", due_date=datetime(today.year, today.month, today.day, 18, 0),
        description="Evening meal for both pets", frequency="daily"
    ),
]

scheduler = Scheduler()
scheduler.schedule_task(buddy, tasks[0])  # Morning Feed    -> Buddy
scheduler.schedule_task(buddy, tasks[1])  # Midday Walk     -> Buddy
scheduler.schedule_task(luna,  tasks[2])  # Luna's Grooming -> Luna
scheduler.schedule_task(luna,  tasks[3])  # Evening Feed    -> Luna

# --- Today's Schedule ---
print("=" * 40)
print("       PAWPAL+ TODAY'S SCHEDULE")
print("=" * 40)
print(f"Owner : {owner.name}")
print(f"Pets  : {', '.join(p.name for p in owner.get_pets())}")
print("-" * 40)

due_today = sorted(scheduler.get_tasks_due_today(), key=lambda t: t.due_date)

if not due_today:
    print("No tasks scheduled for today.")
else:
    for task in due_today:
        status = "✓" if task.is_completed else "○"
        time   = task.due_date.strftime("%I:%M %p")
        print(f"  {status}  {time}  |  {task.title} ({task.type})")
        if task.description:
            print(f"           {task.description}")

print("=" * 40)
