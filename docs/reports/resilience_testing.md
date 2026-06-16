# Resilience & Fault Tolerance

Fault simulation executed locally.

| Failure Event | Recovery Behavior | Status |
| ------------- | ----------------- | ------ |
| Database outage | Graceful pause and retry connection logic. | Passed |
| Plugin crash  | Sandbox isolates error, marks stage 'failed', proceeds with workflow. | Passed |
| API timeout   | 429 / 503 backoff mechanisms triggered. | Passed |
