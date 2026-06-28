from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    description: str
    duration: int        # minutes
    priority: str        # "high" / "medium" / "low"
    is_completed: bool = field(default=False)

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

    def sort_tasks(self) -> List[Task]:
        """Sort tasks by priority; not yet implemented."""
        pass
