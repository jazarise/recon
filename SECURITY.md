# Security Policy

## Supported Versions

We provide security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |
| < 1.0   | :x:                |

The 1.x line will receive security updates and bug fixes for **12 months** following the release of v2.0.

## Reporting a Vulnerability

Please do not report security vulnerabilities through public GitHub issues.

Instead, please report them to our security team by emailing `security@reconx.local`. 

You should receive a response within 48 hours. If the issue is confirmed, we will release a patch as soon as possible, along with a coordinated public disclosure.

### Scope
We are primarily concerned with vulnerabilities in the **Core Platform** (API, Database, Sandbox bypasses, Authentication). Vulnerabilities in third-party binaries (e.g., a buffer overflow in `nmap`) should be reported to their respective upstream maintainers, though we may issue a plugin update to mitigate the risk.
