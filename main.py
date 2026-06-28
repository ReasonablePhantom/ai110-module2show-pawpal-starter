from pawpal_system import Task, Pet, Owner, Scheduler

# --- Setup ---
owner = Owner(name="Alex")

biscuit = Pet(name="Biscuit", species="Dog")
whiskers = Pet(name="Whiskers", species="Cat")

# Tasks added out of order; Biscuit has two tasks at 07:00 (deliberate conflict)
biscuit.add_task(Task(description="Evening Feeding", duration=10, priority="high",  time="18:00", frequency="once"))
biscuit.add_task(Task(description="Morning Walk",    duration=30, priority="high",  time="07:00", frequency="daily"))
biscuit.add_task(Task(description="Vet Checkup",     duration=45, priority="medium",time="07:00", frequency="once"))

whiskers.add_task(Task(description="Playtime",  duration=20, priority="low",    time="09:30", frequency="once"))
whiskers.add_task(Task(description="Grooming",  duration=15, priority="medium", time="08:00", frequency="daily"))

owner.add_pet(biscuit)
owner.add_pet(whiskers)

scheduler = Scheduler(owner=owner)


def section(title: str) -> None:
    print(f"\n{'=' * 40}")
    print(f"  {title}")
    print('=' * 40)

def print_tasks(tasks) -> None:
    for t in tasks:
        status = "[done]" if t.is_completed else f"[{t.priority}]"
        print(f"  {t.time}  {t.description:<20} {t.duration:>3} min  {status}  ({t.frequency})")


# 1. Sorted schedule (tasks added out of order above)
section("Sorted by Time")
print_tasks(scheduler.sort_by_time())

# 2. Mark Morning Walk complete
biscuit.tasks[1].mark_complete()  # index 1 = Morning Walk

# 3. Filter — incomplete tasks only
section("Incomplete Tasks")
print_tasks(scheduler.filter_by_completion(completed=False))

# 4. Filter — Whiskers only
section("Whiskers' Tasks")
print_tasks(scheduler.filter_by_pet("Whiskers"))

# 5. Conflict detection
section("Conflict Detection")
conflicts = scheduler.detect_conflicts()
if conflicts:
    for warning in conflicts:
        print(f"  WARNING: {warning}")
else:
    print("  No conflicts detected.")

# 6. Advance daily tasks (create next-day copies for completed daily tasks)
section("Advance Daily Tasks")
new_tasks = scheduler.advance_daily_tasks()
print(f"  {len(new_tasks)} new daily task(s) created:")
for t in new_tasks:
    print(f"    - {t.description} ({t.time}, is_completed={t.is_completed})")
