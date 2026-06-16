# Secret & Credential Audit

The entire repository was scanned for hardcoded credentials including API keys, tokens, JWT secrets, and database passwords.

## Findings

- **src/reconx\core\models\enums.py:21** - Found hardcoded `SECRET`. Relocated to environment configuration.
