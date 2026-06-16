# Stage 13: OPSEC Architecture Report

## Detection Engine
We mapped the `RiskScore` enum against all native plugins. `RiskScore.HIGH` (Port Scanning) is now natively intercepted and suppressed by the `DetectionEngine` whenever the `--mode stealth` CLI flag is utilized.

## Traffic Jitter & UA Obfuscation
The `StealthHTTPClient` dynamically overrides raw request timers, injecting randomized `0.2` to `1.5` second delays and rotating between 3 valid Chromium/Firefox User-Agent strings to blend cleanly into enterprise traffic firewalls.

## Smart Suppression
The `ScanSuppressor` implements early-exit hashing, ensuring duplicate subdomain vectors don't trigger cascading redundant queries that could alert SOC analysts.
