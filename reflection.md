# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

I started with 4 classes: `Task` (pure data — what needs doing, how long, how urgent), `Pet` (owns a list of Tasks), `Owner` (owns a list of Pets), and `Scheduler` (a service that operates on the Owner's data). I used `@dataclass` for the three data models to get `__init__` and `__repr__` for free, and kept `Scheduler` as a regular class because it has no data of its own — just methods that read and transform the owner's object graph.

**b. Design changes**

Yes. `Task` originally had only 4 fields: `description`, `duration`, `priority`, and `is_completed`. In Phase 4 (algorithmic layer), I added `time` (an HH:MM string) and `frequency` (`"once"` or `"daily"`) to support chronological sorting and daily recurrence. Because both new fields have defaults, no existing code broke — the change was purely additive.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler currently uses `time` for sorting and `frequency` for recurrence. `priority` is stored on every task but not yet used for ordering — it's there for a future "sort by priority within the same time slot" feature. The constraint I focused on first was `time`, because without it the daily schedule table had no natural ordering and the UI felt meaningless. Priority-based ordering would be the next logical addition.

**b. Tradeoffs**

The conflict detector checks for exact `time` matches only — it does not calculate whether a task's duration causes it to overlap with the next task (e.g., a 45-minute Vet Checkup at 07:00 would run until 07:45 and overlap with an 07:30 walk, but the scheduler would not flag this). This is a reasonable simplification for a single-owner, low-volume daily planner where the owner is expected to set times thoughtfully, and full interval-overlap detection would require converting "HH:MM" strings to integers and comparing ranges, adding complexity without much benefit at this scale.

---

## 3. AI Collaboration

**a. How you used AI**

I used Claude Code throughout all 6 phases: scaffolding the `@dataclass` stubs, implementing the algorithm methods (`sort_by_time`, `detect_conflicts`, `advance_daily_tasks`), wiring the Streamlit forms to `st.session_state`, and generating the test suite. The most effective prompts were specific and structural — for example, describing the exact invariant I wanted ("iterate a snapshot of `pet.tasks` to avoid mutating while iterating") rather than a vague goal like "make recurring tasks work." The more precisely I described the contract, the less I had to revise the output.

**b. Judgment and verification**

One moment of independent judgment: in `advance_daily_tasks()`, Claude used `list(pet.tasks)` to snapshot the task list before the loop. I paused to reason through why — without the snapshot, `pet.add_task(new_task)` would extend the same list being iterated, causing newly-created copies to be processed in the same pass and potentially creating an infinite loop. I verified this by mentally tracing a single-task case through both the snapshot and no-snapshot versions before accepting the code. It was a subtle bug that could have been invisible in simple tests.

---

## 4. Testing and Verification

**a. What you tested**

Five behaviors: (1) `mark_complete()` flips `is_completed` to `True`, (2) `add_task()` grows the pet's task list, (3) `sort_by_time()` returns tasks in chronological order when added out of order, (4) `advance_daily_tasks()` creates exactly one uncompleted copy per completed daily task, (5) `detect_conflicts()` returns a warning string when two tasks on the same pet share a time. These are the exact behaviors the Streamlit UI depends on — if any silently broke, the UI would produce wrong output without crashing and I might not notice.

**b. Confidence**

★★★★☆ (4/5) — same rating as in the README. The core happy-path behaviors are covered. Edge cases I'd test next: (a) duration-based overlap (a 45-minute task at 07:00 running past a task at 07:30), (b) calling `advance_daily_tasks()` twice on the same already-completed daily task (would it create two copies?), and (c) `filter_by_pet()` with a pet name that doesn't exist in the owner's list.

---

## 5. Reflection

**a. What went well**

The separation between the data layer (`@dataclass` models) and the service layer (`Scheduler`). Because `Task`, `Pet`, and `Owner` are pure data objects with no cross-cutting logic, every new algorithm in Phase 4 could be added entirely inside `Scheduler` without touching the models. Each phase felt additive rather than disruptive, and the tests stayed green throughout.

**b. What you would improve**

I would add a `date` field to `Task`. Right now `advance_daily_tasks()` creates a copy with the same `time` but no concept of "tomorrow" — the new task is indistinguishable from the original except that `is_completed` is `False`. A `datetime.date` field would let the scheduler target the actual next calendar day and filter the table to show only today's tasks, which is the feature that would make this genuinely useful rather than a demo.

**c. Key takeaway**

Design the interfaces before writing any logic. Going through UML → stubs (all `pass`) → implementation forced a clear separation between "what does this class hold?" and "what does it do?" That discipline made it easy to add Phase 4 algorithms without breaking Phases 1–3, and it made writing tests straightforward because the behavior contract was already explicit in the method signatures before I wrote a single line of logic.
