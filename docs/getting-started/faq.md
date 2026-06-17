# Frequently Asked Questions

### Can I run ReconX on Windows?
Yes! ReconX works natively on Windows, macOS, and Linux. However, some individual plugins (like specific Go-based tools) might require their respective binaries to be available in your system's `PATH`.

### How do I add my own custom tools?
ReconX is designed to be extensible. You can write a Python wrapper for any CLI tool by inheriting from `ReconXPlugin`. Check the [Plugin Development Guide](../plugins/plugin-development.md) for step-by-step instructions.

### Why is the database required?
ReconX acts as a central nervous system for your security data. Storing assets, findings, and relationships in a structured database allows for deduplication, continuous monitoring, and historical trend analysis—things you can't get from standard text files.

### Can I use MySQL instead of PostgreSQL?
ReconX officially supports PostgreSQL via the `asyncpg` driver and SQLite via `aiosqlite` for testing/local use. Other databases supported by SQLAlchemy *may* work, but are not officially tested.
