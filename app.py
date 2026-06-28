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
        col1, col2 = st.columns(2)
        with col1:
            duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
            time = st.text_input("Time (HH:MM)", value="08:00")
        with col2:
            priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
            frequency = st.selectbox("Frequency", ["once", "daily"])
        task_submitted = st.form_submit_button("Add Task")

    if task_submitted and description.strip():
        pet = next(p for p in pets if p.name == selected)
        pet.add_task(Task(
            description=description.strip(),
            duration=int(duration),
            priority=priority,
            time=time.strip(),
            frequency=frequency,
        ))
        st.success(f"Task added to {selected}!")
else:
    st.info("Add a pet first before scheduling tasks.")

st.divider()

# --- Daily Schedule ---
st.subheader("Daily Schedule")
owner = st.session_state.owner
all_tasks = owner.get_all_tasks()

if all_tasks:
    scheduler = Scheduler(owner=owner)

    # Conflict warnings
    for warning in scheduler.detect_conflicts():
        st.warning(warning)

    # Sorted task table
    sorted_tasks = scheduler.sort_by_time()

    # Header row
    h = st.columns([1, 3, 2, 2, 2, 2])
    h[0].markdown("**Time**")
    h[1].markdown("**Task**")
    h[2].markdown("**Pet**")
    h[3].markdown("**Duration**")
    h[4].markdown("**Priority**")
    h[5].markdown("**Status**")
    st.divider()

    for i, task in enumerate(sorted_tasks):
        pet_owner = next(p for p in owner.pets if task in p.tasks)
        cols = st.columns([1, 3, 2, 2, 2, 2])
        cols[0].write(task.time)
        cols[1].write(task.description)
        cols[2].write(pet_owner.name)
        cols[3].write(f"{task.duration} min")
        cols[4].write(task.priority)
        if task.is_completed:
            cols[5].write("Done ✓")
        else:
            if cols[5].button("✓ Complete", key=f"complete_{i}"):
                task.mark_complete()
                scheduler.advance_daily_tasks()
                st.rerun()
else:
    st.info("No tasks yet — add a pet and some tasks above.")
