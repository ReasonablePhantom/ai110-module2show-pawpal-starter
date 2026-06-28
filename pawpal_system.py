from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    description: str
    duration: int        # minutes
    priority: str        # "high" / "medium" / "low"
    is_completed: bool = field(default=False)

    def mark_complete(self) -> None:
        pass


@dataclass
class Pet:
    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass


@dataclass
class Owner:
    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        pass

    def get_all_tasks(self) -> List[Task]:
        pass


class Scheduler:
    def __init__(self, owner: Owner) -> None:
        self.owner = owner

    def generate_daily_plan(self) -> List[Task]:
        pass

    def sort_tasks(self) -> List[Task]:
        pass
