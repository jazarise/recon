# Dependency Conflict Resolution

## Process
We discovered over 1,700 \`requirements.txt\` files spanning various plugins. 
These files contained conflicting versions and even standard library modules.

## Actions Taken
1. Deleted all 1,760 localized \`requirements.txt\` files within the \`plugins/\` directory.
2. Standardized to a single \`pyproject.toml\` at the project root.
3. Created a unified \`requirements.txt\` for legacy compatibility.
