# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

(.venv) brucelyu@BruceLyudeMacBook-Pro-4 ai110-module2show-pawpal-starter % python main.py 
Today's Schedule for Alex
==============================

Pet: Biscuit (Dog)
  - Morning Walk          30 min  [high]
  - Feeding               10 min  [high]

Pet: Whiskers (Cat)
  - Grooming              15 min  [medium]

Total tasks: 3

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
============================= test session starts ==============================
platform darwin -- Python 3.13.13, pytest-9.0.3, pluggy-1.6.0
rootdir: /Users/brucelyu/Desktop/AI110/ai110-module2show-pawpal-starter
collected 5 items

tests/test_pawpal.py::test_task_completion PASSED                        [ 20%]
tests/test_pawpal.py::test_add_task_to_pet PASSED                        [ 40%]
tests/test_pawpal.py::test_sort_by_time PASSED                           [ 60%]
tests/test_pawpal.py::test_advance_daily_tasks PASSED                    [ 80%]
tests/test_pawpal.py::test_detect_conflicts PASSED                       [100%]

============================== 5 passed in 0.02s ===============================
```

**Reliability confidence: ★★★★☆ (4/5)**

Core behaviors (task completion, pet/task relationships, chronological sorting, daily recurrence, exact-time conflict detection) are all covered by passing tests. The main gap is that conflict detection only checks for exact `time` matches — duration-based overlap (e.g., a 45-min task at 07:00 running into a task at 07:30) is not yet tested or detected. Expanding to interval-overlap checks would push this to 5/5.

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Sorts all tasks chronologically by `Task.time` ("HH:MM"); lexicographic sort works because times are zero-padded |
| Filtering | `Scheduler.filter_by_completion(completed)`, `Scheduler.filter_by_pet(pet_name)` | Filter across all pets by done/undone status, or return one pet's task list by name |
| Conflict handling | `Scheduler.detect_conflicts()` | Detects exact `time` collisions per pet; returns warning strings instead of raising |
| Recurring tasks | `Scheduler.advance_daily_tasks()` | Finds completed tasks with `frequency="daily"` and adds a fresh copy (is_completed=False) to the same pet |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. Enter your name in the "Owner" text input to personalize your session.
2. Use the "Add a Pet" form to register your pets (e.g., dog, cat) and add them to your profile.
3. Use the "Schedule a Task" section to assign activities to specific pets, setting the duration, time (HH:MM), priority, and frequency (once/daily).
4. View the "Daily Schedule" table to see all tasks automatically sorted chronologically. (If you schedule two tasks at the exact same time for the same pet, a conflict warning will appear at the top).
5. Click the "✓ Complete" button on a "daily" task to mark it done; the system will automatically generate a fresh, uncompleted task for the next day.

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
