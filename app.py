import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan")

st.title("🐾 PawPal+")

# --- Owner ---
st.subheader("Owner")
owner_name = st.text_input("Your name", value=st.session_state.owner.name)
st.session_state.owner.name = owner_name

st.divider()

# --- Add Pet ---
st.subheader("Add a Pet")
with st.form("add_pet_form"):
    pet_name = st.text_input("Pet name")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    pet_submitted = st.form_submit_button("Add Pet")

if pet_submitted and pet_name.strip():
    st.session_state.owner.add_pet(Pet(name=pet_name.strip(), species=species))
    st.success(f"Added {pet_name.strip()}!")

if st.session_state.owner.pets:
    st.write("**Your pets:**", ", ".join(p.name for p in st.session_state.owner.pets))

st.divider()

# --- Schedule Task ---
st.subheader("Schedule a Task")
pets = st.session_state.owner.pets

if pets:
    with st.form("add_task_form"):
        selected = st.selectbox("Pet", [p.name for p in pets])
        description = st.text_input("Task description", value="Morning walk")
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
        task_submitted = st.form_submit_button("Add Task")

    if task_submitted and description.strip():
        pet = next(p for p in pets if p.name == selected)
        pet.add_task(Task(description=description.strip(), duration=int(duration), priority=priority))
        st.success(f"Task added to {selected}!")
else:
    st.info("Add a pet first before scheduling tasks.")

st.divider()

# --- Daily Schedule ---
st.subheader("Daily Schedule")
all_tasks = st.session_state.owner.get_all_tasks()

if all_tasks:
    scheduler = Scheduler(owner=st.session_state.owner)
    plan = scheduler.generate_daily_plan()
    rows = [
        {
            "Task": t.description,
            "Duration (min)": t.duration,
            "Priority": t.priority,
            "Done": t.is_completed,
        }
        for t in plan
    ]
    st.table(rows)
else:
    st.info("No tasks yet — add a pet and some tasks above.")
