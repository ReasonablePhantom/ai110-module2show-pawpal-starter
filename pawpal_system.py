from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    description: str
    duration: int        # minutes
    priority: str        # "high" / "medium" / "low"
    is_completed: bool = field(default=False)
    time: str = field(default="08:00")      # "HH:MM" 24-hour format
    frequency: str = field(default="once")  # "once" | "daily"

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.is_completed = True


@dataclass
class Pet:
    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Append a task to this pet's task list."""
        self.tasks.append(task)


@dataclass
class Owner:
    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Append a pet to this owner's pet list."""
        self.pets.append(pet)

    def get_all_tasks(self) -> List[Task]:
        """Return a flat list of all tasks across all owned pets."""
        return [task for pet in self.pets for task in pet.tasks]


class Scheduler:
    def __init__(self, owner: Owner) -> None:
        self.owner = owner

    def generate_daily_plan(self) -> List[Task]:
        """Retrieve all tasks from the owner and return them as the daily plan."""
        return self.owner.get_all_tasks()

    def sort_by_time(self) -> List[Task]:
        """Return all tasks sorted chronologically by their scheduled time."""
        return sorted(self.owner.get_all_tasks(), key=lambda t: t.time)

    def filter_by_completion(self, completed: bool) -> List[Task]:
        """Return tasks matching the given completion status across all pets."""
        return [t for t in self.owner.get_all_tasks() if t.is_completed == completed]

    def filter_by_pet(self, pet_name: str) -> List[Task]:
        """Return all tasks belonging to the named pet, or [] if not found."""
        pet = next((p for p in self.owner.pets if p.name == pet_name), None)
        return pet.tasks if pet else []

    def advance_daily_tasks(self) -> List[Task]:
        """Add a fresh next-day copy for every completed daily task; return the new tasks."""
        new_tasks = []
        for pet in self.owner.pets:
            for task in list(pet.tasks):  # snapshot so we don't iterate over newly added tasks
                if task.is_completed and task.frequency == "daily":
                    next_task = Task(
                        description=task.description,
                        duration=task.duration,
                        priority=task.priority,
                        time=task.time,
                        frequency=task.frequency,
                    )
                    pet.add_task(next_task)
                    new_tasks.append(next_task)
        return new_tasks

    def detect_conflicts(self) -> List[str]:
        """Return warning strings for any two tasks on the same pet scheduled at the same time."""
        warnings = []
        for pet in self.owner.pets:
            seen: dict = {}
            for task in pet.tasks:
                if task.time in seen:
                    warnings.append(
                        f"Conflict for {pet.name}: '{task.description}' and "
                        f"'{seen[task.time].description}' both at {task.time}"
                    )
                else:
                    seen[task.time] = task
        return warnings
