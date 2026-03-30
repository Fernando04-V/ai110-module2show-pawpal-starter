import streamlit as st
from datetime import datetime, time
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

# --- Session state init ---
if "owner" not in st.session_state:
    st.session_state.owner = None

if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler()

# ── Owner & Pet Setup ──────────────────────────────────────────────
st.subheader("Owner & Pet")

owner_name = st.text_input("Owner name", value="Jordan")
pet_name   = st.text_input("Pet name",   value="Mochi")
pet_breed  = st.text_input("Breed",      value="Mixed")
pet_age    = st.number_input("Age (years)", min_value=0, max_value=30, value=2)
species    = st.selectbox("Species", ["Dog", "Cat", "Other"])

if st.button("Add Pet"):
    if st.session_state.owner is None:
        st.session_state.owner = Owner(
            id="o1", name=owner_name, email="", phone=""
        )
    pet = Pet(
        id=f"p{len(st.session_state.owner.get_pets()) + 1}",
        name=pet_name,
        species=species,
        breed=pet_breed,
        age=int(pet_age),
    )
    st.session_state.owner.add_pet(pet)
    st.success(f"{pet_name} added to {owner_name}'s pets!")

if st.session_state.owner:
    pets = st.session_state.owner.get_pets()
    if pets:
        st.write("**Current pets:**", ", ".join(p.name for p in pets))

st.divider()

# ── Schedule a Task ────────────────────────────────────────────────
st.subheader("Schedule a Task")

if st.session_state.owner and st.session_state.owner.get_pets():
    pet_options = {p.name: p for p in st.session_state.owner.get_pets()}
    selected_pet_name = st.selectbox("Assign to pet", list(pet_options.keys()))

    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        task_type = st.selectbox("Type", ["feeding", "grooming", "exercise", "vet visit", "other"])
    with col3:
        frequency = st.selectbox("Frequency", ["once", "daily", "weekly", "monthly"])

    task_desc = st.text_input("Description (optional)", value="")
    task_time = st.time_input("Due time (today)", value=time(8, 0))
    due_date  = datetime.combine(datetime.now().date(), task_time)

    if st.button("Schedule Task"):
        pet  = pet_options[selected_pet_name]
        task = Task(
            id=f"t{len(st.session_state.scheduler.task_queue) + 1}",
            title=task_title,
            type=task_type,
            due_date=due_date,
            description=task_desc,
            frequency=frequency,
        )

        # Run conflict check before scheduling and surface warnings in the UI
        conflicts = st.session_state.scheduler.check_conflicts(task, pet_id=pet.id)
        for warning in conflicts:
            st.warning(warning)

        st.session_state.scheduler.schedule_task(pet, task)
        st.success(f"'{task_title}' scheduled for {selected_pet_name} at {task_time.strftime('%I:%M %p')}!")
else:
    st.info("Add a pet above before scheduling tasks.")

st.divider()

# ── Today's Schedule ───────────────────────────────────────────────
st.subheader("Today's Schedule")

# Filter controls
col_pet, col_status = st.columns(2)
with col_pet:
    filter_pet = st.selectbox(
        "Filter by pet",
        ["All pets"] + (
            [p.name for p in st.session_state.owner.get_pets()]
            if st.session_state.owner else []
        ),
    )
with col_status:
    filter_status = st.selectbox(
        "Filter by status",
        ["all", "pending", "completed", "overdue"],
    )

if st.button("Generate Schedule"):
    scheduler = st.session_state.scheduler

    # Resolve pet_id for filter (None = all pets)
    pet_id = None
    if filter_pet != "All pets" and st.session_state.owner:
        matched = [p for p in st.session_state.owner.get_pets() if p.name == filter_pet]
        if matched:
            pet_id = matched[0].id

    status_arg = None if filter_status == "all" else filter_status
    filtered = scheduler.filter_tasks(pet_name=pet_id, status=status_arg)

    # Scope to today only
    today = datetime.now().date()
    today_tasks = [t for t in filtered if t.due_date.date() == today]

    # Sort using Scheduler.sort_by_time()
    sorted_tasks = scheduler.sort_by_time(today_tasks)

    if not sorted_tasks:
        st.info("No tasks match the selected filters for today.")
    else:
        # Build a table-friendly list of dicts
        rows = []
        for task in sorted_tasks:
            if task.is_completed:
                status_label = "Completed"
            elif task.is_overdue():
                status_label = "Overdue"
            else:
                status_label = "Pending"

            rows.append({
                "Time": task.due_date.strftime("%I:%M %p"),
                "Task": task.title,
                "Type": task.type,
                "Frequency": task.frequency,
                "Status": status_label,
                "Description": task.description or "—",
            })

        st.table(rows)

        # Summary counts
        n_done    = sum(1 for t in sorted_tasks if t.is_completed)
        n_overdue = sum(1 for t in sorted_tasks if t.is_overdue())
        n_pending = len(sorted_tasks) - n_done - n_overdue

        c1, c2, c3 = st.columns(3)
        c1.metric("Pending",   n_pending)
        c2.metric("Completed", n_done)
        c3.metric("Overdue",   n_overdue)

        if n_overdue:
            st.error(f"{n_overdue} overdue task(s) need attention!")
        elif n_done == len(sorted_tasks):
            st.success("All tasks for today are complete!")
