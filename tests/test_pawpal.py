from pawpal_system import Task, Pet


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
