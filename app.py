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
        st.session_state.scheduler.schedule_task(pet, task)
        st.success(f"'{task_title}' scheduled for {selected_pet_name} at {task_time.strftime('%I:%M %p')}!")
else:
    st.info("Add a pet above before scheduling tasks.")

st.divider()

# ── Today's Schedule ───────────────────────────────────────────────
st.subheader("Today's Schedule")

if st.button("Generate Schedule"):
    due_today = sorted(
        st.session_state.scheduler.get_tasks_due_today(),
        key=lambda t: t.due_date
    )
    if not due_today:
        st.info("No tasks scheduled for today.")
    else:
        for task in due_today:
            status = "✅" if task.is_completed else "🔲"
            time_str = task.due_date.strftime("%I:%M %p")
            st.markdown(f"{status} **{time_str}** — {task.title} `{task.type}`")
            if task.description:
                st.caption(task.description)
