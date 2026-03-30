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

### Smarter Scheduling

- Added:
    - Sort by time
    - Filter by pet or status
    - Recurring tasks
    - Detect time conflict

### Testing PawPal+

## Command to run tests: python -m pytest

## Description of what the tests cover
- test_task_completion: A new task starts incomplete and calls .complete() to marks it done.

- test_task_addition_increases_pet_task_count: A pet list starts with 0 tasks and appending one brings the count to 1.

- test_sort_by_time_returns_chronological_order: Three tasks added out of order are returned earliest-first by sort_by_time().

- test_complete_and_recur_creates_next_day_task: Completing a daily task auto-schedules an identical task exactly 24 hours later.

- test_conflict_detection_flags_tasks_within_15_minutes: Two tasks only 10 minutes apart trigger a conflict warning naming the overlapping task.

- test_no_conflict_when_tasks_are_far_apart: Two tasks 10 hours apart produce zero warnings.

## Confidence lelvel for the system's reliability based on the test results: 5

## Features
Task Scheduling — Assign care tasks (feeding, grooming, exercise, vet visits, and more) to any pet with a title, type, due time, and optional description.

Recurring Tasks — Tasks marked daily, weekly, or monthly automatically generate their next occurrence when completed, calculated from the original due date to keep timing consistent.

Conflict Detection — Before any task is added, the scheduler checks all existing tasks within a configurable window (default: 15 minutes). Overlapping tasks surface a human-readable warning in the UI instead of silently overwriting each other.

Chronological Sorting — The full task queue (or any filtered subset) can be sorted earliest-to-latest by due date without modifying the original list.

Filtering by Pet and Status — Tasks can be narrowed by pet ID and/or status (pending, completed, overdue) independently or in combination.

Overdue Detection — Any incomplete task whose due date has passed is automatically flagged as overdue, both in filters and in the daily schedule view.

Multi-Pet Support — An owner can manage any number of pets, each with their own independent task list. Cross-pet conflict checking is also supported.

Streamlit Dashboard — A live web UI lets users add pets, schedule tasks, pick filter options, and view today's sorted schedule in a labeled table with Pending / Completed / Overdue summary metrics.

## Location of uml-final.png: pictures/uml_final.png


