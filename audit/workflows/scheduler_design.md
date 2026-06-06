# Scheduler Design

The `Scheduler` (`core/scheduler.py`) is a lightweight background thread running standard `schedule` library primitives.
- Monitors recurring tasks.
- Deposits tasks into the `TaskQueue` when their cron/interval is hit.
- Fully non-blocking.
