from pawpal_system import Task, Pet, Owner, Scheduler


def test_task_completion():
    task = Task(description="Walk", duration=30, priority="high")
    assert task.is_completed is False
    task.mark_complete()
    assert task.is_completed is True


def test_add_task_to_pet():
    pet = Pet(name="Biscuit", species="Dog")
    assert len(pet.tasks) == 0
    pet.add_task(Task(description="Feeding", duration=10, priority="high"))
    assert len(pet.tasks) == 1


def test_sort_by_time():
    owner = Owner(name="Test")
    pet = Pet(name="Rover", species="Dog")
    pet.add_task(Task(description="Dinner",  duration=10, priority="high",   time="18:00"))
    pet.add_task(Task(description="Walk",    duration=30, priority="high",   time="07:00"))
    pet.add_task(Task(description="Midday",  duration=15, priority="medium", time="12:00"))
    owner.add_pet(pet)
    result = Scheduler(owner=owner).sort_by_time()
    assert [t.time for t in result] == ["07:00", "12:00", "18:00"]


def test_advance_daily_tasks():
    owner = Owner(name="Test")
    pet = Pet(name="Rover", species="Dog")
    task = Task(description="Morning Walk", duration=30, priority="high",
                time="07:00", frequency="daily")
    pet.add_task(task)
    owner.add_pet(pet)
    task.mark_complete()
    new_tasks = Scheduler(owner=owner).advance_daily_tasks()
    assert len(new_tasks) == 1
    assert new_tasks[0].description == "Morning Walk"
    assert new_tasks[0].is_completed is False
    assert len(pet.tasks) == 2


def test_detect_conflicts():
    owner = Owner(name="Test")
    pet = Pet(name="Rover", species="Dog")
    pet.add_task(Task(description="Walk",    duration=30, priority="high", time="07:00"))
    pet.add_task(Task(description="Feeding", duration=10, priority="high", time="07:00"))
    owner.add_pet(pet)
    warnings = Scheduler(owner=owner).detect_conflicts()
    assert len(warnings) == 1
    assert "07:00" in warnings[0]
