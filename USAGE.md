# ReconX Usage Guide

## Basic Invocation
```bash
reconx run --workflow default_scan --target 192.168.1.1
```

## System Checks
```bash
reconx doctor
```

## Logs
Execution logs are stored safely in `logs/reconx.log` and `logs/errors.log` utilizing 10MB file rotation limits.
