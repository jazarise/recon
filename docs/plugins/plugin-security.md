# Plugin Security Guidelines

When writing plugins, you are executing commands on the worker nodes. You **must** follow these security guidelines to prevent your plugin from becoming a vulnerability itself.

1. **Never use `shell=True`**: This is strictly enforced. Passing untrusted targets to a shell enables trivial command injection.
2. **Use the SDK**: Always use `run_command` from `sdk.plugin_sdk.helpers`.
3. **Validate Inputs**: Always run `validate_target` before passing it to an underlying binary.
4. **Least Privilege**: Plugins run under the `reconx` user context inside the Docker container. Do not attempt to write to `/etc/` or other protected paths.
