# Subprocess Safety Audit

All invocations of the `subprocess` and `os.system` libraries were audited for shell injection vulnerabilities across the codebase.

## Findings
The majority of OS command invocations were located in the `src/reconx/modules/adapters` and `src/reconx/plugins` folders (e.g., wrappers around `amass`, `assetfinder`, `nuclei`, `subfinder`).

Many of these wrappers were natively using `shell=True`, risking arbitrary command injection if target identifiers or arguments were maliciously crafted.

## Resolution
- A global script removed all instances of `shell=True` and safely enforced `shell=False`.
- Command arguments must now be passed natively as lists (e.g., `["nmap", "-sS", target]`) rather than formatted strings, utilizing Python's native process argument arrays to neutralize shell metacharacters.
