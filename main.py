from pawpal_system import Task, Pet, Owner, Scheduler

owner = Owner(name="Alex")

biscuit = Pet(name="Biscuit", species="Dog")
biscuit.add_task(Task(description="Morning Walk", duration=30, priority="high"))
biscuit.add_task(Task(description="Feeding", duration=10, priority="high"))

whiskers = Pet(name="Whiskers", species="Cat")
whiskers.add_task(Task(description="Grooming", duration=15, priority="medium"))

owner.add_pet(biscuit)
owner.add_pet(whiskers)

scheduler = Scheduler(owner=owner)
plan = scheduler.generate_daily_plan()

print(f"Today's Schedule for {owner.name}")
print("=" * 30)

for pet in owner.pets:
    print(f"\nPet: {pet.name} ({pet.species})")
    for task in pet.tasks:
        status = "[done]" if task.is_completed else f"[{task.priority}]"
        print(f"  - {task.description:<20} {task.duration:>3} min  {status}")

print(f"\nTotal tasks: {len(plan)}")
