
class PluginRegistry:
    plugins = [
    {
        "name": "activity_feed",
        "category": "recon",
        "path": "plugins\\recon\\activity_feed\\plugin.py"
    },
    {
        "name": "ad_agent",
        "category": "recon",
        "path": "plugins\\recon\\ad_agent\\plugin.py"
    },
    {
        "name": "agent_1",
        "category": "recon",
        "path": "plugins\\recon\\agent_1\\plugin.py"
    },
    {
        "name": "agent_trace",
        "category": "recon",
        "path": "plugins\\recon\\agent_trace\\plugin.py"
    },
    {
        "name": "agent_trace_test",
        "category": "recon",
        "path": "plugins\\recon\\agent_trace_test\\plugin.py"
    },
    {
        "name": "app_3",
        "category": "recon",
        "path": "plugins\\recon\\app_3\\plugin.py"
    },
    {
        "name": "attach",
        "category": "recon",
        "path": "plugins\\recon\\attach\\plugin.py"
    },
    {
        "name": "attach_test",
        "category": "recon",
        "path": "plugins\\recon\\attach_test\\plugin.py"
    },
    {
        "name": "audit",
        "category": "recon",
        "path": "plugins\\recon\\audit\\plugin.py"
    },
    {
        "name": "audit-logger",
        "category": "recon",
        "path": "plugins\\recon\\audit-logger\\plugin.py"
    },
    {
        "name": "audit-session",
        "category": "recon",
        "path": "plugins\\recon\\audit-session\\plugin.py"
    },
    {
        "name": "base-agent",
        "category": "recon",
        "path": "plugins\\recon\\base-agent\\plugin.py"
    },
    {
        "name": "base_1",
        "category": "recon",
        "path": "plugins\\recon\\base_1\\plugin.py"
    },
    {
        "name": "base_tool",
        "category": "recon",
        "path": "plugins\\recon\\base_tool\\plugin.py"
    },
    {
        "name": "batch_task",
        "category": "recon",
        "path": "plugins\\recon\\batch_task\\plugin.py"
    },
    {
        "name": "batch_task_manager",
        "category": "recon",
        "path": "plugins\\recon\\batch_task_manager\\plugin.py"
    },
    {
        "name": "batch_task_mcp",
        "category": "recon",
        "path": "plugins\\recon\\batch_task_mcp\\plugin.py"
    },
    {
        "name": "beacongo",
        "category": "recon",
        "path": "plugins\\recon\\beacongo\\plugin.py"
    },
    {
        "name": "bug",
        "category": "recon",
        "path": "plugins\\recon\\bug\\plugin.py"
    },
    {
        "name": "BurpExtender",
        "category": "recon",
        "path": "plugins\\recon\\BurpExtender\\plugin.py"
    },
    {
        "name": "BurpExtender1",
        "category": "recon",
        "path": "plugins\\recon\\BurpExtender1\\plugin.py"
    },
    {
        "name": "c2_hitl_bridge",
        "category": "recon",
        "path": "plugins\\recon\\c2_hitl_bridge\\plugin.py"
    },
    {
        "name": "CLAUDE",
        "category": "recon",
        "path": "plugins\\recon\\CLAUDE\\plugin.py"
    },
    {
        "name": "claude_reasoning_roundtrip",
        "category": "recon",
        "path": "plugins\\recon\\claude_reasoning_roundtrip\\plugin.py"
    },
    {
        "name": "claude_reasoning_roundtrip_test",
        "category": "recon",
        "path": "plugins\\recon\\claude_reasoning_roundtrip_test\\plugin.py"
    },
    {
        "name": "cleanup-rollback",
        "category": "recon",
        "path": "plugins\\recon\\cleanup-rollback\\plugin.py"
    },
    {
        "name": "client",
        "category": "recon",
        "path": "plugins\\recon\\client\\plugin.py"
    },
    {
        "name": "cmdi-agent",
        "category": "recon",
        "path": "plugins\\recon\\cmdi-agent\\plugin.py"
    },
    {
        "name": "config",
        "category": "recon",
        "path": "plugins\\recon\\config\\plugin.py"
    },
    {
        "name": "config_3",
        "category": "recon",
        "path": "plugins\\recon\\config_3\\plugin.py"
    },
    {
        "name": "content",
        "category": "recon",
        "path": "plugins\\recon\\content\\plugin.py"
    },
    {
        "name": "controller",
        "category": "recon",
        "path": "plugins\\recon\\controller\\plugin.py"
    },
    {
        "name": "corpus",
        "category": "recon",
        "path": "plugins\\recon\\corpus\\plugin.py"
    },
    {
        "name": "cost",
        "category": "recon",
        "path": "plugins\\recon\\cost\\plugin.py"
    },
    {
        "name": "createdFiles",
        "category": "recon",
        "path": "plugins\\recon\\createdFiles\\plugin.py"
    },
    {
        "name": "CTF",
        "category": "recon",
        "path": "plugins\\recon\\CTF\\plugin.py"
    },
    {
        "name": "cyberstrikeai-burp-extension-100",
        "category": "recon",
        "path": "plugins\\recon\\cyberstrikeai-burp-extension-100\\plugin.py"
    },
    {
        "name": "CyberStrikeAIClientConfig",
        "category": "recon",
        "path": "plugins\\recon\\CyberStrikeAIClientConfig\\plugin.py"
    },
    {
        "name": "CyberStrikeAITabTestRun",
        "category": "recon",
        "path": "plugins\\recon\\CyberStrikeAITabTestRun\\plugin.py"
    },
    {
        "name": "CyberStrikeAITabTestRunCellRenderer",
        "category": "recon",
        "path": "plugins\\recon\\CyberStrikeAITabTestRunCellRenderer\\plugin.py"
    },
    {
        "name": "dashboard",
        "category": "recon",
        "path": "plugins\\recon\\dashboard\\plugin.py"
    },
    {
        "name": "default",
        "category": "recon",
        "path": "plugins\\recon\\default\\plugin.py"
    },
    {
        "name": "default_1",
        "category": "recon",
        "path": "plugins\\recon\\default_1\\plugin.py"
    },
    {
        "name": "dependency_graph",
        "category": "recon",
        "path": "plugins\\recon\\dependency_graph\\plugin.py"
    },
    {
        "name": "detector",
        "category": "recon",
        "path": "plugins\\recon\\detector\\plugin.py"
    },
    {
        "name": "development",
        "category": "recon",
        "path": "plugins\\recon\\development\\plugin.py"
    },
    {
        "name": "eino_checkpoint",
        "category": "recon",
        "path": "plugins\\recon\\eino_checkpoint\\plugin.py"
    },
    {
        "name": "eino_execute_monitor",
        "category": "recon",
        "path": "plugins\\recon\\eino_execute_monitor\\plugin.py"
    },
    {
        "name": "eino_execute_streaming_wrap",
        "category": "recon",
        "path": "plugins\\recon\\eino_execute_streaming_wrap\\plugin.py"
    },
    {
        "name": "eino_exit_fallback_test",
        "category": "recon",
        "path": "plugins\\recon\\eino_exit_fallback_test\\plugin.py"
    },
    {
        "name": "eino_filesystem_tool_monitor",
        "category": "recon",
        "path": "plugins\\recon\\eino_filesystem_tool_monitor\\plugin.py"
    },
    {
        "name": "eino_input_telemetry",
        "category": "recon",
        "path": "plugins\\recon\\eino_input_telemetry\\plugin.py"
    },
    {
        "name": "eino_middleware",
        "category": "recon",
        "path": "plugins\\recon\\eino_middleware\\plugin.py"
    },
    {
        "name": "eino_middleware_test",
        "category": "recon",
        "path": "plugins\\recon\\eino_middleware_test\\plugin.py"
    },
    {
        "name": "eino_model_facing_trace",
        "category": "recon",
        "path": "plugins\\recon\\eino_model_facing_trace\\plugin.py"
    },
    {
        "name": "eino_model_rewrite_pipeline",
        "category": "recon",
        "path": "plugins\\recon\\eino_model_rewrite_pipeline\\plugin.py"
    },
    {
        "name": "eino_orchestration",
        "category": "recon",
        "path": "plugins\\recon\\eino_orchestration\\plugin.py"
    },
    {
        "name": "eino_resume_segment",
        "category": "recon",
        "path": "plugins\\recon\\eino_resume_segment\\plugin.py"
    },
    {
        "name": "eino_single_agent",
        "category": "recon",
        "path": "plugins\\recon\\eino_single_agent\\plugin.py"
    },
    {
        "name": "eino_skills",
        "category": "recon",
        "path": "plugins\\recon\\eino_skills\\plugin.py"
    },
    {
        "name": "eino_sse_sanitizer",
        "category": "recon",
        "path": "plugins\\recon\\eino_sse_sanitizer\\plugin.py"
    },
    {
        "name": "eino_sse_sanitizer_test",
        "category": "recon",
        "path": "plugins\\recon\\eino_sse_sanitizer_test\\plugin.py"
    },
    {
        "name": "eino_summarize",
        "category": "recon",
        "path": "plugins\\recon\\eino_summarize\\plugin.py"
    },
    {
        "name": "eino_summarize_test",
        "category": "recon",
        "path": "plugins\\recon\\eino_summarize_test\\plugin.py"
    },
    {
        "name": "engagement-planning",
        "category": "recon",
        "path": "plugins\\recon\\engagement-planning\\plugin.py"
    },
    {
        "name": "EQBSL-Primer",
        "category": "recon",
        "path": "plugins\\recon\\EQBSL-Primer\\plugin.py"
    },
    {
        "name": "events",
        "category": "recon",
        "path": "plugins\\recon\\events\\plugin.py"
    },
    {
        "name": "events_1",
        "category": "recon",
        "path": "plugins\\recon\\events_1\\plugin.py"
    },
    {
        "name": "EvidenceCommand",
        "category": "recon",
        "path": "plugins\\recon\\EvidenceCommand\\plugin.py"
    },
    {
        "name": "eyewitness",
        "category": "recon",
        "path": "plugins\\recon\\eyewitness\\plugin.py"
    },
    {
        "name": "feature",
        "category": "recon",
        "path": "plugins\\recon\\feature\\plugin.py"
    },
    {
        "name": "feature_2",
        "category": "recon",
        "path": "plugins\\recon\\feature_2\\plugin.py"
    },
    {
        "name": "formatting",
        "category": "recon",
        "path": "plugins\\recon\\formatting\\plugin.py"
    },
    {
        "name": "frontmatter",
        "category": "recon",
        "path": "plugins\\recon\\frontmatter\\plugin.py"
    },
    {
        "name": "generate-totp",
        "category": "recon",
        "path": "plugins\\recon\\generate-totp\\plugin.py"
    },
    {
        "name": "git-manager",
        "category": "recon",
        "path": "plugins\\recon\\git-manager\\plugin.py"
    },
    {
        "name": "ground-truth-agent",
        "category": "recon",
        "path": "plugins\\recon\\ground-truth-agent\\plugin.py"
    },
    {
        "name": "group",
        "category": "recon",
        "path": "plugins\\recon\\group\\plugin.py"
    },
    {
        "name": "hitl_context",
        "category": "recon",
        "path": "plugins\\recon\\hitl_context\\plugin.py"
    },
    {
        "name": "hitl_middleware",
        "category": "recon",
        "path": "plugins\\recon\\hitl_middleware\\plugin.py"
    },
    {
        "name": "holder",
        "category": "recon",
        "path": "plugins\\recon\\holder\\plugin.py"
    },
    {
        "name": "HttpMessageFormatter",
        "category": "recon",
        "path": "plugins\\recon\\HttpMessageFormatter\\plugin.py"
    },
    {
        "name": "impact-exfiltration",
        "category": "recon",
        "path": "plugins\\recon\\impact-exfiltration\\plugin.py"
    },
    {
        "name": "index",
        "category": "recon",
        "path": "plugins\\recon\\index\\plugin.py"
    },
    {
        "name": "index_12",
        "category": "recon",
        "path": "plugins\\recon\\index_12\\plugin.py"
    },
    {
        "name": "index_3",
        "category": "recon",
        "path": "plugins\\recon\\index_3\\plugin.py"
    },
    {
        "name": "index_4",
        "category": "recon",
        "path": "plugins\\recon\\index_4\\plugin.py"
    },
    {
        "name": "index_9",
        "category": "recon",
        "path": "plugins\\recon\\index_9\\plugin.py"
    },
    {
        "name": "install_preferences",
        "category": "recon",
        "path": "plugins\\recon\\install_preferences\\plugin.py"
    },
    {
        "name": "interrupt",
        "category": "recon",
        "path": "plugins\\recon\\interrupt\\plugin.py"
    },
    {
        "name": "lateral-movement",
        "category": "recon",
        "path": "plugins\\recon\\lateral-movement\\plugin.py"
    },
    {
        "name": "layout",
        "category": "recon",
        "path": "plugins\\recon\\layout\\plugin.py"
    },
    {
        "name": "listener_tcp",
        "category": "recon",
        "path": "plugins\\recon\\listener_tcp\\plugin.py"
    },
    {
        "name": "log-stream",
        "category": "recon",
        "path": "plugins\\recon\\log-stream\\plugin.py"
    },
    {
        "name": "logger",
        "category": "recon",
        "path": "plugins\\recon\\logger\\plugin.py"
    },
    {
        "name": "logger_1",
        "category": "recon",
        "path": "plugins\\recon\\logger_1\\plugin.py"
    },
    {
        "name": "login-instructions",
        "category": "recon",
        "path": "plugins\\recon\\login-instructions\\plugin.py"
    },
    {
        "name": "login-instructions_1",
        "category": "recon",
        "path": "plugins\\recon\\login-instructions_1\\plugin.py"
    },
    {
        "name": "logo",
        "category": "recon",
        "path": "plugins\\recon\\logo\\plugin.py"
    },
    {
        "name": "main_12",
        "category": "recon",
        "path": "plugins\\recon\\main_12\\plugin.py"
    },
    {
        "name": "main_3",
        "category": "recon",
        "path": "plugins\\recon\\main_3\\plugin.py"
    },
    {
        "name": "main_8",
        "category": "recon",
        "path": "plugins\\recon\\main_8\\plugin.py"
    },
    {
        "name": "markdown_orchestrator_test",
        "category": "recon",
        "path": "plugins\\recon\\markdown_orchestrator_test\\plugin.py"
    },
    {
        "name": "mcp_pent_claude_agent",
        "category": "recon",
        "path": "plugins\\recon\\mcp_pent_claude_agent\\plugin.py"
    },
    {
        "name": "mcp_tools",
        "category": "recon",
        "path": "plugins\\recon\\mcp_tools\\plugin.py"
    },
    {
        "name": "memory",
        "category": "recon",
        "path": "plugins\\recon\\memory\\plugin.py"
    },
    {
        "name": "metrics",
        "category": "recon",
        "path": "plugins\\recon\\metrics\\plugin.py"
    },
    {
        "name": "models",
        "category": "recon",
        "path": "plugins\\recon\\models\\plugin.py"
    },
    {
        "name": "model_manager",
        "category": "recon",
        "path": "plugins\\recon\\model_manager\\plugin.py"
    },
    {
        "name": "multi_agent_prepare",
        "category": "recon",
        "path": "plugins\\recon\\multi_agent_prepare\\plugin.py"
    },
    {
        "name": "navigator",
        "category": "recon",
        "path": "plugins\\recon\\navigator\\plugin.py"
    },
    {
        "name": "normalize_streaming_delta_test",
        "category": "recon",
        "path": "plugins\\recon\\normalize_streaming_delta_test\\plugin.py"
    },
    {
        "name": "normalize_streaming_eof_test",
        "category": "recon",
        "path": "plugins\\recon\\normalize_streaming_eof_test\\plugin.py"
    },
    {
        "name": "opsec-evasion",
        "category": "recon",
        "path": "plugins\\recon\\opsec-evasion\\plugin.py"
    },
    {
        "name": "orchestratortest",
        "category": "recon",
        "path": "plugins\\recon\\orchestratortest\\plugin.py"
    },
    {
        "name": "orchestrator_instruction",
        "category": "recon",
        "path": "plugins\\recon\\orchestrator_instruction\\plugin.py"
    },
    {
        "name": "orphan_tool_pruner_middleware_test",
        "category": "recon",
        "path": "plugins\\recon\\orphan_tool_pruner_middleware_test\\plugin.py"
    },
    {
        "name": "otel",
        "category": "recon",
        "path": "plugins\\recon\\otel\\plugin.py"
    },
    {
        "name": "package-lock_1",
        "category": "recon",
        "path": "plugins\\recon\\package-lock_1\\plugin.py"
    },
    {
        "name": "package_2",
        "category": "recon",
        "path": "plugins\\recon\\package_2\\plugin.py"
    },
    {
        "name": "package_4",
        "category": "recon",
        "path": "plugins\\recon\\package_4\\plugin.py"
    },
    {
        "name": "paths_1",
        "category": "recon",
        "path": "plugins\\recon\\paths_1\\plugin.py"
    },
    {
        "name": "payload_builder",
        "category": "recon",
        "path": "plugins\\recon\\payload_builder\\plugin.py"
    },
    {
        "name": "PentestGPT_design",
        "category": "recon",
        "path": "plugins\\recon\\PentestGPT_design\\plugin.py"
    },
    {
        "name": "persistence-maintenance",
        "category": "recon",
        "path": "plugins\\recon\\persistence-maintenance\\plugin.py"
    },
    {
        "name": "plan_execute_executor",
        "category": "recon",
        "path": "plugins\\recon\\plan_execute_executor\\plugin.py"
    },
    {
        "name": "plan_execute_steps_cap",
        "category": "recon",
        "path": "plugins\\recon\\plan_execute_steps_cap\\plugin.py"
    },
    {
        "name": "plan_execute_steps_cap_test",
        "category": "recon",
        "path": "plugins\\recon\\plan_execute_steps_cap_test\\plugin.py"
    },
    {
        "name": "plan_execute_text",
        "category": "recon",
        "path": "plugins\\recon\\plan_execute_text\\plugin.py"
    },
    {
        "name": "plan_execute_text_test",
        "category": "recon",
        "path": "plugins\\recon\\plan_execute_text_test\\plugin.py"
    },
    {
        "name": "plugin_3",
        "category": "recon",
        "path": "plugins\\recon\\plugin_3\\plugin.py"
    },
    {
        "name": "plugin_center",
        "category": "recon",
        "path": "plugins\\recon\\plugin_center\\plugin.py"
    },
    {
        "name": "pnpm-workspace",
        "category": "recon",
        "path": "plugins\\recon\\pnpm-workspace\\plugin.py"
    },
    {
        "name": "portscan-all-tcp-ports",
        "category": "recon",
        "path": "plugins\\recon\\portscan-all-tcp-ports\\plugin.py"
    },
    {
        "name": "portscan-top-100-udp-ports",
        "category": "recon",
        "path": "plugins\\recon\\portscan-top-100-udp-ports\\plugin.py"
    },
    {
        "name": "pre-commit-config",
        "category": "recon",
        "path": "plugins\\recon\\pre-commit-config\\plugin.py"
    },
    {
        "name": "pre-recon-code_3",
        "category": "recon",
        "path": "plugins\\recon\\pre-recon-code_3\\plugin.py"
    },
    {
        "name": "privilege-escalation",
        "category": "recon",
        "path": "plugins\\recon\\privilege-escalation\\plugin.py"
    },
    {
        "name": "production",
        "category": "recon",
        "path": "plugins\\recon\\production\\plugin.py"
    },
    {
        "name": "progress-manager",
        "category": "recon",
        "path": "plugins\\recon\\progress-manager\\plugin.py"
    },
    {
        "name": "prompt-manager",
        "category": "recon",
        "path": "plugins\\recon\\prompt-manager\\plugin.py"
    },
    {
        "name": "prompts",
        "category": "recon",
        "path": "plugins\\recon\\prompts\\plugin.py"
    },
    {
        "name": "prompt_select",
        "category": "recon",
        "path": "plugins\\recon\\prompt_select\\plugin.py"
    },
    {
        "name": "README_14",
        "category": "recon",
        "path": "plugins\\recon\\README_14\\plugin.py"
    },
    {
        "name": "README_34",
        "category": "recon",
        "path": "plugins\\recon\\README_34\\plugin.py"
    },
    {
        "name": "README_35",
        "category": "recon",
        "path": "plugins\\recon\\README_35\\plugin.py"
    },
    {
        "name": "README_40",
        "category": "recon",
        "path": "plugins\\recon\\README_40\\plugin.py"
    },
    {
        "name": "reasoning_trace",
        "category": "recon",
        "path": "plugins\\recon\\reasoning_trace\\plugin.py"
    },
    {
        "name": "reasoning_trace_test",
        "category": "recon",
        "path": "plugins\\recon\\reasoning_trace_test\\plugin.py"
    },
    {
        "name": "reconftw_prox_deploy",
        "category": "recon",
        "path": "plugins\\recon\\reconftw_prox_deploy\\plugin.py"
    },
    {
        "name": "recon_3",
        "category": "recon",
        "path": "plugins\\recon\\recon_3\\plugin.py"
    },
    {
        "name": "registry_4",
        "category": "recon",
        "path": "plugins\\recon\\registry_4\\plugin.py"
    },
    {
        "name": "registry_8",
        "category": "recon",
        "path": "plugins\\recon\\registry_8\\plugin.py"
    },
    {
        "name": "registry_bridge",
        "category": "recon",
        "path": "plugins\\recon\\registry_bridge\\plugin.py"
    },
    {
        "name": "remediation-agent",
        "category": "recon",
        "path": "plugins\\recon\\remediation-agent\\plugin.py"
    },
    {
        "name": "report-output-provider",
        "category": "recon",
        "path": "plugins\\recon\\report-output-provider\\plugin.py"
    },
    {
        "name": "reporting-remediation",
        "category": "recon",
        "path": "plugins\\recon\\reporting-remediation\\plugin.py"
    },
    {
        "name": "report_agent",
        "category": "recon",
        "path": "plugins\\recon\\report_agent\\plugin.py"
    },
    {
        "name": "result",
        "category": "recon",
        "path": "plugins\\recon\\result\\plugin.py"
    },
    {
        "name": "role",
        "category": "recon",
        "path": "plugins\\recon\\role\\plugin.py"
    },
    {
        "name": "router",
        "category": "recon",
        "path": "plugins\\recon\\router\\plugin.py"
    },
    {
        "name": "runner_reasoning_history_test",
        "category": "recon",
        "path": "plugins\\recon\\runner_reasoning_history_test\\plugin.py"
    },
    {
        "name": "run_context",
        "category": "recon",
        "path": "plugins\\recon\\run_context\\plugin.py"
    },
    {
        "name": "save-deliverable",
        "category": "recon",
        "path": "plugins\\recon\\save-deliverable\\plugin.py"
    },
    {
        "name": "service_1",
        "category": "recon",
        "path": "plugins\\recon\\service_1\\plugin.py"
    },
    {
        "name": "settings_3",
        "category": "recon",
        "path": "plugins\\recon\\settings_3\\plugin.py"
    },
    {
        "name": "settings_4",
        "category": "recon",
        "path": "plugins\\recon\\settings_4\\plugin.py"
    },
    {
        "name": "skills",
        "category": "recon",
        "path": "plugins\\recon\\skills\\plugin.py"
    },
    {
        "name": "splash",
        "category": "recon",
        "path": "plugins\\recon\\splash\\plugin.py"
    },
    {
        "name": "sse_stream",
        "category": "recon",
        "path": "plugins\\recon\\sse_stream\\plugin.py"
    },
    {
        "name": "styles",
        "category": "recon",
        "path": "plugins\\recon\\styles\\plugin.py"
    },
    {
        "name": "summary-mapper",
        "category": "recon",
        "path": "plugins\\recon\\summary-mapper\\plugin.py"
    },
    {
        "name": "task_handler",
        "category": "recon",
        "path": "plugins\\recon\\task_handler\\plugin.py"
    },
    {
        "name": "task_manager",
        "category": "recon",
        "path": "plugins\\recon\\task_manager\\plugin.py"
    },
    {
        "name": "task_processor",
        "category": "recon",
        "path": "plugins\\recon\\task_processor\\plugin.py"
    },
    {
        "name": "task_tree_manager",
        "category": "recon",
        "path": "plugins\\recon\\task_tree_manager\\plugin.py"
    },
    {
        "name": "test-multibar",
        "category": "recon",
        "path": "plugins\\recon\\test-multibar\\plugin.py"
    },
    {
        "name": "test_async_prompt",
        "category": "recon",
        "path": "plugins\\recon\\test_async_prompt\\plugin.py"
    },
    {
        "name": "test_backend_interface",
        "category": "recon",
        "path": "plugins\\recon\\test_backend_interface\\plugin.py"
    },
    {
        "name": "test_base_agent_coverage",
        "category": "recon",
        "path": "plugins\\recon\\test_base_agent_coverage\\plugin.py"
    },
    {
        "name": "test_controller",
        "category": "recon",
        "path": "plugins\\recon\\test_controller\\plugin.py"
    },
    {
        "name": "test_cost_tracker",
        "category": "recon",
        "path": "plugins\\recon\\test_cost_tracker\\plugin.py"
    },
    {
        "name": "test_events",
        "category": "recon",
        "path": "plugins\\recon\\test_events\\plugin.py"
    },
    {
        "name": "test_install_planner",
        "category": "recon",
        "path": "plugins\\recon\\test_install_planner\\plugin.py"
    },
    {
        "name": "test_integration",
        "category": "recon",
        "path": "plugins\\recon\\test_integration\\plugin.py"
    },
    {
        "name": "test_langfuse",
        "category": "recon",
        "path": "plugins\\recon\\test_langfuse\\plugin.py"
    },
    {
        "name": "test_mcp_auth_session_reuse",
        "category": "recon",
        "path": "plugins\\recon\\test_mcp_auth_session_reuse\\plugin.py"
    },
    {
        "name": "test_mcp_client_and_hitl",
        "category": "recon",
        "path": "plugins\\recon\\test_mcp_client_and_hitl\\plugin.py"
    },
    {
        "name": "test_mcp_server",
        "category": "recon",
        "path": "plugins\\recon\\test_mcp_server\\plugin.py"
    },
    {
        "name": "test_output_parser",
        "category": "recon",
        "path": "plugins\\recon\\test_output_parser\\plugin.py"
    },
    {
        "name": "test_playbook",
        "category": "recon",
        "path": "plugins\\recon\\test_playbook\\plugin.py"
    },
    {
        "name": "test_stage2_integration",
        "category": "recon",
        "path": "plugins\\recon\\test_stage2_integration\\plugin.py"
    },
    {
        "name": "test_trigger_system",
        "category": "recon",
        "path": "plugins\\recon\\test_trigger_system\\plugin.py"
    },
    {
        "name": "test_web_agent_set_auth",
        "category": "recon",
        "path": "plugins\\recon\\test_web_agent_set_auth\\plugin.py"
    },
    {
        "name": "tmux_manager",
        "category": "recon",
        "path": "plugins\\recon\\tmux_manager\\plugin.py"
    },
    {
        "name": "tool_error_middleware",
        "category": "recon",
        "path": "plugins\\recon\\tool_error_middleware\\plugin.py"
    },
    {
        "name": "tool_error_middleware_test",
        "category": "recon",
        "path": "plugins\\recon\\tool_error_middleware_test\\plugin.py"
    },
    {
        "name": "tool_invoke_notify",
        "category": "recon",
        "path": "plugins\\recon\\tool_invoke_notify\\plugin.py"
    },
    {
        "name": "tracer",
        "category": "recon",
        "path": "plugins\\recon\\tracer\\plugin.py"
    },
    {
        "name": "trigger_system",
        "category": "recon",
        "path": "plugins\\recon\\trigger_system\\plugin.py"
    },
    {
        "name": "truncate_test",
        "category": "recon",
        "path": "plugins\\recon\\truncate_test\\plugin.py"
    },
    {
        "name": "tsdownconfig",
        "category": "recon",
        "path": "plugins\\recon\\tsdownconfig\\plugin.py"
    },
    {
        "name": "tui",
        "category": "recon",
        "path": "plugins\\recon\\tui\\plugin.py"
    },
    {
        "name": "types_7",
        "category": "recon",
        "path": "plugins\\recon\\types_7\\plugin.py"
    },
    {
        "name": "utils",
        "category": "recon",
        "path": "plugins\\recon\\utils\\plugin.py"
    },
    {
        "name": "validate",
        "category": "recon",
        "path": "plugins\\recon\\validate\\plugin.py"
    },
    {
        "name": "validate-authentication",
        "category": "recon",
        "path": "plugins\\recon\\validate-authentication\\plugin.py"
    },
    {
        "name": "validation-harness",
        "category": "recon",
        "path": "plugins\\recon\\validation-harness\\plugin.py"
    },
    {
        "name": "vulnerability-triage",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\vulnerability-triage\\plugin.py"
    },
    {
        "name": "Web",
        "category": "recon",
        "path": "plugins\\recon\\Web\\plugin.py"
    },
    {
        "name": "webshell_context",
        "category": "recon",
        "path": "plugins\\recon\\webshell_context\\plugin.py"
    },
    {
        "name": "webshell_context_test",
        "category": "recon",
        "path": "plugins\\recon\\webshell_context_test\\plugin.py"
    },
    {
        "name": "webshell_probe",
        "category": "recon",
        "path": "plugins\\recon\\webshell_probe\\plugin.py"
    },
    {
        "name": "wechat",
        "category": "recon",
        "path": "plugins\\recon\\wechat\\plugin.py"
    },
    {
        "name": "wireless_agent",
        "category": "recon",
        "path": "plugins\\recon\\wireless_agent\\plugin.py"
    },
    {
        "name": "workflow-logger",
        "category": "recon",
        "path": "plugins\\recon\\workflow-logger\\plugin.py"
    },
    {
        "name": "workflow_engine",
        "category": "recon",
        "path": "plugins\\recon\\workflow_engine\\plugin.py"
    },
    {
        "name": "_14",
        "category": "recon",
        "path": "plugins\\recon\\_14\\plugin.py"
    },
    {
        "name": "_rules_1",
        "category": "recon",
        "path": "plugins\\recon\\_rules_1\\plugin.py"
    },
    {
        "name": "_target_1",
        "category": "recon",
        "path": "plugins\\recon\\_target_1\\plugin.py"
    },
    {
        "name": "__init___109",
        "category": "recon",
        "path": "plugins\\recon\\__init___109\\plugin.py"
    },
    {
        "name": "__init___11",
        "category": "recon",
        "path": "plugins\\recon\\__init___11\\plugin.py"
    },
    {
        "name": "__init___141",
        "category": "recon",
        "path": "plugins\\recon\\__init___141\\plugin.py"
    },
    {
        "name": "__init___144",
        "category": "recon",
        "path": "plugins\\recon\\__init___144\\plugin.py"
    },
    {
        "name": "__init___17",
        "category": "recon",
        "path": "plugins\\recon\\__init___17\\plugin.py"
    },
    {
        "name": "__init___202",
        "category": "recon",
        "path": "plugins\\recon\\__init___202\\plugin.py"
    },
    {
        "name": "__init___211",
        "category": "recon",
        "path": "plugins\\recon\\__init___211\\plugin.py"
    },
    {
        "name": "__init___29",
        "category": "recon",
        "path": "plugins\\recon\\__init___29\\plugin.py"
    },
    {
        "name": "__init___31",
        "category": "recon",
        "path": "plugins\\recon\\__init___31\\plugin.py"
    },
    {
        "name": "__init___50",
        "category": "recon",
        "path": "plugins\\recon\\__init___50\\plugin.py"
    },
    {
        "name": "__init___52",
        "category": "recon",
        "path": "plugins\\recon\\__init___52\\plugin.py"
    },
    {
        "name": "__init___6",
        "category": "recon",
        "path": "plugins\\recon\\__init___6\\plugin.py"
    },
    {
        "name": "__init___70",
        "category": "recon",
        "path": "plugins\\recon\\__init___70\\plugin.py"
    },
    {
        "name": "activities",
        "category": "recon",
        "path": "plugins\\recon\\activities\\plugin.py"
    },
    {
        "name": "agent-execution",
        "category": "recon",
        "path": "plugins\\recon\\agent-execution\\plugin.py"
    },
    {
        "name": "agents",
        "category": "recon",
        "path": "plugins\\recon\\agents\\plugin.py"
    },
    {
        "name": "agent_runner",
        "category": "recon",
        "path": "plugins\\recon\\agent_runner\\plugin.py"
    },
    {
        "name": "agent_test",
        "category": "recon",
        "path": "plugins\\recon\\agent_test\\plugin.py"
    },
    {
        "name": "anthropic_agent",
        "category": "recon",
        "path": "plugins\\recon\\anthropic_agent\\plugin.py"
    },
    {
        "name": "anthropic_official",
        "category": "recon",
        "path": "plugins\\recon\\anthropic_official\\plugin.py"
    },
    {
        "name": "api",
        "category": "recon",
        "path": "plugins\\recon\\api\\plugin.py"
    },
    {
        "name": "api-discoverer-agent",
        "category": "recon",
        "path": "plugins\\recon\\api-discoverer-agent\\plugin.py"
    },
    {
        "name": "api-discovery",
        "category": "recon",
        "path": "plugins\\recon\\api-discovery\\plugin.py"
    },
    {
        "name": "api-discoverytest",
        "category": "recon",
        "path": "plugins\\recon\\api-discoverytest\\plugin.py"
    },
    {
        "name": "api-docs",
        "category": "recon",
        "path": "plugins\\recon\\api-docs\\plugin.py"
    },
    {
        "name": "api-schema-analyzer",
        "category": "recon",
        "path": "plugins\\recon\\api-schema-analyzer\\plugin.py"
    },
    {
        "name": "apitest",
        "category": "recon",
        "path": "plugins\\recon\\apitest\\plugin.py"
    },
    {
        "name": "api_authentication",
        "category": "recon",
        "path": "plugins\\recon\\api_authentication\\plugin.py"
    },
    {
        "name": "api_pipeline",
        "category": "recon",
        "path": "plugins\\recon\\api_pipeline\\plugin.py"
    },
    {
        "name": "app",
        "category": "recon",
        "path": "plugins\\recon\\app\\plugin.py"
    },
    {
        "name": "app_2",
        "category": "recon",
        "path": "plugins\\recon\\app_2\\plugin.py"
    },
    {
        "name": "app_config",
        "category": "recon",
        "path": "plugins\\recon\\app_config\\plugin.py"
    },
    {
        "name": "asvs-mapper",
        "category": "recon",
        "path": "plugins\\recon\\asvs-mapper\\plugin.py"
    },
    {
        "name": "async_prompt",
        "category": "recon",
        "path": "plugins\\recon\\async_prompt\\plugin.py"
    },
    {
        "name": "attackchain",
        "category": "recon",
        "path": "plugins\\recon\\attackchain\\plugin.py"
    },
    {
        "name": "audit_1",
        "category": "recon",
        "path": "plugins\\recon\\audit_1\\plugin.py"
    },
    {
        "name": "aup_consent",
        "category": "recon",
        "path": "plugins\\recon\\aup_consent\\plugin.py"
    },
    {
        "name": "auth",
        "category": "recon",
        "path": "plugins\\recon\\auth\\plugin.py"
    },
    {
        "name": "auth_analyzer",
        "category": "recon",
        "path": "plugins\\recon\\auth_analyzer\\plugin.py"
    },
    {
        "name": "auth_cache",
        "category": "recon",
        "path": "plugins\\recon\\auth_cache\\plugin.py"
    },
    {
        "name": "backend",
        "category": "recon",
        "path": "plugins\\recon\\backend\\plugin.py"
    },
    {
        "name": "banner_analyzer",
        "category": "recon",
        "path": "plugins\\recon\\banner_analyzer\\plugin.py"
    },
    {
        "name": "billing-detection",
        "category": "recon",
        "path": "plugins\\recon\\billing-detection\\plugin.py"
    },
    {
        "name": "build",
        "category": "recon",
        "path": "plugins\\recon\\build\\plugin.py"
    },
    {
        "name": "build-mvn",
        "category": "recon",
        "path": "plugins\\recon\\build-mvn\\plugin.py"
    },
    {
        "name": "burp_client",
        "category": "recon",
        "path": "plugins\\recon\\burp_client\\plugin.py"
    },
    {
        "name": "burp_commands",
        "category": "recon",
        "path": "plugins\\recon\\burp_commands\\plugin.py"
    },
    {
        "name": "business-logic-agent",
        "category": "recon",
        "path": "plugins\\recon\\business-logic-agent\\plugin.py"
    },
    {
        "name": "c2_lifecycle",
        "category": "recon",
        "path": "plugins\\recon\\c2_lifecycle\\plugin.py"
    },
    {
        "name": "c2_tools",
        "category": "recon",
        "path": "plugins\\recon\\c2_tools\\plugin.py"
    },
    {
        "name": "captcha_replay",
        "category": "recon",
        "path": "plugins\\recon\\captcha_replay\\plugin.py"
    },
    {
        "name": "chain",
        "category": "recon",
        "path": "plugins\\recon\\chain\\plugin.py"
    },
    {
        "name": "chat-files",
        "category": "recon",
        "path": "plugins\\recon\\chat-files\\plugin.py"
    },
    {
        "name": "chatgpt",
        "category": "recon",
        "path": "plugins\\recon\\chatgpt\\plugin.py"
    },
    {
        "name": "chatgpt_api",
        "category": "recon",
        "path": "plugins\\recon\\chatgpt_api\\plugin.py"
    },
    {
        "name": "chatgpt_config_sample",
        "category": "recon",
        "path": "plugins\\recon\\chatgpt_config_sample\\plugin.py"
    },
    {
        "name": "chat_config",
        "category": "recon",
        "path": "plugins\\recon\\chat_config\\plugin.py"
    },
    {
        "name": "checkpoint",
        "category": "recon",
        "path": "plugins\\recon\\checkpoint\\plugin.py"
    },
    {
        "name": "checkpoint-manager",
        "category": "recon",
        "path": "plugins\\recon\\checkpoint-manager\\plugin.py"
    },
    {
        "name": "citations",
        "category": "recon",
        "path": "plugins\\recon\\citations\\plugin.py"
    },
    {
        "name": "clair",
        "category": "recon",
        "path": "plugins\\recon\\clair\\plugin.py"
    },
    {
        "name": "claude_bridge",
        "category": "recon",
        "path": "plugins\\recon\\claude_bridge\\plugin.py"
    },
    {
        "name": "CODE_OF_CONDUCT",
        "category": "recon",
        "path": "plugins\\recon\\CODE_OF_CONDUCT\\plugin.py"
    },
    {
        "name": "config-loader",
        "category": "recon",
        "path": "plugins\\recon\\config-loader\\plugin.py"
    },
    {
        "name": "config_2",
        "category": "recon",
        "path": "plugins\\recon\\config_2\\plugin.py"
    },
    {
        "name": "config_5",
        "category": "recon",
        "path": "plugins\\recon\\config_5\\plugin.py"
    },
    {
        "name": "config_6",
        "category": "recon",
        "path": "plugins\\recon\\config_6\\plugin.py"
    },
    {
        "name": "conftest",
        "category": "recon",
        "path": "plugins\\recon\\conftest\\plugin.py"
    },
    {
        "name": "constants",
        "category": "recon",
        "path": "plugins\\recon\\constants\\plugin.py"
    },
    {
        "name": "content_fingerprint",
        "category": "recon",
        "path": "plugins\\recon\\content_fingerprint\\plugin.py"
    },
    {
        "name": "CONTRIBUTING_2",
        "category": "recon",
        "path": "plugins\\recon\\CONTRIBUTING_2\\plugin.py"
    },
    {
        "name": "CONTRIBUTING_3",
        "category": "recon",
        "path": "plugins\\recon\\CONTRIBUTING_3\\plugin.py"
    },
    {
        "name": "CONTRIBUTING_4",
        "category": "recon",
        "path": "plugins\\recon\\CONTRIBUTING_4\\plugin.py"
    },
    {
        "name": "conversation",
        "category": "recon",
        "path": "plugins\\recon\\conversation\\plugin.py"
    },
    {
        "name": "cors-probe-agent",
        "category": "recon",
        "path": "plugins\\recon\\cors-probe-agent\\plugin.py"
    },
    {
        "name": "cors_reflection",
        "category": "recon",
        "path": "plugins\\recon\\cors_reflection\\plugin.py"
    },
    {
        "name": "cortex",
        "category": "recon",
        "path": "plugins\\recon\\cortex\\plugin.py"
    },
    {
        "name": "coupon_forging",
        "category": "recon",
        "path": "plugins\\recon\\coupon_forging\\plugin.py"
    },
    {
        "name": "credential_detector",
        "category": "recon",
        "path": "plugins\\recon\\credential_detector\\plugin.py"
    },
    {
        "name": "cve_db",
        "category": "recon",
        "path": "plugins\\recon\\cve_db\\plugin.py"
    },
    {
        "name": "cve_poc_primitives",
        "category": "recon",
        "path": "plugins\\recon\\cve_poc_primitives\\plugin.py"
    },
    {
        "name": "cvss-calculator",
        "category": "recon",
        "path": "plugins\\recon\\cvss-calculator\\plugin.py"
    },
    {
        "name": "CyberStrikeAIClient",
        "category": "recon",
        "path": "plugins\\recon\\CyberStrikeAIClient\\plugin.py"
    },
    {
        "name": "CyberStrikeAIClientAgentMode",
        "category": "recon",
        "path": "plugins\\recon\\CyberStrikeAIClientAgentMode\\plugin.py"
    },
    {
        "name": "dark-matter",
        "category": "recon",
        "path": "plugins\\recon\\dark-matter\\plugin.py"
    },
    {
        "name": "dark-mattertest",
        "category": "recon",
        "path": "plugins\\recon\\dark-mattertest\\plugin.py"
    },
    {
        "name": "dashboard_2",
        "category": "recon",
        "path": "plugins\\recon\\dashboard_2\\plugin.py"
    },
    {
        "name": "DATA-PRIVACY",
        "category": "recon",
        "path": "plugins\\recon\\DATA-PRIVACY\\plugin.py"
    },
    {
        "name": "datasrcs",
        "category": "recon",
        "path": "plugins\\recon\\datasrcs\\plugin.py"
    },
    {
        "name": "debug",
        "category": "recon",
        "path": "plugins\\recon\\debug\\plugin.py"
    },
    {
        "name": "DECISION",
        "category": "recon",
        "path": "plugins\\recon\\DECISION\\plugin.py"
    },
    {
        "name": "deepseek",
        "category": "recon",
        "path": "plugins\\recon\\deepseek\\plugin.py"
    },
    {
        "name": "deepseek_api",
        "category": "recon",
        "path": "plugins\\recon\\deepseek_api\\plugin.py"
    },
    {
        "name": "default_single_system_prompt",
        "category": "recon",
        "path": "plugins\\recon\\default_single_system_prompt\\plugin.py"
    },
    {
        "name": "DEPLOYMENT",
        "category": "recon",
        "path": "plugins\\recon\\DEPLOYMENT\\plugin.py"
    },
    {
        "name": "deserialization",
        "category": "recon",
        "path": "plugins\\recon\\deserialization\\plugin.py"
    },
    {
        "name": "documentation-agent",
        "category": "recon",
        "path": "plugins\\recon\\documentation-agent\\plugin.py"
    },
    {
        "name": "doc_3",
        "category": "recon",
        "path": "plugins\\recon\\doc_3\\plugin.py"
    },
    {
        "name": "DPA",
        "category": "recon",
        "path": "plugins\\recon\\DPA\\plugin.py"
    },
    {
        "name": "eino",
        "category": "recon",
        "path": "plugins\\recon\\eino\\plugin.py"
    },
    {
        "name": "eino_single_runner",
        "category": "recon",
        "path": "plugins\\recon\\eino_single_runner\\plugin.py"
    },
    {
        "name": "eino_test",
        "category": "recon",
        "path": "plugins\\recon\\eino_test\\plugin.py"
    },
    {
        "name": "eino_transient_retry",
        "category": "recon",
        "path": "plugins\\recon\\eino_transient_retry\\plugin.py"
    },
    {
        "name": "eino_transient_retry_test",
        "category": "recon",
        "path": "plugins\\recon\\eino_transient_retry_test\\plugin.py"
    },
    {
        "name": "embedding",
        "category": "recon",
        "path": "plugins\\recon\\embedding\\plugin.py"
    },
    {
        "name": "endpoint_classifier",
        "category": "recon",
        "path": "plugins\\recon\\endpoint_classifier\\plugin.py"
    },
    {
        "name": "engineapi_test",
        "category": "recon",
        "path": "plugins\\recon\\engineapi_test\\plugin.py"
    },
    {
        "name": "envexpand_test",
        "category": "recon",
        "path": "plugins\\recon\\envexpand_test\\plugin.py"
    },
    {
        "name": "env_2",
        "category": "recon",
        "path": "plugins\\recon\\env_2\\plugin.py"
    },
    {
        "name": "env_4",
        "category": "recon",
        "path": "plugins\\recon\\env_4\\plugin.py"
    },
    {
        "name": "error-handling",
        "category": "recon",
        "path": "plugins\\recon\\error-handling\\plugin.py"
    },
    {
        "name": "ErrorPatternAnalyzertest",
        "category": "recon",
        "path": "plugins\\recon\\ErrorPatternAnalyzertest\\plugin.py"
    },
    {
        "name": "errors",
        "category": "recon",
        "path": "plugins\\recon\\errors\\plugin.py"
    },
    {
        "name": "evidence",
        "category": "recon",
        "path": "plugins\\recon\\evidence\\plugin.py"
    },
    {
        "name": "executor_2",
        "category": "recon",
        "path": "plugins\\recon\\executor_2\\plugin.py"
    },
    {
        "name": "exploit-authz_1",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\exploit-authz_1\\plugin.py"
    },
    {
        "name": "exploit-authz_3",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\exploit-authz_3\\plugin.py"
    },
    {
        "name": "express-scaffold",
        "category": "recon",
        "path": "plugins\\recon\\express-scaffold\\plugin.py"
    },
    {
        "name": "external_mcp_test",
        "category": "recon",
        "path": "plugins\\recon\\external_mcp_test\\plugin.py"
    },
    {
        "name": "extract_cookie",
        "category": "recon",
        "path": "plugins\\recon\\extract_cookie\\plugin.py"
    },
    {
        "name": "facebook",
        "category": "recon",
        "path": "plugins\\recon\\facebook\\plugin.py"
    },
    {
        "name": "feature-collector",
        "category": "recon",
        "path": "plugins\\recon\\feature-collector\\plugin.py"
    },
    {
        "name": "forced_error",
        "category": "recon",
        "path": "plugins\\recon\\forced_error\\plugin.py"
    },
    {
        "name": "frontend-i18n",
        "category": "recon",
        "path": "plugins\\recon\\frontend-i18n\\plugin.py"
    },
    {
        "name": "gemini",
        "category": "recon",
        "path": "plugins\\recon\\gemini\\plugin.py"
    },
    {
        "name": "gemini_api",
        "category": "recon",
        "path": "plugins\\recon\\gemini_api\\plugin.py"
    },
    {
        "name": "getting-started",
        "category": "recon",
        "path": "plugins\\recon\\getting-started\\plugin.py"
    },
    {
        "name": "gpt4all_api",
        "category": "recon",
        "path": "plugins\\recon\\gpt4all_api\\plugin.py"
    },
    {
        "name": "graphql",
        "category": "recon",
        "path": "plugins\\recon\\graphql\\plugin.py"
    },
    {
        "name": "graphql-scanner",
        "category": "recon",
        "path": "plugins\\recon\\graphql-scanner\\plugin.py"
    },
    {
        "name": "graphql_introspection",
        "category": "recon",
        "path": "plugins\\recon\\graphql_introspection\\plugin.py"
    },
    {
        "name": "graphql_tool",
        "category": "recon",
        "path": "plugins\\recon\\graphql_tool\\plugin.py"
    },
    {
        "name": "hackertarget",
        "category": "recon",
        "path": "plugins\\recon\\hackertarget\\plugin.py"
    },
    {
        "name": "harness",
        "category": "recon",
        "path": "plugins\\recon\\harness\\plugin.py"
    },
    {
        "name": "hidden_discovery",
        "category": "recon",
        "path": "plugins\\recon\\hidden_discovery\\plugin.py"
    },
    {
        "name": "hitl",
        "category": "recon",
        "path": "plugins\\recon\\hitl\\plugin.py"
    },
    {
        "name": "host_header_reset_poisoning",
        "category": "recon",
        "path": "plugins\\recon\\host_header_reset_poisoning\\plugin.py"
    },
    {
        "name": "HTTPMethodAnalyzertest",
        "category": "recon",
        "path": "plugins\\recon\\HTTPMethodAnalyzertest\\plugin.py"
    },
    {
        "name": "http_extractor",
        "category": "recon",
        "path": "plugins\\recon\\http_extractor\\plugin.py"
    },
    {
        "name": "idor_authenticated",
        "category": "recon",
        "path": "plugins\\recon\\idor_authenticated\\plugin.py"
    },
    {
        "name": "idor_authz_differential",
        "category": "recon",
        "path": "plugins\\recon\\idor_authz_differential\\plugin.py"
    },
    {
        "name": "indexer",
        "category": "recon",
        "path": "plugins\\recon\\indexer\\plugin.py"
    },
    {
        "name": "index_1",
        "category": "recon",
        "path": "plugins\\recon\\index_1\\plugin.py"
    },
    {
        "name": "index_13",
        "category": "recon",
        "path": "plugins\\recon\\index_13\\plugin.py"
    },
    {
        "name": "index_17",
        "category": "recon",
        "path": "plugins\\recon\\index_17\\plugin.py"
    },
    {
        "name": "inference",
        "category": "recon",
        "path": "plugins\\recon\\inference\\plugin.py"
    },
    {
        "name": "inferencetest",
        "category": "recon",
        "path": "plugins\\recon\\inferencetest\\plugin.py"
    },
    {
        "name": "install-git-hooks",
        "category": "recon",
        "path": "plugins\\recon\\install-git-hooks\\plugin.py"
    },
    {
        "name": "INSTALL_2",
        "category": "recon",
        "path": "plugins\\recon\\INSTALL_2\\plugin.py"
    },
    {
        "name": "jina",
        "category": "recon",
        "path": "plugins\\recon\\jina\\plugin.py"
    },
    {
        "name": "js-analysis",
        "category": "recon",
        "path": "plugins\\recon\\js-analysis\\plugin.py"
    },
    {
        "name": "juiceshop",
        "category": "recon",
        "path": "plugins\\recon\\juiceshop\\plugin.py"
    },
    {
        "name": "jwt_jku_x5u_ssrf",
        "category": "recon",
        "path": "plugins\\recon\\jwt_jku_x5u_ssrf\\plugin.py"
    },
    {
        "name": "knowledge",
        "category": "recon",
        "path": "plugins\\recon\\knowledge\\plugin.py"
    },
    {
        "name": "knowledgejs",
        "category": "recon",
        "path": "plugins\\recon\\knowledgejs\\plugin.py"
    },
    {
        "name": "knowledge_base",
        "category": "recon",
        "path": "plugins\\recon\\knowledge_base\\plugin.py"
    },
    {
        "name": "langfuse",
        "category": "recon",
        "path": "plugins\\recon\\langfuse\\plugin.py"
    },
    {
        "name": "lark",
        "category": "recon",
        "path": "plugins\\recon\\lark\\plugin.py"
    },
    {
        "name": "ldap_injection",
        "category": "recon",
        "path": "plugins\\recon\\ldap_injection\\plugin.py"
    },
    {
        "name": "legacy",
        "category": "recon",
        "path": "plugins\\recon\\legacy\\plugin.py"
    },
    {
        "name": "LICENSE",
        "category": "recon",
        "path": "plugins\\recon\\LICENSE\\plugin.py"
    },
    {
        "name": "LICENSE_1",
        "category": "recon",
        "path": "plugins\\recon\\LICENSE_1\\plugin.py"
    },
    {
        "name": "LICENSE_10",
        "category": "recon",
        "path": "plugins\\recon\\LICENSE_10\\plugin.py"
    },
    {
        "name": "LICENSE_12",
        "category": "recon",
        "path": "plugins\\recon\\LICENSE_12\\plugin.py"
    },
    {
        "name": "LICENSE_13",
        "category": "recon",
        "path": "plugins\\recon\\LICENSE_13\\plugin.py"
    },
    {
        "name": "LICENSE_2",
        "category": "recon",
        "path": "plugins\\recon\\LICENSE_2\\plugin.py"
    },
    {
        "name": "LICENSE_4",
        "category": "recon",
        "path": "plugins\\recon\\LICENSE_4\\plugin.py"
    },
    {
        "name": "LICENSE_6",
        "category": "recon",
        "path": "plugins\\recon\\LICENSE_6\\plugin.py"
    },
    {
        "name": "LICENSE_7",
        "category": "recon",
        "path": "plugins\\recon\\LICENSE_7\\plugin.py"
    },
    {
        "name": "LICENSE_9",
        "category": "recon",
        "path": "plugins\\recon\\LICENSE_9\\plugin.py"
    },
    {
        "name": "llm",
        "category": "recon",
        "path": "plugins\\recon\\llm\\plugin.py"
    },
    {
        "name": "llm-analysis",
        "category": "recon",
        "path": "plugins\\recon\\llm-analysis\\plugin.py"
    },
    {
        "name": "llm-client",
        "category": "recon",
        "path": "plugins\\recon\\llm-client\\plugin.py"
    },
    {
        "name": "llm-clienttest",
        "category": "recon",
        "path": "plugins\\recon\\llm-clienttest\\plugin.py"
    },
    {
        "name": "llm-clienttest_1",
        "category": "recon",
        "path": "plugins\\recon\\llm-clienttest_1\\plugin.py"
    },
    {
        "name": "llm-client_1",
        "category": "recon",
        "path": "plugins\\recon\\llm-client_1\\plugin.py"
    },
    {
        "name": "llm_api",
        "category": "recon",
        "path": "plugins\\recon\\llm_api\\plugin.py"
    },
    {
        "name": "loader_1",
        "category": "recon",
        "path": "plugins\\recon\\loader_1\\plugin.py"
    },
    {
        "name": "LOCAL-SETUP",
        "category": "recon",
        "path": "plugins\\recon\\LOCAL-SETUP\\plugin.py"
    },
    {
        "name": "main_4",
        "category": "recon",
        "path": "plugins\\recon\\main_4\\plugin.py"
    },
    {
        "name": "main_5",
        "category": "recon",
        "path": "plugins\\recon\\main_5\\plugin.py"
    },
    {
        "name": "manager_2",
        "category": "recon",
        "path": "plugins\\recon\\manager_2\\plugin.py"
    },
    {
        "name": "markdown",
        "category": "recon",
        "path": "plugins\\recon\\markdown\\plugin.py"
    },
    {
        "name": "MarkdownRenderer",
        "category": "recon",
        "path": "plugins\\recon\\MarkdownRenderer\\plugin.py"
    },
    {
        "name": "markdown_agents",
        "category": "recon",
        "path": "plugins\\recon\\markdown_agents\\plugin.py"
    },
    {
        "name": "masscan",
        "category": "recon",
        "path": "plugins\\recon\\masscan\\plugin.py"
    },
    {
        "name": "masscan_2",
        "category": "recon",
        "path": "plugins\\recon\\masscan_2\\plugin.py"
    },
    {
        "name": "mass_assignment",
        "category": "recon",
        "path": "plugins\\recon\\mass_assignment\\plugin.py"
    },
    {
        "name": "mcp_client",
        "category": "recon",
        "path": "plugins\\recon\\mcp_client\\plugin.py"
    },
    {
        "name": "mcp_manager",
        "category": "recon",
        "path": "plugins\\recon\\mcp_manager\\plugin.py"
    },
    {
        "name": "mcp_setup",
        "category": "recon",
        "path": "plugins\\recon\\mcp_setup\\plugin.py"
    },
    {
        "name": "memory_compressor",
        "category": "recon",
        "path": "plugins\\recon\\memory_compressor\\plugin.py"
    },
    {
        "name": "message-handlers",
        "category": "recon",
        "path": "plugins\\recon\\message-handlers\\plugin.py"
    },
    {
        "name": "metrics-tracker",
        "category": "recon",
        "path": "plugins\\recon\\metrics-tracker\\plugin.py"
    },
    {
        "name": "models_1",
        "category": "recon",
        "path": "plugins\\recon\\models_1\\plugin.py"
    },
    {
        "name": "models_5",
        "category": "recon",
        "path": "plugins\\recon\\models_5\\plugin.py"
    },
    {
        "name": "module_import",
        "category": "recon",
        "path": "plugins\\recon\\module_import\\plugin.py"
    },
    {
        "name": "monitor",
        "category": "recon",
        "path": "plugins\\recon\\monitor\\plugin.py"
    },
    {
        "name": "multi_agent",
        "category": "recon",
        "path": "plugins\\recon\\multi_agent\\plugin.py"
    },
    {
        "name": "MULTI_AGENT_EINO",
        "category": "recon",
        "path": "plugins\\recon\\MULTI_AGENT_EINO\\plugin.py"
    },
    {
        "name": "nikto_tool",
        "category": "recon",
        "path": "plugins\\recon\\nikto_tool\\plugin.py"
    },
    {
        "name": "nmap-irc",
        "category": "recon",
        "path": "plugins\\recon\\nmap-irc\\plugin.py"
    },
    {
        "name": "notifications",
        "category": "recon",
        "path": "plugins\\recon\\notifications\\plugin.py"
    },
    {
        "name": "no_nested_task",
        "category": "recon",
        "path": "plugins\\recon\\no_nested_task\\plugin.py"
    },
    {
        "name": "ollama_api",
        "category": "recon",
        "path": "plugins\\recon\\ollama_api\\plugin.py"
    },
    {
        "name": "openai",
        "category": "recon",
        "path": "plugins\\recon\\openai\\plugin.py"
    },
    {
        "name": "openapi",
        "category": "recon",
        "path": "plugins\\recon\\openapi\\plugin.py"
    },
    {
        "name": "openapi-discovery-agent",
        "category": "recon",
        "path": "plugins\\recon\\openapi-discovery-agent\\plugin.py"
    },
    {
        "name": "openapi_i18n",
        "category": "recon",
        "path": "plugins\\recon\\openapi_i18n\\plugin.py"
    },
    {
        "name": "openapi_parser",
        "category": "recon",
        "path": "plugins\\recon\\openapi_parser\\plugin.py"
    },
    {
        "name": "open_ai",
        "category": "recon",
        "path": "plugins\\recon\\open_ai\\plugin.py"
    },
    {
        "name": "oracle-patator",
        "category": "recon",
        "path": "plugins\\recon\\oracle-patator\\plugin.py"
    },
    {
        "name": "orchestrator-plan-execute",
        "category": "recon",
        "path": "plugins\\recon\\orchestrator-plan-execute\\plugin.py"
    },
    {
        "name": "orchestrator-supervisor",
        "category": "recon",
        "path": "plugins\\recon\\orchestrator-supervisor\\plugin.py"
    },
    {
        "name": "orphan_tool_pruner_middleware",
        "category": "recon",
        "path": "plugins\\recon\\orphan_tool_pruner_middleware\\plugin.py"
    },
    {
        "name": "osrframework",
        "category": "recon",
        "path": "plugins\\recon\\osrframework\\plugin.py"
    },
    {
        "name": "package_1",
        "category": "recon",
        "path": "plugins\\recon\\package_1\\plugin.py"
    },
    {
        "name": "package_5",
        "category": "recon",
        "path": "plugins\\recon\\package_5\\plugin.py"
    },
    {
        "name": "parameter_mapper",
        "category": "recon",
        "path": "plugins\\recon\\parameter_mapper\\plugin.py"
    },
    {
        "name": "password_reset_weak",
        "category": "recon",
        "path": "plugins\\recon\\password_reset_weak\\plugin.py"
    },
    {
        "name": "path_traversal",
        "category": "recon",
        "path": "plugins\\recon\\path_traversal\\plugin.py"
    },
    {
        "name": "penetration",
        "category": "recon",
        "path": "plugins\\recon\\penetration\\plugin.py"
    },
    {
        "name": "pentest-ai",
        "category": "recon",
        "path": "plugins\\recon\\pentest-ai\\plugin.py"
    },
    {
        "name": "pentest_agent",
        "category": "recon",
        "path": "plugins\\recon\\pentest_agent\\plugin.py"
    },
    {
        "name": "pentest_gpt",
        "category": "recon",
        "path": "plugins\\recon\\pentest_gpt\\plugin.py"
    },
    {
        "name": "pentest_gpt_rebuilt",
        "category": "recon",
        "path": "plugins\\recon\\pentest_gpt_rebuilt\\plugin.py"
    },
    {
        "name": "pent_claude_agent_config",
        "category": "recon",
        "path": "plugins\\recon\\pent_claude_agent_config\\plugin.py"
    },
    {
        "name": "perplexity",
        "category": "recon",
        "path": "plugins\\recon\\perplexity\\plugin.py"
    },
    {
        "name": "persistencetest",
        "category": "recon",
        "path": "plugins\\recon\\persistencetest\\plugin.py"
    },
    {
        "name": "playwright-config-writer",
        "category": "recon",
        "path": "plugins\\recon\\playwright-config-writer\\plugin.py"
    },
    {
        "name": "plugin_loader_1",
        "category": "recon",
        "path": "plugins\\recon\\plugin_loader_1\\plugin.py"
    },
    {
        "name": "poc_agent",
        "category": "recon",
        "path": "plugins\\recon\\poc_agent\\plugin.py"
    },
    {
        "name": "pom",
        "category": "recon",
        "path": "plugins\\recon\\pom\\plugin.py"
    },
    {
        "name": "postman_parser",
        "category": "recon",
        "path": "plugins\\recon\\postman_parser\\plugin.py"
    },
    {
        "name": "pre-recon-code_2",
        "category": "recon",
        "path": "plugins\\recon\\pre-recon-code_2\\plugin.py"
    },
    {
        "name": "privilege_escalation_patch",
        "category": "recon",
        "path": "plugins\\recon\\privilege_escalation_patch\\plugin.py"
    },
    {
        "name": "project_manager",
        "category": "recon",
        "path": "plugins\\recon\\project_manager\\plugin.py"
    },
    {
        "name": "prototype_pollution",
        "category": "recon",
        "path": "plugins\\recon\\prototype_pollution\\plugin.py"
    },
    {
        "name": "pyproject",
        "category": "recon",
        "path": "plugins\\recon\\pyproject\\plugin.py"
    },
    {
        "name": "quake_search",
        "category": "recon",
        "path": "plugins\\recon\\quake_search\\plugin.py"
    },
    {
        "name": "queue",
        "category": "recon",
        "path": "plugins\\recon\\queue\\plugin.py"
    },
    {
        "name": "race_condition",
        "category": "recon",
        "path": "plugins\\recon\\race_condition\\plugin.py"
    },
    {
        "name": "reactive-verifier",
        "category": "recon",
        "path": "plugins\\recon\\reactive-verifier\\plugin.py"
    },
    {
        "name": "READMEzh-CN",
        "category": "recon",
        "path": "plugins\\recon\\READMEzh-CN\\plugin.py"
    },
    {
        "name": "README_10",
        "category": "recon",
        "path": "plugins\\recon\\README_10\\plugin.py"
    },
    {
        "name": "README_11",
        "category": "recon",
        "path": "plugins\\recon\\README_11\\plugin.py"
    },
    {
        "name": "README_13",
        "category": "recon",
        "path": "plugins\\recon\\README_13\\plugin.py"
    },
    {
        "name": "README_15",
        "category": "recon",
        "path": "plugins\\recon\\README_15\\plugin.py"
    },
    {
        "name": "README_32",
        "category": "recon",
        "path": "plugins\\recon\\README_32\\plugin.py"
    },
    {
        "name": "README_33",
        "category": "recon",
        "path": "plugins\\recon\\README_33\\plugin.py"
    },
    {
        "name": "README_38",
        "category": "recon",
        "path": "plugins\\recon\\README_38\\plugin.py"
    },
    {
        "name": "README_50",
        "category": "recon",
        "path": "plugins\\recon\\README_50\\plugin.py"
    },
    {
        "name": "README_54",
        "category": "recon",
        "path": "plugins\\recon\\README_54\\plugin.py"
    },
    {
        "name": "README_55",
        "category": "recon",
        "path": "plugins\\recon\\README_55\\plugin.py"
    },
    {
        "name": "README_CN_3",
        "category": "recon",
        "path": "plugins\\recon\\README_CN_3\\plugin.py"
    },
    {
        "name": "recon",
        "category": "recon",
        "path": "plugins\\recon\\recon\\plugin.py"
    },
    {
        "name": "reconx_engine",
        "category": "recon",
        "path": "plugins\\recon\\reconx_engine\\plugin.py"
    },
    {
        "name": "REFERENCE",
        "category": "recon",
        "path": "plugins\\recon\\REFERENCE\\plugin.py"
    },
    {
        "name": "reflected_xss",
        "category": "recon",
        "path": "plugins\\recon\\reflected_xss\\plugin.py"
    },
    {
        "name": "registry",
        "category": "recon",
        "path": "plugins\\recon\\registry\\plugin.py"
    },
    {
        "name": "release-pypi",
        "category": "recon",
        "path": "plugins\\recon\\release-pypi\\plugin.py"
    },
    {
        "name": "replay",
        "category": "recon",
        "path": "plugins\\recon\\replay\\plugin.py"
    },
    {
        "name": "report-snippet",
        "category": "recon",
        "path": "plugins\\recon\\report-snippet\\plugin.py"
    },
    {
        "name": "report_18",
        "category": "recon",
        "path": "plugins\\recon\\report_18\\plugin.py"
    },
    {
        "name": "report_injector",
        "category": "recon",
        "path": "plugins\\recon\\report_injector\\plugin.py"
    },
    {
        "name": "report_injector_1",
        "category": "recon",
        "path": "plugins\\recon\\report_injector_1\\plugin.py"
    },
    {
        "name": "requirements_6",
        "category": "recon",
        "path": "plugins\\recon\\requirements_6\\plugin.py"
    },
    {
        "name": "reset_juice_shop",
        "category": "recon",
        "path": "plugins\\recon\\reset_juice_shop\\plugin.py"
    },
    {
        "name": "retrieval_postprocess",
        "category": "recon",
        "path": "plugins\\recon\\retrieval_postprocess\\plugin.py"
    },
    {
        "name": "retry",
        "category": "recon",
        "path": "plugins\\recon\\retry\\plugin.py"
    },
    {
        "name": "review",
        "category": "recon",
        "path": "plugins\\recon\\review\\plugin.py"
    },
    {
        "name": "robot",
        "category": "recon",
        "path": "plugins\\recon\\robot\\plugin.py"
    },
    {
        "name": "robot_en",
        "category": "recon",
        "path": "plugins\\recon\\robot_en\\plugin.py"
    },
    {
        "name": "roles",
        "category": "recon",
        "path": "plugins\\recon\\roles\\plugin.py"
    },
    {
        "name": "route_correlator",
        "category": "recon",
        "path": "plugins\\recon\\route_correlator\\plugin.py"
    },
    {
        "name": "RunCommand",
        "category": "recon",
        "path": "plugins\\recon\\RunCommand\\plugin.py"
    },
    {
        "name": "runner",
        "category": "recon",
        "path": "plugins\\recon\\runner\\plugin.py"
    },
    {
        "name": "saml_xsw",
        "category": "recon",
        "path": "plugins\\recon\\saml_xsw\\plugin.py"
    },
    {
        "name": "sandbox",
        "category": "recon",
        "path": "plugins\\recon\\sandbox\\plugin.py"
    },
    {
        "name": "sanitize",
        "category": "recon",
        "path": "plugins\\recon\\sanitize\\plugin.py"
    },
    {
        "name": "schedulertest",
        "category": "recon",
        "path": "plugins\\recon\\schedulertest\\plugin.py"
    },
    {
        "name": "scheduler_2",
        "category": "recon",
        "path": "plugins\\recon\\scheduler_2\\plugin.py"
    },
    {
        "name": "schema-gen-agent",
        "category": "recon",
        "path": "plugins\\recon\\schema-gen-agent\\plugin.py"
    },
    {
        "name": "scope",
        "category": "recon",
        "path": "plugins\\recon\\scope\\plugin.py"
    },
    {
        "name": "search",
        "category": "recon",
        "path": "plugins\\recon\\search\\plugin.py"
    },
    {
        "name": "SecurityHeaderAnalyzertest",
        "category": "recon",
        "path": "plugins\\recon\\SecurityHeaderAnalyzertest\\plugin.py"
    },
    {
        "name": "server",
        "category": "recon",
        "path": "plugins\\recon\\server\\plugin.py"
    },
    {
        "name": "service",
        "category": "recon",
        "path": "plugins\\recon\\service\\plugin.py"
    },
    {
        "name": "services_commands",
        "category": "recon",
        "path": "plugins\\recon\\services_commands\\plugin.py"
    },
    {
        "name": "service_intelligence_view",
        "category": "recon",
        "path": "plugins\\recon\\service_intelligence_view\\plugin.py"
    },
    {
        "name": "settings",
        "category": "recon",
        "path": "plugins\\recon\\settings\\plugin.py"
    },
    {
        "name": "shared",
        "category": "recon",
        "path": "plugins\\recon\\shared\\plugin.py"
    },
    {
        "name": "sherlock",
        "category": "recon",
        "path": "plugins\\recon\\sherlock\\plugin.py"
    },
    {
        "name": "shodan_api",
        "category": "recon",
        "path": "plugins\\recon\\shodan_api\\plugin.py"
    },
    {
        "name": "shodan_apicpython-313",
        "category": "recon",
        "path": "plugins\\recon\\shodan_apicpython-313\\plugin.py"
    },
    {
        "name": "shodan_search",
        "category": "recon",
        "path": "plugins\\recon\\shodan_search\\plugin.py"
    },
    {
        "name": "sitemap-agent",
        "category": "recon",
        "path": "plugins\\recon\\sitemap-agent\\plugin.py"
    },
    {
        "name": "SKILL",
        "category": "recon",
        "path": "plugins\\recon\\SKILL\\plugin.py"
    },
    {
        "name": "SKILL_11",
        "category": "recon",
        "path": "plugins\\recon\\SKILL_11\\plugin.py"
    },
    {
        "name": "SKILL_13",
        "category": "recon",
        "path": "plugins\\recon\\SKILL_13\\plugin.py"
    },
    {
        "name": "SKILL_3",
        "category": "recon",
        "path": "plugins\\recon\\SKILL_3\\plugin.py"
    },
    {
        "name": "SKILL_7",
        "category": "recon",
        "path": "plugins\\recon\\SKILL_7\\plugin.py"
    },
    {
        "name": "SKILL_9",
        "category": "recon",
        "path": "plugins\\recon\\SKILL_9\\plugin.py"
    },
    {
        "name": "source-gen-agent",
        "category": "recon",
        "path": "plugins\\recon\\source-gen-agent\\plugin.py"
    },
    {
        "name": "ssti_polyglot",
        "category": "recon",
        "path": "plugins\\recon\\ssti_polyglot\\plugin.py"
    },
    {
        "name": "status",
        "category": "recon",
        "path": "plugins\\recon\\status\\plugin.py"
    },
    {
        "name": "stored_xss",
        "category": "recon",
        "path": "plugins\\recon\\stored_xss\\plugin.py"
    },
    {
        "name": "style",
        "category": "recon",
        "path": "plugins\\recon\\style\\plugin.py"
    },
    {
        "name": "sub_agent_context",
        "category": "recon",
        "path": "plugins\\recon\\sub_agent_context\\plugin.py"
    },
    {
        "name": "sub_agent_context_test",
        "category": "recon",
        "path": "plugins\\recon\\sub_agent_context_test\\plugin.py"
    },
    {
        "name": "SUMMARY",
        "category": "recon",
        "path": "plugins\\recon\\SUMMARY\\plugin.py"
    },
    {
        "name": "swagger_2",
        "category": "recon",
        "path": "plugins\\recon\\swagger_2\\plugin.py"
    },
    {
        "name": "swagger_parser",
        "category": "recon",
        "path": "plugins\\recon\\swagger_parser\\plugin.py"
    },
    {
        "name": "tasks",
        "category": "recon",
        "path": "plugins\\recon\\tasks\\plugin.py"
    },
    {
        "name": "telemetry",
        "category": "recon",
        "path": "plugins\\recon\\telemetry\\plugin.py"
    },
    {
        "name": "terminal",
        "category": "recon",
        "path": "plugins\\recon\\terminal\\plugin.py"
    },
    {
        "name": "test-cortex-integration",
        "category": "recon",
        "path": "plugins\\recon\\test-cortex-integration\\plugin.py"
    },
    {
        "name": "test-gen-agent",
        "category": "recon",
        "path": "plugins\\recon\\test-gen-agent\\plugin.py"
    },
    {
        "name": "testLogin",
        "category": "recon",
        "path": "plugins\\recon\\testLogin\\plugin.py"
    },
    {
        "name": "test_agent_loop",
        "category": "recon",
        "path": "plugins\\recon\\test_agent_loop\\plugin.py"
    },
    {
        "name": "test_agent_mode_cli",
        "category": "recon",
        "path": "plugins\\recon\\test_agent_mode_cli\\plugin.py"
    },
    {
        "name": "test_anthropic_agent",
        "category": "recon",
        "path": "plugins\\recon\\test_anthropic_agent\\plugin.py"
    },
    {
        "name": "test_auth_profiles",
        "category": "recon",
        "path": "plugins\\recon\\test_auth_profiles\\plugin.py"
    },
    {
        "name": "test_auth_profile_cli",
        "category": "recon",
        "path": "plugins\\recon\\test_auth_profile_cli\\plugin.py"
    },
    {
        "name": "test_auth_runner",
        "category": "recon",
        "path": "plugins\\recon\\test_auth_runner\\plugin.py"
    },
    {
        "name": "test_benchmarks_scoring_common",
        "category": "recon",
        "path": "plugins\\recon\\test_benchmarks_scoring_common\\plugin.py"
    },
    {
        "name": "test_browser_agent",
        "category": "recon",
        "path": "plugins\\recon\\test_browser_agent\\plugin.py"
    },
    {
        "name": "test_chain",
        "category": "recon",
        "path": "plugins\\recon\\test_chain\\plugin.py"
    },
    {
        "name": "test_chain_quality",
        "category": "recon",
        "path": "plugins\\recon\\test_chain_quality\\plugin.py"
    },
    {
        "name": "test_config",
        "category": "recon",
        "path": "plugins\\recon\\test_config\\plugin.py"
    },
    {
        "name": "test_connection",
        "category": "recon",
        "path": "plugins\\recon\\test_connection\\plugin.py"
    },
    {
        "name": "test_handler_web_probes",
        "category": "recon",
        "path": "plugins\\recon\\test_handler_web_probes\\plugin.py"
    },
    {
        "name": "test_langfuse_1",
        "category": "recon",
        "path": "plugins\\recon\\test_langfuse_1\\plugin.py"
    },
    {
        "name": "test_legacy_probe_migration",
        "category": "recon",
        "path": "plugins\\recon\\test_legacy_probe_migration\\plugin.py"
    },
    {
        "name": "test_llm",
        "category": "recon",
        "path": "plugins\\recon\\test_llm\\plugin.py"
    },
    {
        "name": "test_llm_e2e_smoke",
        "category": "recon",
        "path": "plugins\\recon\\test_llm_e2e_smoke\\plugin.py"
    },
    {
        "name": "test_mcp_action_surface",
        "category": "recon",
        "path": "plugins\\recon\\test_mcp_action_surface\\plugin.py"
    },
    {
        "name": "test_new_high_roi_probes",
        "category": "recon",
        "path": "plugins\\recon\\test_new_high_roi_probes\\plugin.py"
    },
    {
        "name": "test_probe_cors_reflection",
        "category": "recon",
        "path": "plugins\\recon\\test_probe_cors_reflection\\plugin.py"
    },
    {
        "name": "test_probe_coupon_forging",
        "category": "recon",
        "path": "plugins\\recon\\test_probe_coupon_forging\\plugin.py"
    },
    {
        "name": "test_probe_cve_poc",
        "category": "recon",
        "path": "plugins\\recon\\test_probe_cve_poc\\plugin.py"
    },
    {
        "name": "test_probe_deserialization",
        "category": "recon",
        "path": "plugins\\recon\\test_probe_deserialization\\plugin.py"
    },
    {
        "name": "test_probe_dom_xss",
        "category": "recon",
        "path": "plugins\\recon\\test_probe_dom_xss\\plugin.py"
    },
    {
        "name": "test_probe_file_upload_validation",
        "category": "recon",
        "path": "plugins\\recon\\test_probe_file_upload_validation\\plugin.py"
    },
    {
        "name": "test_probe_forced_error",
        "category": "recon",
        "path": "plugins\\recon\\test_probe_forced_error\\plugin.py"
    },
    {
        "name": "test_probe_graphql_introspection",
        "category": "recon",
        "path": "plugins\\recon\\test_probe_graphql_introspection\\plugin.py"
    },
    {
        "name": "test_probe_hidden_discovery",
        "category": "recon",
        "path": "plugins\\recon\\test_probe_hidden_discovery\\plugin.py"
    },
    {
        "name": "test_probe_host_header_reset_poisoning",
        "category": "recon",
        "path": "plugins\\recon\\test_probe_host_header_reset_poisoning\\plugin.py"
    },
    {
        "name": "test_probe_idor_authenticated",
        "category": "recon",
        "path": "plugins\\recon\\test_probe_idor_authenticated\\plugin.py"
    },
    {
        "name": "test_probe_idor_authz_differential",
        "category": "recon",
        "path": "plugins\\recon\\test_probe_idor_authz_differential\\plugin.py"
    },
    {
        "name": "test_probe_idor_sequential",
        "category": "recon",
        "path": "plugins\\recon\\test_probe_idor_sequential\\plugin.py"
    },
    {
        "name": "test_probe_ldap_injection",
        "category": "recon",
        "path": "plugins\\recon\\test_probe_ldap_injection\\plugin.py"
    },
    {
        "name": "test_probe_mass_assignment",
        "category": "recon",
        "path": "plugins\\recon\\test_probe_mass_assignment\\plugin.py"
    },
    {
        "name": "test_probe_path_traversal",
        "category": "recon",
        "path": "plugins\\recon\\test_probe_path_traversal\\plugin.py"
    },
    {
        "name": "test_probe_primitives",
        "category": "recon",
        "path": "plugins\\recon\\test_probe_primitives\\plugin.py"
    },
    {
        "name": "test_probe_prototype_pollution",
        "category": "recon",
        "path": "plugins\\recon\\test_probe_prototype_pollution\\plugin.py"
    },
    {
        "name": "test_probe_race_condition",
        "category": "recon",
        "path": "plugins\\recon\\test_probe_race_condition\\plugin.py"
    },
    {
        "name": "test_probe_reflected_xss",
        "category": "recon",
        "path": "plugins\\recon\\test_probe_reflected_xss\\plugin.py"
    },
    {
        "name": "test_probe_registry",
        "category": "recon",
        "path": "plugins\\recon\\test_probe_registry\\plugin.py"
    },
    {
        "name": "test_probe_ssti_stored",
        "category": "recon",
        "path": "plugins\\recon\\test_probe_ssti_stored\\plugin.py"
    },
    {
        "name": "test_probe_stored_xss",
        "category": "recon",
        "path": "plugins\\recon\\test_probe_stored_xss\\plugin.py"
    },
    {
        "name": "test_probe_web3",
        "category": "recon",
        "path": "plugins\\recon\\test_probe_web3\\plugin.py"
    },
    {
        "name": "test_probe_web_cache_deception",
        "category": "recon",
        "path": "plugins\\recon\\test_probe_web_cache_deception\\plugin.py"
    },
    {
        "name": "test_probe_xxe_upload",
        "category": "recon",
        "path": "plugins\\recon\\test_probe_xxe_upload\\plugin.py"
    },
    {
        "name": "test_providers",
        "category": "recon",
        "path": "plugins\\recon\\test_providers\\plugin.py"
    },
    {
        "name": "test_registry_bridge",
        "category": "recon",
        "path": "plugins\\recon\\test_registry_bridge\\plugin.py"
    },
    {
        "name": "test_scope",
        "category": "recon",
        "path": "plugins\\recon\\test_scope\\plugin.py"
    },
    {
        "name": "test_spa_probes",
        "category": "recon",
        "path": "plugins\\recon\\test_spa_probes\\plugin.py"
    },
    {
        "name": "test_specialist_agents_coverage",
        "category": "recon",
        "path": "plugins\\recon\\test_specialist_agents_coverage\\plugin.py"
    },
    {
        "name": "test_stage1",
        "category": "recon",
        "path": "plugins\\recon\\test_stage1\\plugin.py"
    },
    {
        "name": "test_tracing_and_telemetry",
        "category": "recon",
        "path": "plugins\\recon\\test_tracing_and_telemetry\\plugin.py"
    },
    {
        "name": "test_working_memory",
        "category": "recon",
        "path": "plugins\\recon\\test_working_memory\\plugin.py"
    },
    {
        "name": "tracing",
        "category": "recon",
        "path": "plugins\\recon\\tracing\\plugin.py"
    },
    {
        "name": "traffic_parser",
        "category": "recon",
        "path": "plugins\\recon\\traffic_parser\\plugin.py"
    },
    {
        "name": "train-filternet",
        "category": "recon",
        "path": "plugins\\recon\\train-filternet\\plugin.py"
    },
    {
        "name": "train-simple",
        "category": "recon",
        "path": "plugins\\recon\\train-simple\\plugin.py"
    },
    {
        "name": "TROUBLESHOOTING",
        "category": "recon",
        "path": "plugins\\recon\\TROUBLESHOOTING\\plugin.py"
    },
    {
        "name": "truncate",
        "category": "recon",
        "path": "plugins\\recon\\truncate\\plugin.py"
    },
    {
        "name": "trusted_header_bypass",
        "category": "recon",
        "path": "plugins\\recon\\trusted_header_bypass\\plugin.py"
    },
    {
        "name": "types",
        "category": "recon",
        "path": "plugins\\recon\\types\\plugin.py"
    },
    {
        "name": "unauthed-decision-log",
        "category": "recon",
        "path": "plugins\\recon\\unauthed-decision-log\\plugin.py"
    },
    {
        "name": "upgrade",
        "category": "recon",
        "path": "plugins\\recon\\upgrade\\plugin.py"
    },
    {
        "name": "urlscan",
        "category": "recon",
        "path": "plugins\\recon\\urlscan\\plugin.py"
    },
    {
        "name": "utils_2",
        "category": "recon",
        "path": "plugins\\recon\\utils_2\\plugin.py"
    },
    {
        "name": "vuln-auth_3",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\vuln-auth_3\\plugin.py"
    },
    {
        "name": "vuln-ssrf_3",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\vuln-ssrf_3\\plugin.py"
    },
    {
        "name": "vulnerability",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\vulnerability\\plugin.py"
    },
    {
        "name": "wayback",
        "category": "recon",
        "path": "plugins\\recon\\wayback\\plugin.py"
    },
    {
        "name": "waybackurls",
        "category": "recon",
        "path": "plugins\\recon\\waybackurls\\plugin.py"
    },
    {
        "name": "web3_probe",
        "category": "recon",
        "path": "plugins\\recon\\web3_probe\\plugin.py"
    },
    {
        "name": "webshell",
        "category": "recon",
        "path": "plugins\\recon\\webshell\\plugin.py"
    },
    {
        "name": "web_intelligence_view",
        "category": "recon",
        "path": "plugins\\recon\\web_intelligence_view\\plugin.py"
    },
    {
        "name": "web_parser",
        "category": "recon",
        "path": "plugins\\recon\\web_parser\\plugin.py"
    },
    {
        "name": "web_probes",
        "category": "recon",
        "path": "plugins\\recon\\web_probes\\plugin.py"
    },
    {
        "name": "wechat-robot",
        "category": "recon",
        "path": "plugins\\recon\\wechat-robot\\plugin.py"
    },
    {
        "name": "wechat_robot",
        "category": "recon",
        "path": "plugins\\recon\\wechat_robot\\plugin.py"
    },
    {
        "name": "wordlist",
        "category": "recon",
        "path": "plugins\\recon\\wordlist\\plugin.py"
    },
    {
        "name": "workflow-errors",
        "category": "recon",
        "path": "plugins\\recon\\workflow-errors\\plugin.py"
    },
    {
        "name": "workflows",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\workflows\\plugin.py"
    },
    {
        "name": "workflow_engine_1",
        "category": "recon",
        "path": "plugins\\recon\\workflow_engine_1\\plugin.py"
    },
    {
        "name": "wpscan",
        "category": "recon",
        "path": "plugins\\recon\\wpscan\\plugin.py"
    },
    {
        "name": "writer",
        "category": "recon",
        "path": "plugins\\recon\\writer\\plugin.py"
    },
    {
        "name": "xxe_upload",
        "category": "recon",
        "path": "plugins\\recon\\xxe_upload\\plugin.py"
    },
    {
        "name": "zap",
        "category": "recon",
        "path": "plugins\\recon\\zap\\plugin.py"
    },
    {
        "name": "__init___112",
        "category": "recon",
        "path": "plugins\\recon\\__init___112\\plugin.py"
    },
    {
        "name": "__init___115",
        "category": "recon",
        "path": "plugins\\recon\\__init___115\\plugin.py"
    },
    {
        "name": "__init___116",
        "category": "recon",
        "path": "plugins\\recon\\__init___116\\plugin.py"
    },
    {
        "name": "__init___142",
        "category": "recon",
        "path": "plugins\\recon\\__init___142\\plugin.py"
    },
    {
        "name": "__init___146",
        "category": "recon",
        "path": "plugins\\recon\\__init___146\\plugin.py"
    },
    {
        "name": "__init___153",
        "category": "recon",
        "path": "plugins\\recon\\__init___153\\plugin.py"
    },
    {
        "name": "__init___203",
        "category": "recon",
        "path": "plugins\\recon\\__init___203\\plugin.py"
    },
    {
        "name": "__init___22",
        "category": "recon",
        "path": "plugins\\recon\\__init___22\\plugin.py"
    },
    {
        "name": "__init___34",
        "category": "recon",
        "path": "plugins\\recon\\__init___34\\plugin.py"
    },
    {
        "name": "__init___64",
        "category": "recon",
        "path": "plugins\\recon\\__init___64\\plugin.py"
    },
    {
        "name": "builtin-tools",
        "category": "recon",
        "path": "plugins\\recon\\builtin-tools\\plugin.py"
    },
    {
        "name": "CyberStrikeAIClientStreamListener",
        "category": "recon",
        "path": "plugins\\recon\\CyberStrikeAIClientStreamListener\\plugin.py"
    },
    {
        "name": "CyberStrikeAITab1",
        "category": "recon",
        "path": "plugins\\recon\\CyberStrikeAITab1\\plugin.py"
    },
    {
        "name": "CyberStrikeAITabDotIcon",
        "category": "recon",
        "path": "plugins\\recon\\CyberStrikeAITabDotIcon\\plugin.py"
    },
    {
        "name": "headers_inject",
        "category": "recon",
        "path": "plugins\\recon\\headers_inject\\plugin.py"
    },
    {
        "name": "hexstrike-ai-mcp",
        "category": "recon",
        "path": "plugins\\recon\\hexstrike-ai-mcp\\plugin.py"
    },
    {
        "name": "main",
        "category": "recon",
        "path": "plugins\\recon\\main\\plugin.py"
    },
    {
        "name": "mcp",
        "category": "recon",
        "path": "plugins\\recon\\mcp\\plugin.py"
    },
    {
        "name": "mcp_tools_test",
        "category": "recon",
        "path": "plugins\\recon\\mcp_tools_test\\plugin.py"
    },
    {
        "name": "monitor_1",
        "category": "recon",
        "path": "plugins\\recon\\monitor_1\\plugin.py"
    },
    {
        "name": "options",
        "category": "recon",
        "path": "plugins\\recon\\options\\plugin.py"
    },
    {
        "name": "README_6",
        "category": "recon",
        "path": "plugins\\recon\\README_6\\plugin.py"
    },
    {
        "name": "SimpleJson",
        "category": "recon",
        "path": "plugins\\recon\\SimpleJson\\plugin.py"
    },
    {
        "name": "sse_keepalive",
        "category": "recon",
        "path": "plugins\\recon\\sse_keepalive\\plugin.py"
    },
    {
        "name": "SslTrustAll1",
        "category": "recon",
        "path": "plugins\\recon\\SslTrustAll1\\plugin.py"
    },
    {
        "name": "SslTrustAllTimeoutSslSocketFactory",
        "category": "recon",
        "path": "plugins\\recon\\SslTrustAllTimeoutSslSocketFactory\\plugin.py"
    },
    {
        "name": "test_file_transfer",
        "category": "recon",
        "path": "plugins\\recon\\test_file_transfer\\plugin.py"
    },
    {
        "name": "test_handlers_misc",
        "category": "recon",
        "path": "plugins\\recon\\test_handlers_misc\\plugin.py"
    },
    {
        "name": "__init___38",
        "category": "recon",
        "path": "plugins\\recon\\__init___38\\plugin.py"
    },
    {
        "name": "__init___55",
        "category": "recon",
        "path": "plugins\\recon\\__init___55\\plugin.py"
    },
    {
        "name": "__main__",
        "category": "recon",
        "path": "plugins\\recon\\__main__\\plugin.py"
    },
    {
        "name": "404StarLinkLogo",
        "category": "cloud",
        "path": "plugins\\cloud\\404StarLinkLogo\\plugin.py"
    },
    {
        "name": "agent-management",
        "category": "cloud",
        "path": "plugins\\cloud\\agent-management\\plugin.py"
    },
    {
        "name": "agents-for",
        "category": "cloud",
        "path": "plugins\\cloud\\agents-for\\plugin.py"
    },
    {
        "name": "ai_analysis",
        "category": "cloud",
        "path": "plugins\\cloud\\ai_analysis\\plugin.py"
    },
    {
        "name": "alterations",
        "category": "cloud",
        "path": "plugins\\cloud\\alterations\\plugin.py"
    },
    {
        "name": "announcements",
        "category": "cloud",
        "path": "plugins\\cloud\\announcements\\plugin.py"
    },
    {
        "name": "AUP",
        "category": "cloud",
        "path": "plugins\\cloud\\AUP\\plugin.py"
    },
    {
        "name": "auth_profiles",
        "category": "cloud",
        "path": "plugins\\cloud\\auth_profiles\\plugin.py"
    },
    {
        "name": "aws",
        "category": "cloud",
        "path": "plugins\\cloud\\aws\\plugin.py"
    },
    {
        "name": "aws_sm",
        "category": "cloud",
        "path": "plugins\\cloud\\aws_sm\\plugin.py"
    },
    {
        "name": "azure",
        "category": "cloud",
        "path": "plugins\\cloud\\azure\\plugin.py"
    },
    {
        "name": "azure_recon",
        "category": "cloud",
        "path": "plugins\\cloud\\azure_recon\\plugin.py"
    },
    {
        "name": "banner_2",
        "category": "cloud",
        "path": "plugins\\cloud\\banner_2\\plugin.py"
    },
    {
        "name": "benchmark_runner",
        "category": "cloud",
        "path": "plugins\\cloud\\benchmark_runner\\plugin.py"
    },
    {
        "name": "bizlogic-hunter",
        "category": "cloud",
        "path": "plugins\\cloud\\bizlogic-hunter\\plugin.py"
    },
    {
        "name": "bucket_correlator",
        "category": "cloud",
        "path": "plugins\\cloud\\bucket_correlator\\plugin.py"
    },
    {
        "name": "bug_report",
        "category": "cloud",
        "path": "plugins\\cloud\\bug_report\\plugin.py"
    },
    {
        "name": "ccr-config-template",
        "category": "cloud",
        "path": "plugins\\cloud\\ccr-config-template\\plugin.py"
    },
    {
        "name": "chat",
        "category": "cloud",
        "path": "plugins\\cloud\\chat\\plugin.py"
    },
    {
        "name": "chatgpt_config_curl",
        "category": "cloud",
        "path": "plugins\\cloud\\chatgpt_config_curl\\plugin.py"
    },
    {
        "name": "ChatGPT_key",
        "category": "cloud",
        "path": "plugins\\cloud\\ChatGPT_key\\plugin.py"
    },
    {
        "name": "checkov",
        "category": "cloud",
        "path": "plugins\\cloud\\checkov\\plugin.py"
    },
    {
        "name": "ci_1",
        "category": "cloud",
        "path": "plugins\\cloud\\ci_1\\plugin.py"
    },
    {
        "name": "ci_cd_cloud",
        "category": "cloud",
        "path": "plugins\\cloud\\ci_cd_cloud\\plugin.py"
    },
    {
        "name": "ci_cd_cloud_mapper",
        "category": "cloud",
        "path": "plugins\\cloud\\ci_cd_cloud_mapper\\plugin.py"
    },
    {
        "name": "claude-executor",
        "category": "cloud",
        "path": "plugins\\cloud\\claude-executor\\plugin.py"
    },
    {
        "name": "CLAUDE_2",
        "category": "cloud",
        "path": "plugins\\cloud\\CLAUDE_2\\plugin.py"
    },
    {
        "name": "CLAUDE_3",
        "category": "cloud",
        "path": "plugins\\cloud\\CLAUDE_3\\plugin.py"
    },
    {
        "name": "clear",
        "category": "cloud",
        "path": "plugins\\cloud\\clear\\plugin.py"
    },
    {
        "name": "cli",
        "category": "cloud",
        "path": "plugins\\cloud\\cli\\plugin.py"
    },
    {
        "name": "cloud-security",
        "category": "cloud",
        "path": "plugins\\cloud\\cloud-security\\plugin.py"
    },
    {
        "name": "cloudfront_mapper",
        "category": "cloud",
        "path": "plugins\\cloud\\cloudfront_mapper\\plugin.py"
    },
    {
        "name": "cloudmapper",
        "category": "cloud",
        "path": "plugins\\cloud\\cloudmapper\\plugin.py"
    },
    {
        "name": "cloud_agent",
        "category": "cloud",
        "path": "plugins\\cloud\\cloud_agent\\plugin.py"
    },
    {
        "name": "cloud_attack_surface",
        "category": "cloud",
        "path": "plugins\\cloud\\cloud_attack_surface\\plugin.py"
    },
    {
        "name": "cloud_storage",
        "category": "cloud",
        "path": "plugins\\cloud\\cloud_storage\\plugin.py"
    },
    {
        "name": "conftest_2",
        "category": "cloud",
        "path": "plugins\\cloud\\conftest_2\\plugin.py"
    },
    {
        "name": "container-breakout",
        "category": "cloud",
        "path": "plugins\\cloud\\container-breakout\\plugin.py"
    },
    {
        "name": "CUSTOMIZATION",
        "category": "cloud",
        "path": "plugins\\cloud\\CUSTOMIZATION\\plugin.py"
    },
    {
        "name": "CyberStrikeAITab",
        "category": "cloud",
        "path": "plugins\\cloud\\CyberStrikeAITab\\plugin.py"
    },
    {
        "name": "dec-2025",
        "category": "cloud",
        "path": "plugins\\cloud\\dec-2025\\plugin.py"
    },
    {
        "name": "demo",
        "category": "cloud",
        "path": "plugins\\cloud\\demo\\plugin.py"
    },
    {
        "name": "demo_1",
        "category": "cloud",
        "path": "plugins\\cloud\\demo_1\\plugin.py"
    },
    {
        "name": "dependabot_3",
        "category": "cloud",
        "path": "plugins\\cloud\\dependabot_3\\plugin.py"
    },
    {
        "name": "devcontainer",
        "category": "cloud",
        "path": "plugins\\cloud\\devcontainer\\plugin.py"
    },
    {
        "name": "DISCLAIMER",
        "category": "cloud",
        "path": "plugins\\cloud\\DISCLAIMER\\plugin.py"
    },
    {
        "name": "docker",
        "category": "cloud",
        "path": "plugins\\cloud\\docker\\plugin.py"
    },
    {
        "name": "docker-compose",
        "category": "cloud",
        "path": "plugins\\cloud\\docker-compose\\plugin.py"
    },
    {
        "name": "docker-compose_1",
        "category": "cloud",
        "path": "plugins\\cloud\\docker-compose_1\\plugin.py"
    },
    {
        "name": "docker-compose_2",
        "category": "cloud",
        "path": "plugins\\cloud\\docker-compose_2\\plugin.py"
    },
    {
        "name": "docker-compose_3",
        "category": "cloud",
        "path": "plugins\\cloud\\docker-compose_3\\plugin.py"
    },
    {
        "name": "Dockerfile_4",
        "category": "cloud",
        "path": "plugins\\cloud\\Dockerfile_4\\plugin.py"
    },
    {
        "name": "Dockerfile_7",
        "category": "cloud",
        "path": "plugins\\cloud\\Dockerfile_7\\plugin.py"
    },
    {
        "name": "Dockerfile_9",
        "category": "cloud",
        "path": "plugins\\cloud\\Dockerfile_9\\plugin.py"
    },
    {
        "name": "docker_2",
        "category": "cloud",
        "path": "plugins\\cloud\\docker_2\\plugin.py"
    },
    {
        "name": "docker_manager",
        "category": "cloud",
        "path": "plugins\\cloud\\docker_manager\\plugin.py"
    },
    {
        "name": "docker_nightly",
        "category": "cloud",
        "path": "plugins\\cloud\\docker_nightly\\plugin.py"
    },
    {
        "name": "docker_registry_analyzer",
        "category": "cloud",
        "path": "plugins\\cloud\\docker_registry_analyzer\\plugin.py"
    },
    {
        "name": "domains",
        "category": "cloud",
        "path": "plugins\\cloud\\domains\\plugin.py"
    },
    {
        "name": "embedder",
        "category": "cloud",
        "path": "plugins\\cloud\\embedder\\plugin.py"
    },
    {
        "name": "engagement-planner",
        "category": "cloud",
        "path": "plugins\\cloud\\engagement-planner\\plugin.py"
    },
    {
        "name": "entrypoint",
        "category": "cloud",
        "path": "plugins\\cloud\\entrypoint\\plugin.py"
    },
    {
        "name": "env",
        "category": "cloud",
        "path": "plugins\\cloud\\env\\plugin.py"
    },
    {
        "name": "env_3",
        "category": "cloud",
        "path": "plugins\\cloud\\env_3\\plugin.py"
    },
    {
        "name": "example-stig-finding",
        "category": "cloud",
        "path": "plugins\\cloud\\example-stig-finding\\plugin.py"
    },
    {
        "name": "executor_test",
        "category": "cloud",
        "path": "plugins\\cloud\\executor_test\\plugin.py"
    },
    {
        "name": "exploit-auth",
        "category": "cloud",
        "path": "plugins\\cloud\\exploit-auth\\plugin.py"
    },
    {
        "name": "exploit-authz",
        "category": "cloud",
        "path": "plugins\\cloud\\exploit-authz\\plugin.py"
    },
    {
        "name": "exploit-authz_2",
        "category": "cloud",
        "path": "plugins\\cloud\\exploit-authz_2\\plugin.py"
    },
    {
        "name": "exploit-auth_2",
        "category": "cloud",
        "path": "plugins\\cloud\\exploit-auth_2\\plugin.py"
    },
    {
        "name": "exploit-injection",
        "category": "cloud",
        "path": "plugins\\cloud\\exploit-injection\\plugin.py"
    },
    {
        "name": "exploit-xss",
        "category": "cloud",
        "path": "plugins\\cloud\\exploit-xss\\plugin.py"
    },
    {
        "name": "exploit-xss_2",
        "category": "cloud",
        "path": "plugins\\cloud\\exploit-xss_2\\plugin.py"
    },
    {
        "name": "export_menu",
        "category": "cloud",
        "path": "plugins\\cloud\\export_menu\\plugin.py"
    },
    {
        "name": "factory",
        "category": "cloud",
        "path": "plugins\\cloud\\factory\\plugin.py"
    },
    {
        "name": "fill-legal",
        "category": "cloud",
        "path": "plugins\\cloud\\fill-legal\\plugin.py"
    },
    {
        "name": "fingerprinter",
        "category": "cloud",
        "path": "plugins\\cloud\\fingerprinter\\plugin.py"
    },
    {
        "name": "fingerprintertest",
        "category": "cloud",
        "path": "plugins\\cloud\\fingerprintertest\\plugin.py"
    },
    {
        "name": "fix-workspace-permissions",
        "category": "cloud",
        "path": "plugins\\cloud\\fix-workspace-permissions\\plugin.py"
    },
    {
        "name": "gcp",
        "category": "cloud",
        "path": "plugins\\cloud\\gcp\\plugin.py"
    },
    {
        "name": "gcp_recon",
        "category": "cloud",
        "path": "plugins\\cloud\\gcp_recon\\plugin.py"
    },
    {
        "name": "github-banner",
        "category": "cloud",
        "path": "plugins\\cloud\\github-banner\\plugin.py"
    },
    {
        "name": "gitleaks",
        "category": "cloud",
        "path": "plugins\\cloud\\gitleaks\\plugin.py"
    },
    {
        "name": "go_2",
        "category": "cloud",
        "path": "plugins\\cloud\\go_2\\plugin.py"
    },
    {
        "name": "graphw00f",
        "category": "cloud",
        "path": "plugins\\cloud\\graphw00f\\plugin.py"
    },
    {
        "name": "hexstrike-logo",
        "category": "cloud",
        "path": "plugins\\cloud\\hexstrike-logo\\plugin.py"
    },
    {
        "name": "home",
        "category": "cloud",
        "path": "plugins\\cloud\\home\\plugin.py"
    },
    {
        "name": "index_5",
        "category": "cloud",
        "path": "plugins\\cloud\\index_5\\plugin.py"
    },
    {
        "name": "javascript",
        "category": "cloud",
        "path": "plugins\\cloud\\javascript\\plugin.py"
    },
    {
        "name": "js-harvester-agent",
        "category": "cloud",
        "path": "plugins\\cloud\\js-harvester-agent\\plugin.py"
    },
    {
        "name": "kube-bench",
        "category": "cloud",
        "path": "plugins\\cloud\\kube-bench\\plugin.py"
    },
    {
        "name": "kube-hunter",
        "category": "cloud",
        "path": "plugins\\cloud\\kube-hunter\\plugin.py"
    },
    {
        "name": "kubernetes",
        "category": "cloud",
        "path": "plugins\\cloud\\kubernetes\\plugin.py"
    },
    {
        "name": "launch-config",
        "category": "cloud",
        "path": "plugins\\cloud\\launch-config\\plugin.py"
    },
    {
        "name": "leaksapi-banner",
        "category": "cloud",
        "path": "plugins\\cloud\\leaksapi-banner\\plugin.py"
    },
    {
        "name": "leaksapi-logo",
        "category": "cloud",
        "path": "plugins\\cloud\\leaksapi-logo\\plugin.py"
    },
    {
        "name": "LICENSE_5",
        "category": "cloud",
        "path": "plugins\\cloud\\LICENSE_5\\plugin.py"
    },
    {
        "name": "litellm_provider",
        "category": "cloud",
        "path": "plugins\\cloud\\litellm_provider\\plugin.py"
    },
    {
        "name": "logo_3",
        "category": "cloud",
        "path": "plugins\\cloud\\logo_3\\plugin.py"
    },
    {
        "name": "main_13",
        "category": "cloud",
        "path": "plugins\\cloud\\main_13\\plugin.py"
    },
    {
        "name": "main_menu",
        "category": "cloud",
        "path": "plugins\\cloud\\main_menu\\plugin.py"
    },
    {
        "name": "Makefile",
        "category": "cloud",
        "path": "plugins\\cloud\\Makefile\\plugin.py"
    },
    {
        "name": "mindmap_obsidian",
        "category": "cloud",
        "path": "plugins\\cloud\\mindmap_obsidian\\plugin.py"
    },
    {
        "name": "misconfig-detector",
        "category": "cloud",
        "path": "plugins\\cloud\\misconfig-detector\\plugin.py"
    },
    {
        "name": "misconfigtest",
        "category": "cloud",
        "path": "plugins\\cloud\\misconfigtest\\plugin.py"
    },
    {
        "name": "mobile-pentester",
        "category": "cloud",
        "path": "plugins\\cloud\\mobile-pentester\\plugin.py"
    },
    {
        "name": "mode",
        "category": "cloud",
        "path": "plugins\\cloud\\mode\\plugin.py"
    },
    {
        "name": "orchestrator",
        "category": "cloud",
        "path": "plugins\\cloud\\orchestrator\\plugin.py"
    },
    {
        "name": "osint",
        "category": "osint",
        "path": "plugins\\osint\\osint\\plugin.py"
    },
    {
        "name": "outputs",
        "category": "cloud",
        "path": "plugins\\cloud\\outputs\\plugin.py"
    },
    {
        "name": "package_3",
        "category": "cloud",
        "path": "plugins\\cloud\\package_3\\plugin.py"
    },
    {
        "name": "pacu",
        "category": "cloud",
        "path": "plugins\\cloud\\pacu\\plugin.py"
    },
    {
        "name": "pentestgpt_executor",
        "category": "cloud",
        "path": "plugins\\cloud\\pentestgpt_executor\\plugin.py"
    },
    {
        "name": "PentestGPT_Hackable2",
        "category": "cloud",
        "path": "plugins\\cloud\\PentestGPT_Hackable2\\plugin.py"
    },
    {
        "name": "plugins",
        "category": "cloud",
        "path": "plugins\\cloud\\plugins\\plugin.py"
    },
    {
        "name": "pnpm-lock",
        "category": "cloud",
        "path": "plugins\\cloud\\pnpm-lock\\plugin.py"
    },
    {
        "name": "poc-validator",
        "category": "cloud",
        "path": "plugins\\cloud\\poc-validator\\plugin.py"
    },
    {
        "name": "pre-recon-code",
        "category": "cloud",
        "path": "plugins\\cloud\\pre-recon-code\\plugin.py"
    },
    {
        "name": "privesc-advisor",
        "category": "cloud",
        "path": "plugins\\cloud\\privesc-advisor\\plugin.py"
    },
    {
        "name": "privesc_agent",
        "category": "cloud",
        "path": "plugins\\cloud\\privesc_agent\\plugin.py"
    },
    {
        "name": "prowler",
        "category": "cloud",
        "path": "plugins\\cloud\\prowler\\plugin.py"
    },
    {
        "name": "pyproject_3",
        "category": "cloud",
        "path": "plugins\\cloud\\pyproject_3\\plugin.py"
    },
    {
        "name": "quick-start",
        "category": "cloud",
        "path": "plugins\\cloud\\quick-start\\plugin.py"
    },
    {
        "name": "README_21",
        "category": "cloud",
        "path": "plugins\\cloud\\README_21\\plugin.py"
    },
    {
        "name": "README_22",
        "category": "cloud",
        "path": "plugins\\cloud\\README_22\\plugin.py"
    },
    {
        "name": "README_28",
        "category": "cloud",
        "path": "plugins\\cloud\\README_28\\plugin.py"
    },
    {
        "name": "README_29",
        "category": "cloud",
        "path": "plugins\\cloud\\README_29\\plugin.py"
    },
    {
        "name": "README_30",
        "category": "cloud",
        "path": "plugins\\cloud\\README_30\\plugin.py"
    },
    {
        "name": "reconx",
        "category": "cloud",
        "path": "plugins\\cloud\\reconx\\plugin.py"
    },
    {
        "name": "release-beta",
        "category": "cloud",
        "path": "plugins\\cloud\\release-beta\\plugin.py"
    },
    {
        "name": "release_1",
        "category": "cloud",
        "path": "plugins\\cloud\\release_1\\plugin.py"
    },
    {
        "name": "requirements_7",
        "category": "cloud",
        "path": "plugins\\cloud\\requirements_7\\plugin.py"
    },
    {
        "name": "resolver",
        "category": "cloud",
        "path": "plugins\\cloud\\resolver\\plugin.py"
    },
    {
        "name": "results",
        "category": "cloud",
        "path": "plugins\\cloud\\results\\plugin.py"
    },
    {
        "name": "role-management",
        "category": "cloud",
        "path": "plugins\\cloud\\role-management\\plugin.py"
    },
    {
        "name": "rollback",
        "category": "cloud",
        "path": "plugins\\cloud\\rollback\\plugin.py"
    },
    {
        "name": "sarif",
        "category": "cloud",
        "path": "plugins\\cloud\\sarif\\plugin.py"
    },
    {
        "name": "scan_pipeline",
        "category": "cloud",
        "path": "plugins\\cloud\\scan_pipeline\\plugin.py"
    },
    {
        "name": "scan_running",
        "category": "cloud",
        "path": "plugins\\cloud\\scan_running\\plugin.py"
    },
    {
        "name": "scout-suite",
        "category": "cloud",
        "path": "plugins\\cloud\\scout-suite\\plugin.py"
    },
    {
        "name": "Screenshot2",
        "category": "cloud",
        "path": "plugins\\cloud\\Screenshot2\\plugin.py"
    },
    {
        "name": "Screenshot3",
        "category": "cloud",
        "path": "plugins\\cloud\\Screenshot3\\plugin.py"
    },
    {
        "name": "Screenshot4",
        "category": "cloud",
        "path": "plugins\\cloud\\Screenshot4\\plugin.py"
    },
    {
        "name": "secret-scanner-agent",
        "category": "cloud",
        "path": "plugins\\cloud\\secret-scanner-agent\\plugin.py"
    },
    {
        "name": "secure_credential",
        "category": "cloud",
        "path": "plugins\\cloud\\secure_credential\\plugin.py"
    },
    {
        "name": "security",
        "category": "cloud",
        "path": "plugins\\cloud\\security\\plugin.py"
    },
    {
        "name": "SECURITY_3",
        "category": "cloud",
        "path": "plugins\\cloud\\SECURITY_3\\plugin.py"
    },
    {
        "name": "selection_agent",
        "category": "cloud",
        "path": "plugins\\cloud\\selection_agent\\plugin.py"
    },
    {
        "name": "server_mcp_pentest_18",
        "category": "cloud",
        "path": "plugins\\cloud\\server_mcp_pentest_18\\plugin.py"
    },
    {
        "name": "service_analyzer",
        "category": "cloud",
        "path": "plugins\\cloud\\service_analyzer\\plugin.py"
    },
    {
        "name": "service_correlator_1",
        "category": "cloud",
        "path": "plugins\\cloud\\service_correlator_1\\plugin.py"
    },
    {
        "name": "settings_2",
        "category": "cloud",
        "path": "plugins\\cloud\\settings_2\\plugin.py"
    },
    {
        "name": "setup",
        "category": "cloud",
        "path": "plugins\\cloud\\setup\\plugin.py"
    },
    {
        "name": "setup_1",
        "category": "cloud",
        "path": "plugins\\cloud\\setup_1\\plugin.py"
    },
    {
        "name": "shannon-banner",
        "category": "cloud",
        "path": "plugins\\cloud\\shannon-banner\\plugin.py"
    },
    {
        "name": "SHANNON-PRO_1",
        "category": "cloud",
        "path": "plugins\\cloud\\SHANNON-PRO_1\\plugin.py"
    },
    {
        "name": "shannon-report-capital-api",
        "category": "cloud",
        "path": "plugins\\cloud\\shannon-report-capital-api\\plugin.py"
    },
    {
        "name": "shannon-screen",
        "category": "cloud",
        "path": "plugins\\cloud\\shannon-screen\\plugin.py"
    },
    {
        "name": "shodan",
        "category": "cloud",
        "path": "plugins\\cloud\\shodan\\plugin.py"
    },
    {
        "name": "six2dez_reconftw-stars-history",
        "category": "cloud",
        "path": "plugins\\cloud\\six2dez_reconftw-stars-history\\plugin.py"
    },
    {
        "name": "SKILL_1",
        "category": "cloud",
        "path": "plugins\\cloud\\SKILL_1\\plugin.py"
    },
    {
        "name": "SKILL_14",
        "category": "cloud",
        "path": "plugins\\cloud\\SKILL_14\\plugin.py"
    },
    {
        "name": "SKILL_16",
        "category": "cloud",
        "path": "plugins\\cloud\\SKILL_16\\plugin.py"
    },
    {
        "name": "SKILL_17",
        "category": "cloud",
        "path": "plugins\\cloud\\SKILL_17\\plugin.py"
    },
    {
        "name": "SKILL_4",
        "category": "cloud",
        "path": "plugins\\cloud\\SKILL_4\\plugin.py"
    },
    {
        "name": "social-engineer",
        "category": "cloud",
        "path": "plugins\\cloud\\social-engineer\\plugin.py"
    },
    {
        "name": "sponsor-wechat-alipay-qr",
        "category": "cloud",
        "path": "plugins\\cloud\\sponsor-wechat-alipay-qr\\plugin.py"
    },
    {
        "name": "ssrf_payloads",
        "category": "cloud",
        "path": "plugins\\cloud\\ssrf_payloads\\plugin.py"
    },
    {
        "name": "stop",
        "category": "cloud",
        "path": "plugins\\cloud\\stop\\plugin.py"
    },
    {
        "name": "tch",
        "category": "cloud",
        "path": "plugins\\cloud\\tch\\plugin.py"
    },
    {
        "name": "tcp_beacon_server",
        "category": "cloud",
        "path": "plugins\\cloud\\tcp_beacon_server\\plugin.py"
    },
    {
        "name": "teardown",
        "category": "cloud",
        "path": "plugins\\cloud\\teardown\\plugin.py"
    },
    {
        "name": "techdetect",
        "category": "cloud",
        "path": "plugins\\cloud\\techdetect\\plugin.py"
    },
    {
        "name": "terraform-reconFTW",
        "category": "cloud",
        "path": "plugins\\cloud\\terraform-reconFTW\\plugin.py"
    },
    {
        "name": "test_ad_agent_e2e_smoke",
        "category": "cloud",
        "path": "plugins\\cloud\\test_ad_agent_e2e_smoke\\plugin.py"
    },
    {
        "name": "test_agents",
        "category": "cloud",
        "path": "plugins\\cloud\\test_agents\\plugin.py"
    },
    {
        "name": "test_benchmark_cli",
        "category": "cloud",
        "path": "plugins\\cloud\\test_benchmark_cli\\plugin.py"
    },
    {
        "name": "test_chain_context_discriminator",
        "category": "cloud",
        "path": "plugins\\cloud\\test_chain_context_discriminator\\plugin.py"
    },
    {
        "name": "test_cli_menu",
        "category": "cloud",
        "path": "plugins\\cloud\\test_cli_menu\\plugin.py"
    },
    {
        "name": "test_cloud_agent_e2e_smoke",
        "category": "cloud",
        "path": "plugins\\cloud\\test_cloud_agent_e2e_smoke\\plugin.py"
    },
    {
        "name": "test_container_health",
        "category": "cloud",
        "path": "plugins\\cloud\\test_container_health\\plugin.py"
    },
    {
        "name": "test_docker_build",
        "category": "cloud",
        "path": "plugins\\cloud\\test_docker_build\\plugin.py"
    },
    {
        "name": "test_flag_detection",
        "category": "cloud",
        "path": "plugins\\cloud\\test_flag_detection\\plugin.py"
    },
    {
        "name": "test_litellm_provider",
        "category": "cloud",
        "path": "plugins\\cloud\\test_litellm_provider\\plugin.py"
    },
    {
        "name": "test_misc_coverage_2",
        "category": "cloud",
        "path": "plugins\\cloud\\test_misc_coverage_2\\plugin.py"
    },
    {
        "name": "test_osint_domain_info_msftrecon",
        "category": "osint",
        "path": "plugins\\osint\\test_osint_domain_info_msftrecon\\plugin.py"
    },
    {
        "name": "test_providers_and_small_agents",
        "category": "cloud",
        "path": "plugins\\cloud\\test_providers_and_small_agents\\plugin.py"
    },
    {
        "name": "test_selection_agent",
        "category": "cloud",
        "path": "plugins\\cloud\\test_selection_agent\\plugin.py"
    },
    {
        "name": "trufflehog",
        "category": "cloud",
        "path": "plugins\\cloud\\trufflehog\\plugin.py"
    },
    {
        "name": "type_confusion",
        "category": "cloud",
        "path": "plugins\\cloud\\type_confusion\\plugin.py"
    },
    {
        "name": "uninstall",
        "category": "cloud",
        "path": "plugins\\cloud\\uninstall\\plugin.py"
    },
    {
        "name": "USAGE",
        "category": "cloud",
        "path": "plugins\\cloud\\USAGE\\plugin.py"
    },
    {
        "name": "usage_input",
        "category": "cloud",
        "path": "plugins\\cloud\\usage_input\\plugin.py"
    },
    {
        "name": "usage_output",
        "category": "cloud",
        "path": "plugins\\cloud\\usage_output\\plugin.py"
    },
    {
        "name": "usage_server1",
        "category": "cloud",
        "path": "plugins\\cloud\\usage_server1\\plugin.py"
    },
    {
        "name": "usage_server2",
        "category": "cloud",
        "path": "plugins\\cloud\\usage_server2\\plugin.py"
    },
    {
        "name": "variables",
        "category": "cloud",
        "path": "plugins\\cloud\\variables\\plugin.py"
    },
    {
        "name": "vectorDB",
        "category": "cloud",
        "path": "plugins\\cloud\\vectorDB\\plugin.py"
    },
    {
        "name": "vuln-auth",
        "category": "cloud",
        "path": "plugins\\cloud\\vuln-auth\\plugin.py"
    },
    {
        "name": "vuln-authz",
        "category": "cloud",
        "path": "plugins\\cloud\\vuln-authz\\plugin.py"
    },
    {
        "name": "vuln-authz_2",
        "category": "cloud",
        "path": "plugins\\cloud\\vuln-authz_2\\plugin.py"
    },
    {
        "name": "vuln-auth_2",
        "category": "cloud",
        "path": "plugins\\cloud\\vuln-auth_2\\plugin.py"
    },
    {
        "name": "vuln-injection",
        "category": "cloud",
        "path": "plugins\\cloud\\vuln-injection\\plugin.py"
    },
    {
        "name": "vuln-injection_2",
        "category": "cloud",
        "path": "plugins\\cloud\\vuln-injection_2\\plugin.py"
    },
    {
        "name": "vuln-xss",
        "category": "cloud",
        "path": "plugins\\cloud\\vuln-xss\\plugin.py"
    },
    {
        "name": "vuln-xss_2",
        "category": "cloud",
        "path": "plugins\\cloud\\vuln-xss_2\\plugin.py"
    },
    {
        "name": "vulnerability-management",
        "category": "cloud",
        "path": "plugins\\cloud\\vulnerability-management\\plugin.py"
    },
    {
        "name": "waf-detector-agent",
        "category": "cloud",
        "path": "plugins\\cloud\\waf-detector-agent\\plugin.py"
    },
    {
        "name": "wafw00f",
        "category": "cloud",
        "path": "plugins\\cloud\\wafw00f\\plugin.py"
    },
    {
        "name": "web-console",
        "category": "cloud",
        "path": "plugins\\cloud\\web-console\\plugin.py"
    },
    {
        "name": "wechat-group-cyberstrikeai-qr",
        "category": "cloud",
        "path": "plugins\\cloud\\wechat-group-cyberstrikeai-qr\\plugin.py"
    },
    {
        "name": "whois",
        "category": "recon",
        "path": "plugins\\recon\\whois\\plugin.py"
    },
    {
        "name": "workflow_center",
        "category": "cloud",
        "path": "plugins\\cloud\\workflow_center\\plugin.py"
    },
    {
        "name": "workspaces",
        "category": "cloud",
        "path": "plugins\\cloud\\workspaces\\plugin.py"
    },
    {
        "name": "zh-CN",
        "category": "cloud",
        "path": "plugins\\cloud\\zh-CN\\plugin.py"
    },
    {
        "name": "_10",
        "category": "cloud",
        "path": "plugins\\cloud\\_10\\plugin.py"
    },
    {
        "name": "__init___119",
        "category": "cloud",
        "path": "plugins\\cloud\\__init___119\\plugin.py"
    },
    {
        "name": "__init___26",
        "category": "cloud",
        "path": "plugins\\cloud\\__init___26\\plugin.py"
    },
    {
        "name": "__init___78",
        "category": "cloud",
        "path": "plugins\\cloud\\__init___78\\plugin.py"
    },
    {
        "name": "common",
        "category": "recon",
        "path": "plugins\\recon\\common\\plugin.py"
    },
    {
        "name": "hashpump",
        "category": "recon",
        "path": "plugins\\recon\\hashpump\\plugin.py"
    },
    {
        "name": "libc-database",
        "category": "recon",
        "path": "plugins\\recon\\libc-database\\plugin.py"
    },
    {
        "name": "linpeas",
        "category": "recon",
        "path": "plugins\\recon\\linpeas\\plugin.py"
    },
    {
        "name": "one-gadget",
        "category": "recon",
        "path": "plugins\\recon\\one-gadget\\plugin.py"
    },
    {
        "name": "output_parser",
        "category": "recon",
        "path": "plugins\\recon\\output_parser\\plugin.py"
    },
    {
        "name": "pwninit",
        "category": "recon",
        "path": "plugins\\recon\\pwninit\\plugin.py"
    },
    {
        "name": "README_31",
        "category": "recon",
        "path": "plugins\\recon\\README_31\\plugin.py"
    },
    {
        "name": "score_juiceshop",
        "category": "recon",
        "path": "plugins\\recon\\score_juiceshop\\plugin.py"
    },
    {
        "name": "steghide",
        "category": "recon",
        "path": "plugins\\recon\\steghide\\plugin.py"
    },
    {
        "name": "test_session",
        "category": "recon",
        "path": "plugins\\recon\\test_session\\plugin.py"
    },
    {
        "name": "zsteg",
        "category": "recon",
        "path": "plugins\\recon\\zsteg\\plugin.py"
    },
    {
        "name": "__init___219",
        "category": "recon",
        "path": "plugins\\recon\\__init___219\\plugin.py"
    },
    {
        "name": "active_recon",
        "category": "recon",
        "path": "plugins\\recon\\active_recon\\plugin.py"
    },
    {
        "name": "asn_intel",
        "category": "recon",
        "path": "plugins\\recon\\asn_intel\\plugin.py"
    },
    {
        "name": "bigbountyrecon",
        "category": "recon",
        "path": "plugins\\recon\\bigbountyrecon\\plugin.py"
    },
    {
        "name": "content_discovery",
        "category": "recon",
        "path": "plugins\\recon\\content_discovery\\plugin.py"
    },
    {
        "name": "csp_extractor",
        "category": "recon",
        "path": "plugins\\recon\\csp_extractor\\plugin.py"
    },
    {
        "name": "graphql_scan",
        "category": "recon",
        "path": "plugins\\recon\\graphql_scan\\plugin.py"
    },
    {
        "name": "httpx",
        "category": "recon",
        "path": "plugins\\recon\\httpx\\plugin.py"
    },
    {
        "name": "naabu",
        "category": "recon",
        "path": "plugins\\recon\\naabu\\plugin.py"
    },
    {
        "name": "nuclei",
        "category": "recon",
        "path": "plugins\\recon\\nuclei\\plugin.py"
    },
    {
        "name": "passive_recon",
        "category": "recon",
        "path": "plugins\\recon\\passive_recon\\plugin.py"
    },
    {
        "name": "scan4all",
        "category": "recon",
        "path": "plugins\\recon\\scan4all\\plugin.py"
    },
    {
        "name": "subfinder",
        "category": "recon",
        "path": "plugins\\recon\\subfinder\\plugin.py"
    },
    {
        "name": "xss_scan",
        "category": "recon",
        "path": "plugins\\recon\\xss_scan\\plugin.py"
    },
    {
        "name": "cloud_enum",
        "category": "cloud",
        "path": "plugins\\cloud\\cloud_enum\\plugin.py"
    },
    {
        "name": "subdomains",
        "category": "recon",
        "path": "plugins\\recon\\subdomains\\plugin.py"
    },
    {
        "name": "surface_mapping",
        "category": "recon",
        "path": "plugins\\recon\\surface_mapping\\plugin.py"
    },
    {
        "name": "web_assets",
        "category": "recon",
        "path": "plugins\\recon\\web_assets\\plugin.py"
    },
    {
        "name": "asn",
        "category": "recon",
        "path": "plugins\\recon\\asn\\plugin.py"
    },
    {
        "name": "AGENT-GUIDE",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\AGENT-GUIDE\\plugin.py"
    },
    {
        "name": "agent_mode_controller",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\agent_mode_controller\\plugin.py"
    },
    {
        "name": "attackchain_1",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\attackchain_1\\plugin.py"
    },
    {
        "name": "balanced-active-scan",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\balanced-active-scan\\plugin.py"
    },
    {
        "name": "BigQueryInjection",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\BigQueryInjection\\plugin.py"
    },
    {
        "name": "cache",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\cache\\plugin.py"
    },
    {
        "name": "CassandraInjection",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\CassandraInjection\\plugin.py"
    },
    {
        "name": "checkpoint-provider",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\checkpoint-provider\\plugin.py"
    },
    {
        "name": "concurrency",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\concurrency\\plugin.py"
    },
    {
        "name": "container",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\container\\plugin.py"
    },
    {
        "name": "context",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\context\\plugin.py"
    },
    {
        "name": "conversation_1",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\conversation_1\\plugin.py"
    },
    {
        "name": "cve_mapper",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\cve_mapper\\plugin.py"
    },
    {
        "name": "cvss",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\cvss\\plugin.py"
    },
    {
        "name": "database",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\database\\plugin.py"
    },
    {
        "name": "DB2Injection",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\DB2Injection\\plugin.py"
    },
    {
        "name": "db_1",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\db_1\\plugin.py"
    },
    {
        "name": "db_test",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\db_test\\plugin.py"
    },
    {
        "name": "deliverables",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\deliverables\\plugin.py"
    },
    {
        "name": "detection_agent",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\detection_agent\\plugin.py"
    },
    {
        "name": "eino_adk_run_loop",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\eino_adk_run_loop\\plugin.py"
    },
    {
        "name": "eino_meta_test",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\eino_meta_test\\plugin.py"
    },
    {
        "name": "eino_retriever_adapter",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\eino_retriever_adapter\\plugin.py"
    },
    {
        "name": "eino_retrieve_chain",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\eino_retrieve_chain\\plugin.py"
    },
    {
        "name": "eino_sqlite_indexer",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\eino_sqlite_indexer\\plugin.py"
    },
    {
        "name": "endpoint-prober",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\endpoint-prober\\plugin.py"
    },
    {
        "name": "ErrorPatternAnalyzer",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\ErrorPatternAnalyzer\\plugin.py"
    },
    {
        "name": "exploit-auth_1",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\exploit-auth_1\\plugin.py"
    },
    {
        "name": "exploit-auth_3",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\exploit-auth_3\\plugin.py"
    },
    {
        "name": "exploit-injection_1",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\exploit-injection_1\\plugin.py"
    },
    {
        "name": "exploit-injection_3",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\exploit-injection_3\\plugin.py"
    },
    {
        "name": "exploit-ssrf_1",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\exploit-ssrf_1\\plugin.py"
    },
    {
        "name": "exploit-ssrf_3",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\exploit-ssrf_3\\plugin.py"
    },
    {
        "name": "exploit-xss_1",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\exploit-xss_1\\plugin.py"
    },
    {
        "name": "exploit-xss_3",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\exploit-xss_3\\plugin.py"
    },
    {
        "name": "exploitation-checker",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\exploitation-checker\\plugin.py"
    },
    {
        "name": "export",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\export\\plugin.py"
    },
    {
        "name": "export-metrics",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\export-metrics\\plugin.py"
    },
    {
        "name": "finalizers",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\finalizers\\plugin.py"
    },
    {
        "name": "findings",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\findings\\plugin.py"
    },
    {
        "name": "FINDINGS-DB",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\FINDINGS-DB\\plugin.py"
    },
    {
        "name": "findings-provider",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\findings-provider\\plugin.py"
    },
    {
        "name": "findings-renderer",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\findings-renderer\\plugin.py"
    },
    {
        "name": "generators",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\generators\\plugin.py"
    },
    {
        "name": "gowitness",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\gowitness\\plugin.py"
    },
    {
        "name": "Hackable2_3",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\Hackable2_3\\plugin.py"
    },
    {
        "name": "handoff",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\handoff\\plugin.py"
    },
    {
        "name": "index_pipeline",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\index_pipeline\\plugin.py"
    },
    {
        "name": "Kioptrix_level_1",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\Kioptrix_level_1\\plugin.py"
    },
    {
        "name": "listener_http_test",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\listener_http_test\\plugin.py"
    },
    {
        "name": "manager",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\manager\\plugin.py"
    },
    {
        "name": "manager_start_test",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\manager_start_test\\plugin.py"
    },
    {
        "name": "menu_system",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\menu_system\\plugin.py"
    },
    {
        "name": "metasploit",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\metasploit\\plugin.py"
    },
    {
        "name": "metasploit_aux",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\metasploit_aux\\plugin.py"
    },
    {
        "name": "metatron",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\metatron\\plugin.py"
    },
    {
        "name": "migrate",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\migrate\\plugin.py"
    },
    {
        "name": "net-recon-agent",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\net-recon-agent\\plugin.py"
    },
    {
        "name": "nikto",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\nikto\\plugin.py"
    },
    {
        "name": "nmap-distccd",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\nmap-distccd\\plugin.py"
    },
    {
        "name": "nmap_2",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\nmap_2\\plugin.py"
    },
    {
        "name": "notification",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\notification\\plugin.py"
    },
    {
        "name": "output-formatter",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\output-formatter\\plugin.py"
    },
    {
        "name": "output-formatters",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\output-formatters\\plugin.py"
    },
    {
        "name": "payloads",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\payloads\\plugin.py"
    },
    {
        "name": "pentestTarget",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\pentestTarget\\plugin.py"
    },
    {
        "name": "pipeline",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\pipeline\\plugin.py"
    },
    {
        "name": "primitives",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\primitives\\plugin.py"
    },
    {
        "name": "prompt_class",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\prompt_class\\plugin.py"
    },
    {
        "name": "pwntools",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\pwntools\\plugin.py"
    },
    {
        "name": "query-execution-result",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\query-execution-result\\plugin.py"
    },
    {
        "name": "queue-schemas",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\queue-schemas\\plugin.py"
    },
    {
        "name": "queue-validation",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\queue-validation\\plugin.py"
    },
    {
        "name": "report-executive",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\report-executive\\plugin.py"
    },
    {
        "name": "report-executive_3",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\report-executive_3\\plugin.py"
    },
    {
        "name": "report-generator",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\report-generator\\plugin.py"
    },
    {
        "name": "reporting",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\reporting\\plugin.py"
    },
    {
        "name": "requester",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\requester\\plugin.py"
    },
    {
        "name": "requestercpython-313",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\requestercpython-313\\plugin.py"
    },
    {
        "name": "retriever",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\retriever\\plugin.py"
    },
    {
        "name": "schema",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\schema\\plugin.py"
    },
    {
        "name": "schema_migrate",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\schema_migrate\\plugin.py"
    },
    {
        "name": "session-manager",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\session-manager\\plugin.py"
    },
    {
        "name": "settings-writer",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\settings-writer\\plugin.py"
    },
    {
        "name": "SKILL_10",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\SKILL_10\\plugin.py"
    },
    {
        "name": "SKILL_15",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\SKILL_15\\plugin.py"
    },
    {
        "name": "SKILL_21",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\SKILL_21\\plugin.py"
    },
    {
        "name": "target",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\target\\plugin.py"
    },
    {
        "name": "task",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\task\\plugin.py"
    },
    {
        "name": "test_aup_consent",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\test_aup_consent\\plugin.py"
    },
    {
        "name": "test_benchmark_registry",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\test_benchmark_registry\\plugin.py"
    },
    {
        "name": "test_chain_dedup",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\test_chain_dedup\\plugin.py"
    },
    {
        "name": "test_chain_validation",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\test_chain_validation\\plugin.py"
    },
    {
        "name": "test_cve_db",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\test_cve_db\\plugin.py"
    },
    {
        "name": "test_cvss",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\test_cvss\\plugin.py"
    },
    {
        "name": "test_diff",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\test_diff\\plugin.py"
    },
    {
        "name": "test_findings",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\test_findings\\plugin.py"
    },
    {
        "name": "test_findings_db_reaper",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\test_findings_db_reaper\\plugin.py"
    },
    {
        "name": "test_findings_db_reconciler",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\test_findings_db_reconciler\\plugin.py"
    },
    {
        "name": "test_handler_finalizers",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\test_handler_finalizers\\plugin.py"
    },
    {
        "name": "test_intensity_safe",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\test_intensity_safe\\plugin.py"
    },
    {
        "name": "test_orchestrator",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\test_orchestrator\\plugin.py"
    },
    {
        "name": "test_probe_cookie_prefix_bypass",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\test_probe_cookie_prefix_bypass\\plugin.py"
    },
    {
        "name": "test_probe_jwt_jku_x5u_ssrf",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\test_probe_jwt_jku_x5u_ssrf\\plugin.py"
    },
    {
        "name": "test_probe_nextjs_rsc_rce",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\test_probe_nextjs_rsc_rce\\plugin.py"
    },
    {
        "name": "test_probe_saml_xsw",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\test_probe_saml_xsw\\plugin.py"
    },
    {
        "name": "test_probe_sqli_login_bypass",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\test_probe_sqli_login_bypass\\plugin.py"
    },
    {
        "name": "test_sarif",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\test_sarif\\plugin.py"
    },
    {
        "name": "test_webhooks",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\test_webhooks\\plugin.py"
    },
    {
        "name": "tls-analyzer",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\tls-analyzer\\plugin.py"
    },
    {
        "name": "TOKEN-OPTIMIZATION",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\TOKEN-OPTIMIZATION\\plugin.py"
    },
    {
        "name": "tool",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\tool\\plugin.py"
    },
    {
        "name": "types_5",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\types_5\\plugin.py"
    },
    {
        "name": "vuln-authz_3",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\vuln-authz_3\\plugin.py"
    },
    {
        "name": "vuln-injection_3",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\vuln-injection_3\\plugin.py"
    },
    {
        "name": "vuln-mapper",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\vuln-mapper\\plugin.py"
    },
    {
        "name": "vuln-mappertest",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\vuln-mappertest\\plugin.py"
    },
    {
        "name": "vuln-ssrf_1",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\vuln-ssrf_1\\plugin.py"
    },
    {
        "name": "vuln-xss_1",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\vuln-xss_1\\plugin.py"
    },
    {
        "name": "vuln-xss_3",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\vuln-xss_3\\plugin.py"
    },
    {
        "name": "worker",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\worker\\plugin.py"
    },
    {
        "name": "working_memory",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\working_memory\\plugin.py"
    },
    {
        "name": "xsser",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\xsser\\plugin.py"
    },
    {
        "name": "_exploit-scope",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\_exploit-scope\\plugin.py"
    },
    {
        "name": "_exploit-scope_1",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\_exploit-scope_1\\plugin.py"
    },
    {
        "name": "_vuln-scope",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\_vuln-scope\\plugin.py"
    },
    {
        "name": "_vuln-scope_1",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\_vuln-scope_1\\plugin.py"
    },
    {
        "name": "dns_intelligence",
        "category": "recon",
        "path": "plugins\\recon\\dns_intelligence\\plugin.py"
    },
    {
        "name": "llm_analysis",
        "category": "recon",
        "path": "plugins\\recon\\llm_analysis\\plugin.py"
    },
    {
        "name": "malicious",
        "category": "recon",
        "path": "plugins\\recon\\malicious\\plugin.py"
    },
    {
        "name": "network_discovery",
        "category": "recon",
        "path": "plugins\\recon\\network_discovery\\plugin.py"
    },
    {
        "name": "viewport",
        "category": "recon",
        "path": "plugins\\recon\\viewport\\plugin.py"
    },
    {
        "name": "web_recon",
        "category": "recon",
        "path": "plugins\\recon\\web_recon\\plugin.py"
    },
    {
        "name": "active",
        "category": "recon",
        "path": "plugins\\recon\\active\\plugin.py"
    },
    {
        "name": "active_test",
        "category": "recon",
        "path": "plugins\\recon\\active_test\\plugin.py"
    },
    {
        "name": "auth_manager",
        "category": "recon",
        "path": "plugins\\recon\\auth_manager\\plugin.py"
    },
    {
        "name": "basic_scan",
        "category": "recon",
        "path": "plugins\\recon\\basic_scan\\plugin.py"
    },
    {
        "name": "beacon_host",
        "category": "recon",
        "path": "plugins\\recon\\beacon_host\\plugin.py"
    },
    {
        "name": "brute",
        "category": "recon",
        "path": "plugins\\recon\\brute\\plugin.py"
    },
    {
        "name": "bruteforce-ftp",
        "category": "recon",
        "path": "plugins\\recon\\bruteforce-ftp\\plugin.py"
    },
    {
        "name": "bruteforce-http",
        "category": "recon",
        "path": "plugins\\recon\\bruteforce-http\\plugin.py"
    },
    {
        "name": "bruteforce-rdp",
        "category": "recon",
        "path": "plugins\\recon\\bruteforce-rdp\\plugin.py"
    },
    {
        "name": "bruteforce-smb",
        "category": "recon",
        "path": "plugins\\recon\\bruteforce-smb\\plugin.py"
    },
    {
        "name": "bruteforce-ssh",
        "category": "recon",
        "path": "plugins\\recon\\bruteforce-ssh\\plugin.py"
    },
    {
        "name": "brute_test",
        "category": "recon",
        "path": "plugins\\recon\\brute_test\\plugin.py"
    },
    {
        "name": "cgo_specific",
        "category": "recon",
        "path": "plugins\\recon\\cgo_specific\\plugin.py"
    },
    {
        "name": "check-env",
        "category": "recon",
        "path": "plugins\\recon\\check-env\\plugin.py"
    },
    {
        "name": "client_2",
        "category": "recon",
        "path": "plugins\\recon\\client_2\\plugin.py"
    },
    {
        "name": "client_sdk",
        "category": "recon",
        "path": "plugins\\recon\\client_sdk\\plugin.py"
    },
    {
        "name": "codeclimate",
        "category": "recon",
        "path": "plugins\\recon\\codeclimate\\plugin.py"
    },
    {
        "name": "config_4",
        "category": "recon",
        "path": "plugins\\recon\\config_4\\plugin.py"
    },
    {
        "name": "curl-known-security",
        "category": "recon",
        "path": "plugins\\recon\\curl-known-security\\plugin.py"
    },
    {
        "name": "curl-robots",
        "category": "recon",
        "path": "plugins\\recon\\curl-robots\\plugin.py"
    },
    {
        "name": "CyberStrikeAIClient1",
        "category": "recon",
        "path": "plugins\\recon\\CyberStrikeAIClient1\\plugin.py"
    },
    {
        "name": "datasrcs_test",
        "category": "recon",
        "path": "plugins\\recon\\datasrcs_test\\plugin.py"
    },
    {
        "name": "deepsource",
        "category": "recon",
        "path": "plugins\\recon\\deepsource\\plugin.py"
    },
    {
        "name": "dependabot_2",
        "category": "recon",
        "path": "plugins\\recon\\dependabot_2\\plugin.py"
    },
    {
        "name": "eino_retrieve_chain_test",
        "category": "recon",
        "path": "plugins\\recon\\eino_retrieve_chain_test\\plugin.py"
    },
    {
        "name": "entrypoint_1",
        "category": "recon",
        "path": "plugins\\recon\\entrypoint_1\\plugin.py"
    },
    {
        "name": "enum4linux",
        "category": "recon",
        "path": "plugins\\recon\\enum4linux\\plugin.py"
    },
    {
        "name": "envexpand",
        "category": "recon",
        "path": "plugins\\recon\\envexpand\\plugin.py"
    },
    {
        "name": "env_1",
        "category": "recon",
        "path": "plugins\\recon\\env_1\\plugin.py"
    },
    {
        "name": "error",
        "category": "recon",
        "path": "plugins\\recon\\error\\plugin.py"
    },
    {
        "name": "eslintconfig",
        "category": "recon",
        "path": "plugins\\recon\\eslintconfig\\plugin.py"
    },
    {
        "name": "execute-python-script",
        "category": "recon",
        "path": "plugins\\recon\\execute-python-script\\plugin.py"
    },
    {
        "name": "external_manager",
        "category": "recon",
        "path": "plugins\\recon\\external_manager\\plugin.py"
    },
    {
        "name": "external_manager_test",
        "category": "recon",
        "path": "plugins\\recon\\external_manager_test\\plugin.py"
    },
    {
        "name": "external_mcp",
        "category": "recon",
        "path": "plugins\\recon\\external_mcp\\plugin.py"
    },
    {
        "name": "falco",
        "category": "recon",
        "path": "plugins\\recon\\falco\\plugin.py"
    },
    {
        "name": "get-arch",
        "category": "recon",
        "path": "plugins\\recon\\get-arch\\plugin.py"
    },
    {
        "name": "goreleaser",
        "category": "recon",
        "path": "plugins\\recon\\goreleaser\\plugin.py"
    },
    {
        "name": "index_14",
        "category": "recon",
        "path": "plugins\\recon\\index_14\\plugin.py"
    },
    {
        "name": "index_7",
        "category": "recon",
        "path": "plugins\\recon\\index_7\\plugin.py"
    },
    {
        "name": "install-python-package",
        "category": "recon",
        "path": "plugins\\recon\\install-python-package\\plugin.py"
    },
    {
        "name": "issue_importer",
        "category": "recon",
        "path": "plugins\\recon\\issue_importer\\plugin.py"
    },
    {
        "name": "jaeles",
        "category": "recon",
        "path": "plugins\\recon\\jaeles\\plugin.py"
    },
    {
        "name": "ldap-search",
        "category": "recon",
        "path": "plugins\\recon\\ldap-search\\plugin.py"
    },
    {
        "name": "lint",
        "category": "recon",
        "path": "plugins\\recon\\lint\\plugin.py"
    },
    {
        "name": "loggercpython-313",
        "category": "recon",
        "path": "plugins\\recon\\loggercpython-313\\plugin.py"
    },
    {
        "name": "logger_2",
        "category": "recon",
        "path": "plugins\\recon\\logger_2\\plugin.py"
    },
    {
        "name": "lookup-sid",
        "category": "recon",
        "path": "plugins\\recon\\lookup-sid\\plugin.py"
    },
    {
        "name": "main_14",
        "category": "recon",
        "path": "plugins\\recon\\main_14\\plugin.py"
    },
    {
        "name": "main_15",
        "category": "recon",
        "path": "plugins\\recon\\main_15\\plugin.py"
    },
    {
        "name": "main_server_http_redirect",
        "category": "recon",
        "path": "plugins\\recon\\main_server_http_redirect\\plugin.py"
    },
    {
        "name": "main_server_http_redirect_test",
        "category": "recon",
        "path": "plugins\\recon\\main_server_http_redirect_test\\plugin.py"
    },
    {
        "name": "mcp_reverse_shell",
        "category": "recon",
        "path": "plugins\\recon\\mcp_reverse_shell\\plugin.py"
    },
    {
        "name": "meta",
        "category": "recon",
        "path": "plugins\\recon\\meta\\plugin.py"
    },
    {
        "name": "nbtscan",
        "category": "recon",
        "path": "plugins\\recon\\nbtscan\\plugin.py"
    },
    {
        "name": "nmap-finger",
        "category": "recon",
        "path": "plugins\\recon\\nmap-finger\\plugin.py"
    },
    {
        "name": "nmap-kerberos",
        "category": "recon",
        "path": "plugins\\recon\\nmap-kerberos\\plugin.py"
    },
    {
        "name": "nmap-msrpc",
        "category": "recon",
        "path": "plugins\\recon\\nmap-msrpc\\plugin.py"
    },
    {
        "name": "nmap-nntp",
        "category": "recon",
        "path": "plugins\\recon\\nmap-nntp\\plugin.py"
    },
    {
        "name": "nmap-redis",
        "category": "recon",
        "path": "plugins\\recon\\nmap-redis\\plugin.py"
    },
    {
        "name": "nmap-rmi",
        "category": "recon",
        "path": "plugins\\recon\\nmap-rmi\\plugin.py"
    },
    {
        "name": "nmap-sip",
        "category": "recon",
        "path": "plugins\\recon\\nmap-sip\\plugin.py"
    },
    {
        "name": "nmap-ssh",
        "category": "recon",
        "path": "plugins\\recon\\nmap-ssh\\plugin.py"
    },
    {
        "name": "nmap-telnet",
        "category": "recon",
        "path": "plugins\\recon\\nmap-telnet\\plugin.py"
    },
    {
        "name": "nmap-tftp",
        "category": "recon",
        "path": "plugins\\recon\\nmap-tftp\\plugin.py"
    },
    {
        "name": "nmap_tool_1",
        "category": "recon",
        "path": "plugins\\recon\\nmap_tool_1\\plugin.py"
    },
    {
        "name": "onesixtyone",
        "category": "recon",
        "path": "plugins\\recon\\onesixtyone\\plugin.py"
    },
    {
        "name": "oracle-odat",
        "category": "recon",
        "path": "plugins\\recon\\oracle-odat\\plugin.py"
    },
    {
        "name": "oracle-scanner",
        "category": "recon",
        "path": "plugins\\recon\\oracle-scanner\\plugin.py"
    },
    {
        "name": "oracle-tnscmd",
        "category": "recon",
        "path": "plugins\\recon\\oracle-tnscmd\\plugin.py"
    },
    {
        "name": "parallel_scans",
        "category": "recon",
        "path": "plugins\\recon\\parallel_scans\\plugin.py"
    },
    {
        "name": "paths",
        "category": "recon",
        "path": "plugins\\recon\\paths\\plugin.py"
    },
    {
        "name": "portscan-top-tcp-ports",
        "category": "recon",
        "path": "plugins\\recon\\portscan-top-tcp-ports\\plugin.py"
    },
    {
        "name": "pre-commit-config_1",
        "category": "recon",
        "path": "plugins\\recon\\pre-commit-config_1\\plugin.py"
    },
    {
        "name": "process_registry",
        "category": "recon",
        "path": "plugins\\recon\\process_registry\\plugin.py"
    },
    {
        "name": "pyproject_5",
        "category": "recon",
        "path": "plugins\\recon\\pyproject_5\\plugin.py"
    },
    {
        "name": "README_CN",
        "category": "recon",
        "path": "plugins\\recon\\README_CN\\plugin.py"
    },
    {
        "name": "README_CN_2",
        "category": "recon",
        "path": "plugins\\recon\\README_CN_2\\plugin.py"
    },
    {
        "name": "reconFTW",
        "category": "recon",
        "path": "plugins\\recon\\reconFTW\\plugin.py"
    },
    {
        "name": "redirect-host-discovery",
        "category": "recon",
        "path": "plugins\\recon\\redirect-host-discovery\\plugin.py"
    },
    {
        "name": "redis-cli",
        "category": "recon",
        "path": "plugins\\recon\\redis-cli\\plugin.py"
    },
    {
        "name": "registry_2",
        "category": "recon",
        "path": "plugins\\recon\\registry_2\\plugin.py"
    },
    {
        "name": "release",
        "category": "recon",
        "path": "plugins\\recon\\release\\plugin.py"
    },
    {
        "name": "requirements_14",
        "category": "recon",
        "path": "plugins\\recon\\requirements_14\\plugin.py"
    },
    {
        "name": "requirements_15",
        "category": "recon",
        "path": "plugins\\recon\\requirements_15\\plugin.py"
    },
    {
        "name": "requirements_5",
        "category": "recon",
        "path": "plugins\\recon\\requirements_5\\plugin.py"
    },
    {
        "name": "resiliencetest",
        "category": "recon",
        "path": "plugins\\recon\\resiliencetest\\plugin.py"
    },
    {
        "name": "resolvers_test",
        "category": "recon",
        "path": "plugins\\recon\\resolvers_test\\plugin.py"
    },
    {
        "name": "resources",
        "category": "recon",
        "path": "plugins\\recon\\resources\\plugin.py"
    },
    {
        "name": "retrieval_postprocess_test",
        "category": "recon",
        "path": "plugins\\recon\\retrieval_postprocess_test\\plugin.py"
    },
    {
        "name": "rigid",
        "category": "recon",
        "path": "plugins\\recon\\rigid\\plugin.py"
    },
    {
        "name": "rigid_test",
        "category": "recon",
        "path": "plugins\\recon\\rigid_test\\plugin.py"
    },
    {
        "name": "rpcclient",
        "category": "recon",
        "path": "plugins\\recon\\rpcclient\\plugin.py"
    },
    {
        "name": "rpcdump",
        "category": "recon",
        "path": "plugins\\recon\\rpcdump\\plugin.py"
    },
    {
        "name": "rsync-list-files",
        "category": "recon",
        "path": "plugins\\recon\\rsync-list-files\\plugin.py"
    },
    {
        "name": "run",
        "category": "recon",
        "path": "plugins\\recon\\run\\plugin.py"
    },
    {
        "name": "run-shannon-blackbox",
        "category": "recon",
        "path": "plugins\\recon\\run-shannon-blackbox\\plugin.py"
    },
    {
        "name": "run_all",
        "category": "recon",
        "path": "plugins\\recon\\run_all\\plugin.py"
    },
    {
        "name": "run_bench",
        "category": "recon",
        "path": "plugins\\recon\\run_bench\\plugin.py"
    },
    {
        "name": "rustscan",
        "category": "recon",
        "path": "plugins\\recon\\rustscan\\plugin.py"
    },
    {
        "name": "rustscan_tool",
        "category": "recon",
        "path": "plugins\\recon\\rustscan_tool\\plugin.py"
    },
    {
        "name": "server_https_bootstrap",
        "category": "recon",
        "path": "plugins\\recon\\server_https_bootstrap\\plugin.py"
    },
    {
        "name": "shannon",
        "category": "recon",
        "path": "plugins\\recon\\shannon\\plugin.py"
    },
    {
        "name": "showmount",
        "category": "recon",
        "path": "plugins\\recon\\showmount\\plugin.py"
    },
    {
        "name": "sipvicious",
        "category": "recon",
        "path": "plugins\\recon\\sipvicious\\plugin.py"
    },
    {
        "name": "sleep",
        "category": "recon",
        "path": "plugins\\recon\\sleep\\plugin.py"
    },
    {
        "name": "smb-vuln",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\smb-vuln\\plugin.py"
    },
    {
        "name": "smbclient",
        "category": "recon",
        "path": "plugins\\recon\\smbclient\\plugin.py"
    },
    {
        "name": "smbmap",
        "category": "recon",
        "path": "plugins\\recon\\smbmap\\plugin.py"
    },
    {
        "name": "snmpwalk",
        "category": "recon",
        "path": "plugins\\recon\\snmpwalk\\plugin.py"
    },
    {
        "name": "SslTrustAll",
        "category": "recon",
        "path": "plugins\\recon\\SslTrustAll\\plugin.py"
    },
    {
        "name": "subprocess_mixin",
        "category": "recon",
        "path": "plugins\\recon\\subprocess_mixin\\plugin.py"
    },
    {
        "name": "subprocess_runner",
        "category": "recon",
        "path": "plugins\\recon\\subprocess_runner\\plugin.py"
    },
    {
        "name": "terminal_ws_unix",
        "category": "recon",
        "path": "plugins\\recon\\terminal_ws_unix\\plugin.py"
    },
    {
        "name": "terrascan",
        "category": "recon",
        "path": "plugins\\recon\\terrascan\\plugin.py"
    },
    {
        "name": "test_cli_vps_count",
        "category": "recon",
        "path": "plugins\\recon\\test_cli_vps_count\\plugin.py"
    },
    {
        "name": "test_ensure_webs_all",
        "category": "recon",
        "path": "plugins\\recon\\test_ensure_webs_all\\plugin.py"
    },
    {
        "name": "test_exec_context",
        "category": "recon",
        "path": "plugins\\recon\\test_exec_context\\plugin.py"
    },
    {
        "name": "test_injection",
        "category": "recon",
        "path": "plugins\\recon\\test_injection\\plugin.py"
    },
    {
        "name": "test_mcp_setup",
        "category": "recon",
        "path": "plugins\\recon\\test_mcp_setup\\plugin.py"
    },
    {
        "name": "test_permutation_wordlist_select",
        "category": "recon",
        "path": "plugins\\recon\\test_permutation_wordlist_select\\plugin.py"
    },
    {
        "name": "test_process_registry",
        "category": "recon",
        "path": "plugins\\recon\\test_process_registry\\plugin.py"
    },
    {
        "name": "test_profile_migration",
        "category": "recon",
        "path": "plugins\\recon\\test_profile_migration\\plugin.py"
    },
    {
        "name": "test_resolver_env",
        "category": "recon",
        "path": "plugins\\recon\\test_resolver_env\\plugin.py"
    },
    {
        "name": "test_secure_credential",
        "category": "recon",
        "path": "plugins\\recon\\test_secure_credential\\plugin.py"
    },
    {
        "name": "test_target_expander",
        "category": "recon",
        "path": "plugins\\recon\\test_target_expander\\plugin.py"
    },
    {
        "name": "test_tracing_coverage",
        "category": "recon",
        "path": "plugins\\recon\\test_tracing_coverage\\plugin.py"
    },
    {
        "name": "test_verbosity",
        "category": "recon",
        "path": "plugins\\recon\\test_verbosity\\plugin.py"
    },
    {
        "name": "trivy",
        "category": "recon",
        "path": "plugins\\recon\\trivy\\plugin.py"
    },
    {
        "name": "tsconfig",
        "category": "recon",
        "path": "plugins\\recon\\tsconfig\\plugin.py"
    },
    {
        "name": "tsconfigbase",
        "category": "recon",
        "path": "plugins\\recon\\tsconfigbase\\plugin.py"
    },
    {
        "name": "tsconfig_1",
        "category": "recon",
        "path": "plugins\\recon\\tsconfig_1\\plugin.py"
    },
    {
        "name": "turbo",
        "category": "recon",
        "path": "plugins\\recon\\turbo\\plugin.py"
    },
    {
        "name": "webhooks",
        "category": "recon",
        "path": "plugins\\recon\\webhooks\\plugin.py"
    },
    {
        "name": "whatweb",
        "category": "recon",
        "path": "plugins\\recon\\whatweb\\plugin.py"
    },
    {
        "name": "winrm-detection",
        "category": "recon",
        "path": "plugins\\recon\\winrm-detection\\plugin.py"
    },
    {
        "name": "wordlist_test",
        "category": "recon",
        "path": "plugins\\recon\\wordlist_test\\plugin.py"
    },
    {
        "name": "_13",
        "category": "recon",
        "path": "plugins\\recon\\_13\\plugin.py"
    },
    {
        "name": "__init___201",
        "category": "recon",
        "path": "plugins\\recon\\__init___201\\plugin.py"
    },
    {
        "name": "__init___205",
        "category": "recon",
        "path": "plugins\\recon\\__init___205\\plugin.py"
    },
    {
        "name": "__init___51",
        "category": "recon",
        "path": "plugins\\recon\\__init___51\\plugin.py"
    },
    {
        "name": "acquifinder",
        "category": "recon",
        "path": "plugins\\recon\\acquifinder\\plugin.py"
    },
    {
        "name": "activity-logger",
        "category": "recon",
        "path": "plugins\\recon\\activity-logger\\plugin.py"
    },
    {
        "name": "activity-logger_1",
        "category": "recon",
        "path": "plugins\\recon\\activity-logger_1\\plugin.py"
    },
    {
        "name": "bloodhound",
        "category": "recon",
        "path": "plugins\\recon\\bloodhound\\plugin.py"
    },
    {
        "name": "domain-profiler",
        "category": "recon",
        "path": "plugins\\recon\\domain-profiler\\plugin.py"
    },
    {
        "name": "error-formatter",
        "category": "recon",
        "path": "plugins\\recon\\error-formatter\\plugin.py"
    },
    {
        "name": "feature_request",
        "category": "recon",
        "path": "plugins\\recon\\feature_request\\plugin.py"
    },
    {
        "name": "file-io",
        "category": "recon",
        "path": "plugins\\recon\\file-io\\plugin.py"
    },
    {
        "name": "file-operations",
        "category": "recon",
        "path": "plugins\\recon\\file-operations\\plugin.py"
    },
    {
        "name": "glob",
        "category": "recon",
        "path": "plugins\\recon\\glob\\plugin.py"
    },
    {
        "name": "input-validator",
        "category": "recon",
        "path": "plugins\\recon\\input-validator\\plugin.py"
    },
    {
        "name": "junit_xml",
        "category": "recon",
        "path": "plugins\\recon\\junit_xml\\plugin.py"
    },
    {
        "name": "Keygraph_Button",
        "category": "recon",
        "path": "plugins\\recon\\Keygraph_Button\\plugin.py"
    },
    {
        "name": "metrics_1",
        "category": "recon",
        "path": "plugins\\recon\\metrics_1\\plugin.py"
    },
    {
        "name": "progress-indicator",
        "category": "recon",
        "path": "plugins\\recon\\progress-indicator\\plugin.py"
    },
    {
        "name": "totp-validator",
        "category": "recon",
        "path": "plugins\\recon\\totp-validator\\plugin.py"
    },
    {
        "name": "__init___207",
        "category": "recon",
        "path": "plugins\\recon\\__init___207\\plugin.py"
    },
    {
        "name": "fingerprinting",
        "category": "recon",
        "path": "plugins\\recon\\fingerprinting\\plugin.py"
    },
    {
        "name": "http_headers",
        "category": "recon",
        "path": "plugins\\recon\\http_headers\\plugin.py"
    },
    {
        "name": "contacts",
        "category": "osint",
        "path": "plugins\\osint\\contacts\\plugin.py"
    },
    {
        "name": "metadata",
        "category": "osint",
        "path": "plugins\\osint\\metadata\\plugin.py"
    },
    {
        "name": "service_detection",
        "category": "recon",
        "path": "plugins\\recon\\service_detection\\plugin.py"
    },
    {
        "name": "ssl",
        "category": "recon",
        "path": "plugins\\recon\\ssl\\plugin.py"
    },
    {
        "name": "tech_detection",
        "category": "recon",
        "path": "plugins\\recon\\tech_detection\\plugin.py"
    },
    {
        "name": "ARCHITECTURE_2",
        "category": "recon",
        "path": "plugins\\recon\\ARCHITECTURE_2\\plugin.py"
    },
    {
        "name": "bucket_exposure_engine",
        "category": "recon",
        "path": "plugins\\recon\\bucket_exposure_engine\\plugin.py"
    },
    {
        "name": "codeql",
        "category": "recon",
        "path": "plugins\\recon\\codeql\\plugin.py"
    },
    {
        "name": "codeql-analysis",
        "category": "recon",
        "path": "plugins\\recon\\codeql-analysis\\plugin.py"
    },
    {
        "name": "conversation_manager",
        "category": "recon",
        "path": "plugins\\recon\\conversation_manager\\plugin.py"
    },
    {
        "name": "dep-auto-merge",
        "category": "recon",
        "path": "plugins\\recon\\dep-auto-merge\\plugin.py"
    },
    {
        "name": "eino_meta",
        "category": "recon",
        "path": "plugins\\recon\\eino_meta\\plugin.py"
    },
    {
        "name": "execution-runner",
        "category": "recon",
        "path": "plugins\\recon\\execution-runner\\plugin.py"
    },
    {
        "name": "functional",
        "category": "recon",
        "path": "plugins\\recon\\functional\\plugin.py"
    },
    {
        "name": "gosum",
        "category": "recon",
        "path": "plugins\\recon\\gosum\\plugin.py"
    },
    {
        "name": "health-monitor",
        "category": "recon",
        "path": "plugins\\recon\\health-monitor\\plugin.py"
    },
    {
        "name": "index_2",
        "category": "recon",
        "path": "plugins\\recon\\index_2\\plugin.py"
    },
    {
        "name": "meta-cognition",
        "category": "recon",
        "path": "plugins\\recon\\meta-cognition\\plugin.py"
    },
    {
        "name": "queue-validator",
        "category": "recon",
        "path": "plugins\\recon\\queue-validator\\plugin.py"
    },
    {
        "name": "README_25",
        "category": "recon",
        "path": "plugins\\recon\\README_25\\plugin.py"
    },
    {
        "name": "README_9",
        "category": "recon",
        "path": "plugins\\recon\\README_9\\plugin.py"
    },
    {
        "name": "recorder",
        "category": "recon",
        "path": "plugins\\recon\\recorder\\plugin.py"
    },
    {
        "name": "release-binary",
        "category": "recon",
        "path": "plugins\\recon\\release-binary\\plugin.py"
    },
    {
        "name": "release-test",
        "category": "recon",
        "path": "plugins\\recon\\release-test\\plugin.py"
    },
    {
        "name": "rustscan_2",
        "category": "recon",
        "path": "plugins\\recon\\rustscan_2\\plugin.py"
    },
    {
        "name": "tests",
        "category": "recon",
        "path": "plugins\\recon\\tests\\plugin.py"
    },
    {
        "name": "update",
        "category": "recon",
        "path": "plugins\\recon\\update\\plugin.py"
    },
    {
        "name": "vulnerability_1",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\vulnerability_1\\plugin.py"
    },
    {
        "name": "__init___147",
        "category": "recon",
        "path": "plugins\\recon\\__init___147\\plugin.py"
    },
    {
        "name": "__init___224",
        "category": "recon",
        "path": "plugins\\recon\\__init___224\\plugin.py"
    },
    {
        "name": "__init___231",
        "category": "recon",
        "path": "plugins\\recon\\__init___231\\plugin.py"
    },
    {
        "name": "__init___57",
        "category": "recon",
        "path": "plugins\\recon\\__init___57\\plugin.py"
    },
    {
        "name": "auth_1",
        "category": "osint",
        "path": "plugins\\osint\\auth_1\\plugin.py"
    },
    {
        "name": "backfill-arch-data",
        "category": "osint",
        "path": "plugins\\osint\\backfill-arch-data\\plugin.py"
    },
    {
        "name": "conftest_1",
        "category": "osint",
        "path": "plugins\\osint\\conftest_1\\plugin.py"
    },
    {
        "name": "COOKIES",
        "category": "osint",
        "path": "plugins\\osint\\COOKIES\\plugin.py"
    },
    {
        "name": "credential_tester_agent",
        "category": "osint",
        "path": "plugins\\osint\\credential_tester_agent\\plugin.py"
    },
    {
        "name": "crtsh",
        "category": "osint",
        "path": "plugins\\osint\\crtsh\\plugin.py"
    },
    {
        "name": "environment",
        "category": "osint",
        "path": "plugins\\osint\\environment\\plugin.py"
    },
    {
        "name": "holehe",
        "category": "osint",
        "path": "plugins\\osint\\holehe\\plugin.py"
    },
    {
        "name": "intel-collection",
        "category": "osint",
        "path": "plugins\\osint\\intel-collection\\plugin.py"
    },
    {
        "name": "parsers_1",
        "category": "osint",
        "path": "plugins\\osint\\parsers_1\\plugin.py"
    },
    {
        "name": "phoneinfoga",
        "category": "osint",
        "path": "plugins\\osint\\phoneinfoga\\plugin.py"
    },
    {
        "name": "privacy_detect",
        "category": "osint",
        "path": "plugins\\osint\\privacy_detect\\plugin.py"
    },
    {
        "name": "sdk",
        "category": "osint",
        "path": "plugins\\osint\\sdk\\plugin.py"
    },
    {
        "name": "smtp-user-enum",
        "category": "osint",
        "path": "plugins\\osint\\smtp-user-enum\\plugin.py"
    },
    {
        "name": "social_engineer_agent",
        "category": "osint",
        "path": "plugins\\osint\\social_engineer_agent\\plugin.py"
    },
    {
        "name": "splash-screen",
        "category": "osint",
        "path": "plugins\\osint\\splash-screen\\plugin.py"
    },
    {
        "name": "test_probe_password_reset_weak",
        "category": "osint",
        "path": "plugins\\osint\\test_probe_password_reset_weak\\plugin.py"
    },
    {
        "name": "validation",
        "category": "osint",
        "path": "plugins\\osint\\validation\\plugin.py"
    },
    {
        "name": "vulnscan",
        "category": "osint",
        "path": "plugins\\osint\\vulnscan\\plugin.py"
    },
    {
        "name": "whois_tool",
        "category": "osint",
        "path": "plugins\\osint\\whois_tool\\plugin.py"
    },
    {
        "name": "_safety",
        "category": "osint",
        "path": "plugins\\osint\\_safety\\plugin.py"
    },
    {
        "name": "__init___125",
        "category": "osint",
        "path": "plugins\\osint\\__init___125\\plugin.py"
    },
    {
        "name": "__init___128",
        "category": "osint",
        "path": "plugins\\osint\\__init___128\\plugin.py"
    },
    {
        "name": "arbiter",
        "category": "recon",
        "path": "plugins\\recon\\arbiter\\plugin.py"
    },
    {
        "name": "auth_2",
        "category": "recon",
        "path": "plugins\\recon\\auth_2\\plugin.py"
    },
    {
        "name": "debug-world-model",
        "category": "recon",
        "path": "plugins\\recon\\debug-world-model\\plugin.py"
    },
    {
        "name": "dotdotpwn",
        "category": "recon",
        "path": "plugins\\recon\\dotdotpwn\\plugin.py"
    },
    {
        "name": "exposure_prioritizer",
        "category": "recon",
        "path": "plugins\\recon\\exposure_prioritizer\\plugin.py"
    },
    {
        "name": "fingerprint_correlator",
        "category": "recon",
        "path": "plugins\\recon\\fingerprint_correlator\\plugin.py"
    },
    {
        "name": "index_15",
        "category": "recon",
        "path": "plugins\\recon\\index_15\\plugin.py"
    },
    {
        "name": "index_16",
        "category": "recon",
        "path": "plugins\\recon\\index_16\\plugin.py"
    },
    {
        "name": "lint_python",
        "category": "recon",
        "path": "plugins\\recon\\lint_python\\plugin.py"
    },
    {
        "name": "main_7",
        "category": "recon",
        "path": "plugins\\recon\\main_7\\plugin.py"
    },
    {
        "name": "model-registry",
        "category": "recon",
        "path": "plugins\\recon\\model-registry\\plugin.py"
    },
    {
        "name": "netexec",
        "category": "recon",
        "path": "plugins\\recon\\netexec\\plugin.py"
    },
    {
        "name": "package",
        "category": "recon",
        "path": "plugins\\recon\\package\\plugin.py"
    },
    {
        "name": "plugin_loader",
        "category": "recon",
        "path": "plugins\\recon\\plugin_loader\\plugin.py"
    },
    {
        "name": "portscan-guess-tcp-ports",
        "category": "recon",
        "path": "plugins\\recon\\portscan-guess-tcp-ports\\plugin.py"
    },
    {
        "name": "README_12",
        "category": "recon",
        "path": "plugins\\recon\\README_12\\plugin.py"
    },
    {
        "name": "registry_3",
        "category": "recon",
        "path": "plugins\\recon\\registry_3\\plugin.py"
    },
    {
        "name": "releaserc",
        "category": "recon",
        "path": "plugins\\recon\\releaserc\\plugin.py"
    },
    {
        "name": "renderers",
        "category": "recon",
        "path": "plugins\\recon\\renderers\\plugin.py"
    },
    {
        "name": "test_plugin_loader",
        "category": "recon",
        "path": "plugins\\recon\\test_plugin_loader\\plugin.py"
    },
    {
        "name": "tools_commands",
        "category": "recon",
        "path": "plugins\\recon\\tools_commands\\plugin.py"
    },
    {
        "name": "tooltipcpython-313",
        "category": "recon",
        "path": "plugins\\recon\\tooltipcpython-313\\plugin.py"
    },
    {
        "name": "validatorcpython-313",
        "category": "recon",
        "path": "plugins\\recon\\validatorcpython-313\\plugin.py"
    },
    {
        "name": "volatility3",
        "category": "recon",
        "path": "plugins\\recon\\volatility3\\plugin.py"
    },
    {
        "name": "whatweb_2",
        "category": "recon",
        "path": "plugins\\recon\\whatweb_2\\plugin.py"
    },
    {
        "name": "__init__cpython-313",
        "category": "recon",
        "path": "plugins\\recon\\__init__cpython-313\\plugin.py"
    },
    {
        "name": "__init__cpython-313_1",
        "category": "recon",
        "path": "plugins\\recon\\__init__cpython-313_1\\plugin.py"
    },
    {
        "name": "__init___212",
        "category": "recon",
        "path": "plugins\\recon\\__init___212\\plugin.py"
    },
    {
        "name": "__init___213",
        "category": "recon",
        "path": "plugins\\recon\\__init___213\\plugin.py"
    },
    {
        "name": "__init___214",
        "category": "recon",
        "path": "plugins\\recon\\__init___214\\plugin.py"
    },
    {
        "name": "__init___215",
        "category": "recon",
        "path": "plugins\\recon\\__init___215\\plugin.py"
    },
    {
        "name": "__init___216",
        "category": "recon",
        "path": "plugins\\recon\\__init___216\\plugin.py"
    },
    {
        "name": "__init___217",
        "category": "recon",
        "path": "plugins\\recon\\__init___217\\plugin.py"
    },
    {
        "name": "__init___28",
        "category": "recon",
        "path": "plugins\\recon\\__init___28\\plugin.py"
    },
    {
        "name": "__init___43",
        "category": "recon",
        "path": "plugins\\recon\\__init___43\\plugin.py"
    },
    {
        "name": "__init___58",
        "category": "recon",
        "path": "plugins\\recon\\__init___58\\plugin.py"
    },
    {
        "name": "__init___71",
        "category": "recon",
        "path": "plugins\\recon\\__init___71\\plugin.py"
    },
    {
        "name": "2dd29513_findings",
        "category": "recon",
        "path": "plugins\\recon\\2dd29513_findings\\plugin.py"
    },
    {
        "name": "2dd29513_run_B_safe",
        "category": "recon",
        "path": "plugins\\recon\\2dd29513_run_B_safe\\plugin.py"
    },
    {
        "name": "active-crawl",
        "category": "recon",
        "path": "plugins\\recon\\active-crawl\\plugin.py"
    },
    {
        "name": "active_scanning",
        "category": "recon",
        "path": "plugins\\recon\\active_scanning\\plugin.py"
    },
    {
        "name": "ad-attacker",
        "category": "recon",
        "path": "plugins\\recon\\ad-attacker\\plugin.py"
    },
    {
        "name": "adapter",
        "category": "recon",
        "path": "plugins\\recon\\adapter\\plugin.py"
    },
    {
        "name": "addr",
        "category": "recon",
        "path": "plugins\\recon\\addr\\plugin.py"
    },
    {
        "name": "agent",
        "category": "recon",
        "path": "plugins\\recon\\agent\\plugin.py"
    },
    {
        "name": "AGENTS",
        "category": "recon",
        "path": "plugins\\recon\\AGENTS\\plugin.py"
    },
    {
        "name": "AGENTS_1",
        "category": "recon",
        "path": "plugins\\recon\\AGENTS_1\\plugin.py"
    },
    {
        "name": "agent_3",
        "category": "recon",
        "path": "plugins\\recon\\agent_3\\plugin.py"
    },
    {
        "name": "alerts",
        "category": "recon",
        "path": "plugins\\recon\\alerts\\plugin.py"
    },
    {
        "name": "alerts_1",
        "category": "recon",
        "path": "plugins\\recon\\alerts_1\\plugin.py"
    },
    {
        "name": "alienvault",
        "category": "recon",
        "path": "plugins\\recon\\alienvault\\plugin.py"
    },
    {
        "name": "alterx",
        "category": "recon",
        "path": "plugins\\recon\\alterx\\plugin.py"
    },
    {
        "name": "amass",
        "category": "recon",
        "path": "plugins\\recon\\amass\\plugin.py"
    },
    {
        "name": "amass_2",
        "category": "recon",
        "path": "plugins\\recon\\amass_2\\plugin.py"
    },
    {
        "name": "anomaly_detector",
        "category": "recon",
        "path": "plugins\\recon\\anomaly_detector\\plugin.py"
    },
    {
        "name": "anomaly_engine",
        "category": "recon",
        "path": "plugins\\recon\\anomaly_engine\\plugin.py"
    },
    {
        "name": "anthropic",
        "category": "recon",
        "path": "plugins\\recon\\anthropic\\plugin.py"
    },
    {
        "name": "anubis",
        "category": "recon",
        "path": "plugins\\recon\\anubis\\plugin.py"
    },
    {
        "name": "apex",
        "category": "recon",
        "path": "plugins\\recon\\apex\\plugin.py"
    },
    {
        "name": "api_attack_surface",
        "category": "recon",
        "path": "plugins\\recon\\api_attack_surface\\plugin.py"
    },
    {
        "name": "api_fingerprint",
        "category": "recon",
        "path": "plugins\\recon\\api_fingerprint\\plugin.py"
    },
    {
        "name": "api_models",
        "category": "recon",
        "path": "plugins\\recon\\api_models\\plugin.py"
    },
    {
        "name": "api_path_discovery",
        "category": "recon",
        "path": "plugins\\recon\\api_path_discovery\\plugin.py"
    },
    {
        "name": "architect-infer-agent",
        "category": "recon",
        "path": "plugins\\recon\\architect-infer-agent\\plugin.py"
    },
    {
        "name": "ARCHITECTURE",
        "category": "recon",
        "path": "plugins\\recon\\ARCHITECTURE\\plugin.py"
    },
    {
        "name": "ARCHITECTURE_1",
        "category": "recon",
        "path": "plugins\\recon\\ARCHITECTURE_1\\plugin.py"
    },
    {
        "name": "asncache",
        "category": "recon",
        "path": "plugins\\recon\\asncache\\plugin.py"
    },
    {
        "name": "asnmap",
        "category": "recon",
        "path": "plugins\\recon\\asnmap\\plugin.py"
    },
    {
        "name": "assetfinder",
        "category": "recon",
        "path": "plugins\\recon\\assetfinder\\plugin.py"
    },
    {
        "name": "assets",
        "category": "recon",
        "path": "plugins\\recon\\assets\\plugin.py"
    },
    {
        "name": "assets_test",
        "category": "recon",
        "path": "plugins\\recon\\assets_test\\plugin.py"
    },
    {
        "name": "asset_classifier",
        "category": "recon",
        "path": "plugins\\recon\\asset_classifier\\plugin.py"
    },
    {
        "name": "asset_decode",
        "category": "recon",
        "path": "plugins\\recon\\asset_decode\\plugin.py"
    },
    {
        "name": "asset_secrets_scan",
        "category": "recon",
        "path": "plugins\\recon\\asset_secrets_scan\\plugin.py"
    },
    {
        "name": "assoc",
        "category": "recon",
        "path": "plugins\\recon\\assoc\\plugin.py"
    },
    {
        "name": "attack-chain",
        "category": "recon",
        "path": "plugins\\recon\\attack-chain\\plugin.py"
    },
    {
        "name": "attack-planner",
        "category": "recon",
        "path": "plugins\\recon\\attack-planner\\plugin.py"
    },
    {
        "name": "attack-surface-enumeration",
        "category": "recon",
        "path": "plugins\\recon\\attack-surface-enumeration\\plugin.py"
    },
    {
        "name": "attack_surface_mapper",
        "category": "recon",
        "path": "plugins\\recon\\attack_surface_mapper\\plugin.py"
    },
    {
        "name": "attack_surface_mapping",
        "category": "recon",
        "path": "plugins\\recon\\attack_surface_mapping\\plugin.py"
    },
    {
        "name": "auth-flow-analyzer",
        "category": "recon",
        "path": "plugins\\recon\\auth-flow-analyzer\\plugin.py"
    },
    {
        "name": "authed-findings",
        "category": "recon",
        "path": "plugins\\recon\\authed-findings\\plugin.py"
    },
    {
        "name": "authenticated_scan",
        "category": "recon",
        "path": "plugins\\recon\\authenticated_scan\\plugin.py"
    },
    {
        "name": "auth_handler",
        "category": "recon",
        "path": "plugins\\recon\\auth_handler\\plugin.py"
    },
    {
        "name": "auth_session",
        "category": "recon",
        "path": "plugins\\recon\\auth_session\\plugin.py"
    },
    {
        "name": "autnum",
        "category": "recon",
        "path": "plugins\\recon\\autnum\\plugin.py"
    },
    {
        "name": "autsys",
        "category": "recon",
        "path": "plugins\\recon\\autsys\\plugin.py"
    },
    {
        "name": "autsys_1",
        "category": "recon",
        "path": "plugins\\recon\\autsys_1\\plugin.py"
    },
    {
        "name": "aws_recon",
        "category": "cloud",
        "path": "plugins\\cloud\\aws_recon\\plugin.py"
    },
    {
        "name": "axiom",
        "category": "recon",
        "path": "plugins\\recon\\axiom\\plugin.py"
    },
    {
        "name": "backlog",
        "category": "recon",
        "path": "plugins\\recon\\backlog\\plugin.py"
    },
    {
        "name": "backlog_1",
        "category": "recon",
        "path": "plugins\\recon\\backlog_1\\plugin.py"
    },
    {
        "name": "backlog_test",
        "category": "recon",
        "path": "plugins\\recon\\backlog_test\\plugin.py"
    },
    {
        "name": "banner",
        "category": "recon",
        "path": "plugins\\recon\\banner\\plugin.py"
    },
    {
        "name": "banners",
        "category": "recon",
        "path": "plugins\\recon\\banners\\plugin.py"
    },
    {
        "name": "banner_url",
        "category": "recon",
        "path": "plugins\\recon\\banner_url\\plugin.py"
    },
    {
        "name": "base",
        "category": "recon",
        "path": "plugins\\recon\\base\\plugin.py"
    },
    {
        "name": "base_3",
        "category": "recon",
        "path": "plugins\\recon\\base_3\\plugin.py"
    },
    {
        "name": "bevigil",
        "category": "recon",
        "path": "plugins\\recon\\bevigil\\plugin.py"
    },
    {
        "name": "binaryedge",
        "category": "recon",
        "path": "plugins\\recon\\binaryedge\\plugin.py"
    },
    {
        "name": "bing",
        "category": "recon",
        "path": "plugins\\recon\\bing\\plugin.py"
    },
    {
        "name": "blackbox-config-agent",
        "category": "recon",
        "path": "plugins\\recon\\blackbox-config-agent\\plugin.py"
    },
    {
        "name": "blackbox-context",
        "category": "recon",
        "path": "plugins\\recon\\blackbox-context\\plugin.py"
    },
    {
        "name": "blacklist_test",
        "category": "recon",
        "path": "plugins\\recon\\blacklist_test\\plugin.py"
    },
    {
        "name": "browser-crawler-agent",
        "category": "recon",
        "path": "plugins\\recon\\browser-crawler-agent\\plugin.py"
    },
    {
        "name": "browser_agent",
        "category": "recon",
        "path": "plugins\\recon\\browser_agent\\plugin.py"
    },
    {
        "name": "bufferover",
        "category": "recon",
        "path": "plugins\\recon\\bufferover\\plugin.py"
    },
    {
        "name": "bufferoverrun",
        "category": "recon",
        "path": "plugins\\recon\\bufferoverrun\\plugin.py"
    },
    {
        "name": "bug-bounty",
        "category": "recon",
        "path": "plugins\\recon\\bug-bounty\\plugin.py"
    },
    {
        "name": "bug_report_3",
        "category": "recon",
        "path": "plugins\\recon\\bug_report_3\\plugin.py"
    },
    {
        "name": "build-test",
        "category": "recon",
        "path": "plugins\\recon\\build-test\\plugin.py"
    },
    {
        "name": "builder",
        "category": "recon",
        "path": "plugins\\recon\\builder\\plugin.py"
    },
    {
        "name": "builtwith",
        "category": "recon",
        "path": "plugins\\recon\\builtwith\\plugin.py"
    },
    {
        "name": "burp_suite",
        "category": "recon",
        "path": "plugins\\recon\\burp_suite\\plugin.py"
    },
    {
        "name": "c1ae665a_findings",
        "category": "recon",
        "path": "plugins\\recon\\c1ae665a_findings\\plugin.py"
    },
    {
        "name": "c1ae665a_run_A_default",
        "category": "recon",
        "path": "plugins\\recon\\c1ae665a_run_A_default\\plugin.py"
    },
    {
        "name": "c2-operator",
        "category": "recon",
        "path": "plugins\\recon\\c2-operator\\plugin.py"
    },
    {
        "name": "c2_1",
        "category": "recon",
        "path": "plugins\\recon\\c2_1\\plugin.py"
    },
    {
        "name": "c99",
        "category": "recon",
        "path": "plugins\\recon\\c99\\plugin.py"
    },
    {
        "name": "categories",
        "category": "recon",
        "path": "plugins\\recon\\categories\\plugin.py"
    },
    {
        "name": "censys",
        "category": "recon",
        "path": "plugins\\recon\\censys\\plugin.py"
    },
    {
        "name": "censys_test",
        "category": "recon",
        "path": "plugins\\recon\\censys_test\\plugin.py"
    },
    {
        "name": "certspotter",
        "category": "recon",
        "path": "plugins\\recon\\certspotter\\plugin.py"
    },
    {
        "name": "certspotter_2",
        "category": "recon",
        "path": "plugins\\recon\\certspotter_2\\plugin.py"
    },
    {
        "name": "chain_agent",
        "category": "recon",
        "path": "plugins\\recon\\chain_agent\\plugin.py"
    },
    {
        "name": "CHANGELOG",
        "category": "recon",
        "path": "plugins\\recon\\CHANGELOG\\plugin.py"
    },
    {
        "name": "CHANGELOG_121",
        "category": "recon",
        "path": "plugins\\recon\\CHANGELOG_121\\plugin.py"
    },
    {
        "name": "CHANGELOG_122",
        "category": "recon",
        "path": "plugins\\recon\\CHANGELOG_122\\plugin.py"
    },
    {
        "name": "CHANGELOG_123",
        "category": "recon",
        "path": "plugins\\recon\\CHANGELOG_123\\plugin.py"
    },
    {
        "name": "CHANGELOG_13",
        "category": "recon",
        "path": "plugins\\recon\\CHANGELOG_13\\plugin.py"
    },
    {
        "name": "CHANGELOG_14",
        "category": "recon",
        "path": "plugins\\recon\\CHANGELOG_14\\plugin.py"
    },
    {
        "name": "CHANGELOG_15",
        "category": "recon",
        "path": "plugins\\recon\\CHANGELOG_15\\plugin.py"
    },
    {
        "name": "CHANGELOG_16",
        "category": "recon",
        "path": "plugins\\recon\\CHANGELOG_16\\plugin.py"
    },
    {
        "name": "CHANGELOG_17",
        "category": "recon",
        "path": "plugins\\recon\\CHANGELOG_17\\plugin.py"
    },
    {
        "name": "CHANGELOG_18",
        "category": "recon",
        "path": "plugins\\recon\\CHANGELOG_18\\plugin.py"
    },
    {
        "name": "CHANGELOG_181",
        "category": "recon",
        "path": "plugins\\recon\\CHANGELOG_181\\plugin.py"
    },
    {
        "name": "CHANGELOG_182",
        "category": "recon",
        "path": "plugins\\recon\\CHANGELOG_182\\plugin.py"
    },
    {
        "name": "CHANGELOG_19",
        "category": "recon",
        "path": "plugins\\recon\\CHANGELOG_19\\plugin.py"
    },
    {
        "name": "CHANGELOG_2",
        "category": "recon",
        "path": "plugins\\recon\\CHANGELOG_2\\plugin.py"
    },
    {
        "name": "CHANGELOG_20",
        "category": "recon",
        "path": "plugins\\recon\\CHANGELOG_20\\plugin.py"
    },
    {
        "name": "CHANGELOG_3",
        "category": "recon",
        "path": "plugins\\recon\\CHANGELOG_3\\plugin.py"
    },
    {
        "name": "chaos",
        "category": "recon",
        "path": "plugins\\recon\\chaos\\plugin.py"
    },
    {
        "name": "chaos_2",
        "category": "recon",
        "path": "plugins\\recon\\chaos_2\\plugin.py"
    },
    {
        "name": "check_artifacts",
        "category": "recon",
        "path": "plugins\\recon\\check_artifacts\\plugin.py"
    },
    {
        "name": "chinaz",
        "category": "recon",
        "path": "plugins\\recon\\chinaz\\plugin.py"
    },
    {
        "name": "claims",
        "category": "recon",
        "path": "plugins\\recon\\claims\\plugin.py"
    },
    {
        "name": "CLAUDE_4",
        "category": "recon",
        "path": "plugins\\recon\\CLAUDE_4\\plugin.py"
    },
    {
        "name": "client_1",
        "category": "recon",
        "path": "plugins\\recon\\client_1\\plugin.py"
    },
    {
        "name": "client_4",
        "category": "recon",
        "path": "plugins\\recon\\client_4\\plugin.py"
    },
    {
        "name": "clitest",
        "category": "recon",
        "path": "plugins\\recon\\clitest\\plugin.py"
    },
    {
        "name": "cli_1",
        "category": "recon",
        "path": "plugins\\recon\\cli_1\\plugin.py"
    },
    {
        "name": "cli_2",
        "category": "recon",
        "path": "plugins\\recon\\cli_2\\plugin.py"
    },
    {
        "name": "cli_3",
        "category": "recon",
        "path": "plugins\\recon\\cli_3\\plugin.py"
    },
    {
        "name": "cli_4",
        "category": "recon",
        "path": "plugins\\recon\\cli_4\\plugin.py"
    },
    {
        "name": "cli_5",
        "category": "recon",
        "path": "plugins\\recon\\cli_5\\plugin.py"
    },
    {
        "name": "cloud_fingerprint",
        "category": "cloud",
        "path": "plugins\\cloud\\cloud_fingerprint\\plugin.py"
    },
    {
        "name": "cloud_models",
        "category": "cloud",
        "path": "plugins\\cloud\\cloud_models\\plugin.py"
    },
    {
        "name": "cloud_pipeline",
        "category": "cloud",
        "path": "plugins\\cloud\\cloud_pipeline\\plugin.py"
    },
    {
        "name": "cname",
        "category": "recon",
        "path": "plugins\\recon\\cname\\plugin.py"
    },
    {
        "name": "codecov",
        "category": "recon",
        "path": "plugins\\recon\\codecov\\plugin.py"
    },
    {
        "name": "commoncrawl",
        "category": "recon",
        "path": "plugins\\recon\\commoncrawl\\plugin.py"
    },
    {
        "name": "common_2",
        "category": "recon",
        "path": "plugins\\recon\\common_2\\plugin.py"
    },
    {
        "name": "company_enrich",
        "category": "recon",
        "path": "plugins\\recon\\company_enrich\\plugin.py"
    },
    {
        "name": "company_rounds",
        "category": "recon",
        "path": "plugins\\recon\\company_rounds\\plugin.py"
    },
    {
        "name": "company_search",
        "category": "recon",
        "path": "plugins\\recon\\company_search\\plugin.py"
    },
    {
        "name": "confidence_engine",
        "category": "recon",
        "path": "plugins\\recon\\confidence_engine\\plugin.py"
    },
    {
        "name": "config-parser",
        "category": "recon",
        "path": "plugins\\recon\\config-parser\\plugin.py"
    },
    {
        "name": "config-schema",
        "category": "recon",
        "path": "plugins\\recon\\config-schema\\plugin.py"
    },
    {
        "name": "config-schema_1",
        "category": "recon",
        "path": "plugins\\recon\\config-schema_1\\plugin.py"
    },
    {
        "name": "configtest",
        "category": "recon",
        "path": "plugins\\recon\\configtest\\plugin.py"
    },
    {
        "name": "configure_mcp",
        "category": "recon",
        "path": "plugins\\recon\\configure_mcp\\plugin.py"
    },
    {
        "name": "config_1",
        "category": "recon",
        "path": "plugins\\recon\\config_1\\plugin.py"
    },
    {
        "name": "contact",
        "category": "recon",
        "path": "plugins\\recon\\contact\\plugin.py"
    },
    {
        "name": "container-api",
        "category": "recon",
        "path": "plugins\\recon\\container-api\\plugin.py"
    },
    {
        "name": "content-discovery-agent",
        "category": "recon",
        "path": "plugins\\recon\\content-discovery-agent\\plugin.py"
    },
    {
        "name": "context_analyzer",
        "category": "recon",
        "path": "plugins\\recon\\context_analyzer\\plugin.py"
    },
    {
        "name": "contracts",
        "category": "recon",
        "path": "plugins\\recon\\contracts\\plugin.py"
    },
    {
        "name": "CONTRIBUTING",
        "category": "recon",
        "path": "plugins\\recon\\CONTRIBUTING\\plugin.py"
    },
    {
        "name": "CONTRIBUTING_5",
        "category": "recon",
        "path": "plugins\\recon\\CONTRIBUTING_5\\plugin.py"
    },
    {
        "name": "cookie_prefix_bypass",
        "category": "recon",
        "path": "plugins\\recon\\cookie_prefix_bypass\\plugin.py"
    },
    {
        "name": "core",
        "category": "recon",
        "path": "plugins\\recon\\core\\plugin.py"
    },
    {
        "name": "correlation_engine",
        "category": "recon",
        "path": "plugins\\recon\\correlation_engine\\plugin.py"
    },
    {
        "name": "COVERAGE",
        "category": "recon",
        "path": "plugins\\recon\\COVERAGE\\plugin.py"
    },
    {
        "name": "COVERAGE_1",
        "category": "recon",
        "path": "plugins\\recon\\COVERAGE_1\\plugin.py"
    },
    {
        "name": "crawler",
        "category": "recon",
        "path": "plugins\\recon\\crawler\\plugin.py"
    },
    {
        "name": "crawler-agent",
        "category": "recon",
        "path": "plugins\\recon\\crawler-agent\\plugin.py"
    },
    {
        "name": "crawlercpython-313",
        "category": "recon",
        "path": "plugins\\recon\\crawlercpython-313\\plugin.py"
    },
    {
        "name": "crawler_1",
        "category": "recon",
        "path": "plugins\\recon\\crawler_1\\plugin.py"
    },
    {
        "name": "crawler_2",
        "category": "recon",
        "path": "plugins\\recon\\crawler_2\\plugin.py"
    },
    {
        "name": "crawler_3",
        "category": "recon",
        "path": "plugins\\recon\\crawler_3\\plugin.py"
    },
    {
        "name": "credential-tester",
        "category": "recon",
        "path": "plugins\\recon\\credential-tester\\plugin.py"
    },
    {
        "name": "credentialed-scans",
        "category": "recon",
        "path": "plugins\\recon\\credentialed-scans\\plugin.py"
    },
    {
        "name": "crtsh_1",
        "category": "recon",
        "path": "plugins\\recon\\crtsh_1\\plugin.py"
    },
    {
        "name": "crtsh_3",
        "category": "recon",
        "path": "plugins\\recon\\crtsh_3\\plugin.py"
    },
    {
        "name": "ctf-solver",
        "category": "recon",
        "path": "plugins\\recon\\ctf-solver\\plugin.py"
    },
    {
        "name": "dashboard_1",
        "category": "recon",
        "path": "plugins\\recon\\dashboard_1\\plugin.py"
    },
    {
        "name": "data-flow-mapper",
        "category": "recon",
        "path": "plugins\\recon\\data-flow-mapper\\plugin.py"
    },
    {
        "name": "database_1",
        "category": "recon",
        "path": "plugins\\recon\\database_1\\plugin.py"
    },
    {
        "name": "datasources",
        "category": "recon",
        "path": "plugins\\recon\\datasources\\plugin.py"
    },
    {
        "name": "DeathNote_1",
        "category": "recon",
        "path": "plugins\\recon\\DeathNote_1\\plugin.py"
    },
    {
        "name": "decision_engine",
        "category": "recon",
        "path": "plugins\\recon\\decision_engine\\plugin.py"
    },
    {
        "name": "decision_engine_1",
        "category": "recon",
        "path": "plugins\\recon\\decision_engine_1\\plugin.py"
    },
    {
        "name": "dedup",
        "category": "recon",
        "path": "plugins\\recon\\dedup\\plugin.py"
    },
    {
        "name": "deduplicator",
        "category": "recon",
        "path": "plugins\\recon\\deduplicator\\plugin.py"
    },
    {
        "name": "DEPENDENCIES",
        "category": "recon",
        "path": "plugins\\recon\\DEPENDENCIES\\plugin.py"
    },
    {
        "name": "DESIGN-FEATURES",
        "category": "recon",
        "path": "plugins\\recon\\DESIGN-FEATURES\\plugin.py"
    },
    {
        "name": "detection-engineer",
        "category": "recon",
        "path": "plugins\\recon\\detection-engineer\\plugin.py"
    },
    {
        "name": "detection_engine",
        "category": "recon",
        "path": "plugins\\recon\\detection_engine\\plugin.py"
    },
    {
        "name": "digitalyama",
        "category": "recon",
        "path": "plugins\\recon\\digitalyama\\plugin.py"
    },
    {
        "name": "digitorus",
        "category": "recon",
        "path": "plugins\\recon\\digitorus\\plugin.py"
    },
    {
        "name": "dirbrute",
        "category": "recon",
        "path": "plugins\\recon\\dirbrute\\plugin.py"
    },
    {
        "name": "dirbuster",
        "category": "recon",
        "path": "plugins\\recon\\dirbuster\\plugin.py"
    },
    {
        "name": "directories",
        "category": "recon",
        "path": "plugins\\recon\\directories\\plugin.py"
    },
    {
        "name": "DISCLAIMER_2",
        "category": "recon",
        "path": "plugins\\recon\\DISCLAIMER_2\\plugin.py"
    },
    {
        "name": "dispatch",
        "category": "recon",
        "path": "plugins\\recon\\dispatch\\plugin.py"
    },
    {
        "name": "dispatcher",
        "category": "recon",
        "path": "plugins\\recon\\dispatcher\\plugin.py"
    },
    {
        "name": "dns",
        "category": "recon",
        "path": "plugins\\recon\\dns\\plugin.py"
    },
    {
        "name": "dns-reverse-lookup",
        "category": "recon",
        "path": "plugins\\recon\\dns-reverse-lookup\\plugin.py"
    },
    {
        "name": "dns-zone-transfer",
        "category": "recon",
        "path": "plugins\\recon\\dns-zone-transfer\\plugin.py"
    },
    {
        "name": "dnsdb",
        "category": "recon",
        "path": "plugins\\recon\\dnsdb\\plugin.py"
    },
    {
        "name": "dnsdumpster",
        "category": "recon",
        "path": "plugins\\recon\\dnsdumpster\\plugin.py"
    },
    {
        "name": "dnsenum",
        "category": "recon",
        "path": "plugins\\recon\\dnsenum\\plugin.py"
    },
    {
        "name": "dnsenum_tool",
        "category": "recon",
        "path": "plugins\\recon\\dnsenum_tool\\plugin.py"
    },
    {
        "name": "dnshistory",
        "category": "recon",
        "path": "plugins\\recon\\dnshistory\\plugin.py"
    },
    {
        "name": "dnslog",
        "category": "recon",
        "path": "plugins\\recon\\dnslog\\plugin.py"
    },
    {
        "name": "dnsrecon",
        "category": "recon",
        "path": "plugins\\recon\\dnsrecon\\plugin.py"
    },
    {
        "name": "dnsrecon-subdomain-bruteforce",
        "category": "recon",
        "path": "plugins\\recon\\dnsrecon-subdomain-bruteforce\\plugin.py"
    },
    {
        "name": "dnsrecon_tool",
        "category": "recon",
        "path": "plugins\\recon\\dnsrecon_tool\\plugin.py"
    },
    {
        "name": "dnsrepo",
        "category": "recon",
        "path": "plugins\\recon\\dnsrepo\\plugin.py"
    },
    {
        "name": "dnsrepo_2",
        "category": "recon",
        "path": "plugins\\recon\\dnsrepo_2\\plugin.py"
    },
    {
        "name": "dnsx",
        "category": "recon",
        "path": "plugins\\recon\\dnsx\\plugin.py"
    },
    {
        "name": "dnsx_tool",
        "category": "recon",
        "path": "plugins\\recon\\dnsx_tool\\plugin.py"
    },
    {
        "name": "dns_extractor",
        "category": "recon",
        "path": "plugins\\recon\\dns_extractor\\plugin.py"
    },
    {
        "name": "dns_pipeline",
        "category": "recon",
        "path": "plugins\\recon\\dns_pipeline\\plugin.py"
    },
    {
        "name": "dns_test",
        "category": "recon",
        "path": "plugins\\recon\\dns_test\\plugin.py"
    },
    {
        "name": "dns_tool",
        "category": "recon",
        "path": "plugins\\recon\\dns_tool\\plugin.py"
    },
    {
        "name": "doc",
        "category": "recon",
        "path": "plugins\\recon\\doc\\plugin.py"
    },
    {
        "name": "Dockerfile",
        "category": "recon",
        "path": "plugins\\recon\\Dockerfile\\plugin.py"
    },
    {
        "name": "Dockerfile_1",
        "category": "recon",
        "path": "plugins\\recon\\Dockerfile_1\\plugin.py"
    },
    {
        "name": "Dockerfile_10",
        "category": "recon",
        "path": "plugins\\recon\\Dockerfile_10\\plugin.py"
    },
    {
        "name": "Dockerfile_11",
        "category": "recon",
        "path": "plugins\\recon\\Dockerfile_11\\plugin.py"
    },
    {
        "name": "Dockerfile_2",
        "category": "recon",
        "path": "plugins\\recon\\Dockerfile_2\\plugin.py"
    },
    {
        "name": "Dockerfile_5",
        "category": "recon",
        "path": "plugins\\recon\\Dockerfile_5\\plugin.py"
    },
    {
        "name": "Dockerfile_8",
        "category": "recon",
        "path": "plugins\\recon\\Dockerfile_8\\plugin.py"
    },
    {
        "name": "dockerhub-push",
        "category": "recon",
        "path": "plugins\\recon\\dockerhub-push\\plugin.py"
    },
    {
        "name": "docs",
        "category": "recon",
        "path": "plugins\\recon\\docs\\plugin.py"
    },
    {
        "name": "docs_1",
        "category": "recon",
        "path": "plugins\\recon\\docs_1\\plugin.py"
    },
    {
        "name": "doctor",
        "category": "recon",
        "path": "plugins\\recon\\doctor\\plugin.py"
    },
    {
        "name": "doc_1",
        "category": "recon",
        "path": "plugins\\recon\\doc_1\\plugin.py"
    },
    {
        "name": "doc_2",
        "category": "recon",
        "path": "plugins\\recon\\doc_2\\plugin.py"
    },
    {
        "name": "domainsproject",
        "category": "recon",
        "path": "plugins\\recon\\domainsproject\\plugin.py"
    },
    {
        "name": "domain_record",
        "category": "recon",
        "path": "plugins\\recon\\domain_record\\plugin.py"
    },
    {
        "name": "dom_xss",
        "category": "recon",
        "path": "plugins\\recon\\dom_xss\\plugin.py"
    },
    {
        "name": "dot",
        "category": "recon",
        "path": "plugins\\recon\\dot\\plugin.py"
    },
    {
        "name": "dot_test",
        "category": "recon",
        "path": "plugins\\recon\\dot_test\\plugin.py"
    },
    {
        "name": "driftnet",
        "category": "recon",
        "path": "plugins\\recon\\driftnet\\plugin.py"
    },
    {
        "name": "duckduckgo",
        "category": "recon",
        "path": "plugins\\recon\\duckduckgo\\plugin.py"
    },
    {
        "name": "efd01c52_probe_runs",
        "category": "recon",
        "path": "plugins\\recon\\efd01c52_probe_runs\\plugin.py"
    },
    {
        "name": "email",
        "category": "recon",
        "path": "plugins\\recon\\email\\plugin.py"
    },
    {
        "name": "email-osint-agent",
        "category": "osint",
        "path": "plugins\\osint\\email-osint-agent\\plugin.py"
    },
    {
        "name": "employees",
        "category": "recon",
        "path": "plugins\\recon\\employees\\plugin.py"
    },
    {
        "name": "en-US",
        "category": "recon",
        "path": "plugins\\recon\\en-US\\plugin.py"
    },
    {
        "name": "engine",
        "category": "recon",
        "path": "plugins\\recon\\engine\\plugin.py"
    },
    {
        "name": "engineapi",
        "category": "recon",
        "path": "plugins\\recon\\engineapi\\plugin.py"
    },
    {
        "name": "engine_1",
        "category": "recon",
        "path": "plugins\\recon\\engine_1\\plugin.py"
    },
    {
        "name": "enumerate",
        "category": "recon",
        "path": "plugins\\recon\\enumerate\\plugin.py"
    },
    {
        "name": "enumerate_test",
        "category": "recon",
        "path": "plugins\\recon\\enumerate_test\\plugin.py"
    },
    {
        "name": "epistemic-reasoning",
        "category": "recon",
        "path": "plugins\\recon\\epistemic-reasoning\\plugin.py"
    },
    {
        "name": "evaluator",
        "category": "recon",
        "path": "plugins\\recon\\evaluator\\plugin.py"
    },
    {
        "name": "EVIDENCE",
        "category": "recon",
        "path": "plugins\\recon\\EVIDENCE\\plugin.py"
    },
    {
        "name": "evidence-graph",
        "category": "recon",
        "path": "plugins\\recon\\evidence-graph\\plugin.py"
    },
    {
        "name": "evidence-normalizers",
        "category": "recon",
        "path": "plugins\\recon\\evidence-normalizers\\plugin.py"
    },
    {
        "name": "example-blackbox-config",
        "category": "recon",
        "path": "plugins\\recon\\example-blackbox-config\\plugin.py"
    },
    {
        "name": "example-config",
        "category": "recon",
        "path": "plugins\\recon\\example-config\\plugin.py"
    },
    {
        "name": "example-config_1",
        "category": "recon",
        "path": "plugins\\recon\\example-config_1\\plugin.py"
    },
    {
        "name": "example-detection-rule",
        "category": "recon",
        "path": "plugins\\recon\\example-detection-rule\\plugin.py"
    },
    {
        "name": "example-engagement-plan",
        "category": "recon",
        "path": "plugins\\recon\\example-engagement-plan\\plugin.py"
    },
    {
        "name": "example-nmap-analysis",
        "category": "recon",
        "path": "plugins\\recon\\example-nmap-analysis\\plugin.py"
    },
    {
        "name": "execution-log",
        "category": "recon",
        "path": "plugins\\recon\\execution-log\\plugin.py"
    },
    {
        "name": "execution_view",
        "category": "recon",
        "path": "plugins\\recon\\execution_view\\plugin.py"
    },
    {
        "name": "executor",
        "category": "recon",
        "path": "plugins\\recon\\executor\\plugin.py"
    },
    {
        "name": "executor_helpers",
        "category": "recon",
        "path": "plugins\\recon\\executor_helpers\\plugin.py"
    },
    {
        "name": "exif_metadata",
        "category": "recon",
        "path": "plugins\\recon\\exif_metadata\\plugin.py"
    },
    {
        "name": "explanation_engine",
        "category": "recon",
        "path": "plugins\\recon\\explanation_engine\\plugin.py"
    },
    {
        "name": "exploit-chainer",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\exploit-chainer\\plugin.py"
    },
    {
        "name": "exploit-guide",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\exploit-guide\\plugin.py"
    },
    {
        "name": "exploit-ssrf",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\exploit-ssrf\\plugin.py"
    },
    {
        "name": "exploit-ssrf_2",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\exploit-ssrf_2\\plugin.py"
    },
    {
        "name": "exporter",
        "category": "recon",
        "path": "plugins\\recon\\exporter\\plugin.py"
    },
    {
        "name": "exposure_classifier",
        "category": "recon",
        "path": "plugins\\recon\\exposure_classifier\\plugin.py"
    },
    {
        "name": "external-recon",
        "category": "recon",
        "path": "plugins\\recon\\external-recon\\plugin.py"
    },
    {
        "name": "extractor",
        "category": "recon",
        "path": "plugins\\recon\\extractor\\plugin.py"
    },
    {
        "name": "false_positive_filter",
        "category": "recon",
        "path": "plugins\\recon\\false_positive_filter\\plugin.py"
    },
    {
        "name": "fastapi-scaffold",
        "category": "recon",
        "path": "plugins\\recon\\fastapi-scaffold\\plugin.py"
    },
    {
        "name": "feature_request_3",
        "category": "recon",
        "path": "plugins\\recon\\feature_request_3\\plugin.py"
    },
    {
        "name": "ffuf_2",
        "category": "recon",
        "path": "plugins\\recon\\ffuf_2\\plugin.py"
    },
    {
        "name": "fierce",
        "category": "recon",
        "path": "plugins\\recon\\fierce\\plugin.py"
    },
    {
        "name": "fierce_tool",
        "category": "recon",
        "path": "plugins\\recon\\fierce_tool\\plugin.py"
    },
    {
        "name": "file",
        "category": "recon",
        "path": "plugins\\recon\\file\\plugin.py"
    },
    {
        "name": "files",
        "category": "recon",
        "path": "plugins\\recon\\files\\plugin.py"
    },
    {
        "name": "file_upload_validation",
        "category": "recon",
        "path": "plugins\\recon\\file_upload_validation\\plugin.py"
    },
    {
        "name": "filter",
        "category": "recon",
        "path": "plugins\\recon\\filter\\plugin.py"
    },
    {
        "name": "filternet-bayes",
        "category": "recon",
        "path": "plugins\\recon\\filternet-bayes\\plugin.py"
    },
    {
        "name": "find",
        "category": "recon",
        "path": "plugins\\recon\\find\\plugin.py"
    },
    {
        "name": "findings_db",
        "category": "recon",
        "path": "plugins\\recon\\findings_db\\plugin.py"
    },
    {
        "name": "findomain",
        "category": "recon",
        "path": "plugins\\recon\\findomain\\plugin.py"
    },
    {
        "name": "findsubdomains",
        "category": "recon",
        "path": "plugins\\recon\\findsubdomains\\plugin.py"
    },
    {
        "name": "fingerprints",
        "category": "recon",
        "path": "plugins\\recon\\fingerprints\\plugin.py"
    },
    {
        "name": "fofa",
        "category": "recon",
        "path": "plugins\\recon\\fofa\\plugin.py"
    },
    {
        "name": "fofa_2",
        "category": "recon",
        "path": "plugins\\recon\\fofa_2\\plugin.py"
    },
    {
        "name": "fofa_search",
        "category": "recon",
        "path": "plugins\\recon\\fofa_search\\plugin.py"
    },
    {
        "name": "forensics-analyst",
        "category": "recon",
        "path": "plugins\\recon\\forensics-analyst\\plugin.py"
    },
    {
        "name": "fork-philosophy",
        "category": "recon",
        "path": "plugins\\recon\\fork-philosophy\\plugin.py"
    },
    {
        "name": "fqdn",
        "category": "recon",
        "path": "plugins\\recon\\fqdn\\plugin.py"
    },
    {
        "name": "fqdn_endpoint",
        "category": "recon",
        "path": "plugins\\recon\\fqdn_endpoint\\plugin.py"
    },
    {
        "name": "fqdn_lookup",
        "category": "recon",
        "path": "plugins\\recon\\fqdn_lookup\\plugin.py"
    },
    {
        "name": "fullhunt",
        "category": "recon",
        "path": "plugins\\recon\\fullhunt\\plugin.py"
    },
    {
        "name": "full_v0",
        "category": "recon",
        "path": "plugins\\recon\\full_v0\\plugin.py"
    },
    {
        "name": "full_v1",
        "category": "recon",
        "path": "plugins\\recon\\full_v1\\plugin.py"
    },
    {
        "name": "full_v2",
        "category": "recon",
        "path": "plugins\\recon\\full_v2\\plugin.py"
    },
    {
        "name": "FUNDING_1",
        "category": "recon",
        "path": "plugins\\recon\\FUNDING_1\\plugin.py"
    },
    {
        "name": "fuzzy",
        "category": "recon",
        "path": "plugins\\recon\\fuzzy\\plugin.py"
    },
    {
        "name": "fuzz_wordlist",
        "category": "recon",
        "path": "plugins\\recon\\fuzz_wordlist\\plugin.py"
    },
    {
        "name": "gau",
        "category": "recon",
        "path": "plugins\\recon\\gau\\plugin.py"
    },
    {
        "name": "gau_2",
        "category": "recon",
        "path": "plugins\\recon\\gau_2\\plugin.py"
    },
    {
        "name": "gexf",
        "category": "recon",
        "path": "plugins\\recon\\gexf\\plugin.py"
    },
    {
        "name": "gexf_test",
        "category": "recon",
        "path": "plugins\\recon\\gexf_test\\plugin.py"
    },
    {
        "name": "github",
        "category": "recon",
        "path": "plugins\\recon\\github\\plugin.py"
    },
    {
        "name": "github_subdomains",
        "category": "recon",
        "path": "plugins\\recon\\github_subdomains\\plugin.py"
    },
    {
        "name": "gitlab",
        "category": "recon",
        "path": "plugins\\recon\\gitlab\\plugin.py"
    },
    {
        "name": "gleif",
        "category": "recon",
        "path": "plugins\\recon\\gleif\\plugin.py"
    },
    {
        "name": "gleif_1",
        "category": "recon",
        "path": "plugins\\recon\\gleif_1\\plugin.py"
    },
    {
        "name": "global",
        "category": "recon",
        "path": "plugins\\recon\\global\\plugin.py"
    },
    {
        "name": "gobuster",
        "category": "recon",
        "path": "plugins\\recon\\gobuster\\plugin.py"
    },
    {
        "name": "gobuster_2",
        "category": "recon",
        "path": "plugins\\recon\\gobuster_2\\plugin.py"
    },
    {
        "name": "gobuster_tool",
        "category": "recon",
        "path": "plugins\\recon\\gobuster_tool\\plugin.py"
    },
    {
        "name": "goreleaser_1",
        "category": "recon",
        "path": "plugins\\recon\\goreleaser_1\\plugin.py"
    },
    {
        "name": "gospider",
        "category": "recon",
        "path": "plugins\\recon\\gospider\\plugin.py"
    },
    {
        "name": "go_1",
        "category": "recon",
        "path": "plugins\\recon\\go_1\\plugin.py"
    },
    {
        "name": "go_4",
        "category": "recon",
        "path": "plugins\\recon\\go_4\\plugin.py"
    },
    {
        "name": "graph",
        "category": "recon",
        "path": "plugins\\recon\\graph\\plugin.py"
    },
    {
        "name": "graphdb",
        "category": "recon",
        "path": "plugins\\recon\\graphdb\\plugin.py"
    },
    {
        "name": "graphdb_test",
        "category": "recon",
        "path": "plugins\\recon\\graphdb_test\\plugin.py"
    },
    {
        "name": "grepapp",
        "category": "recon",
        "path": "plugins\\recon\\grepapp\\plugin.py"
    },
    {
        "name": "guided",
        "category": "recon",
        "path": "plugins\\recon\\guided\\plugin.py"
    },
    {
        "name": "guided_recon",
        "category": "recon",
        "path": "plugins\\recon\\guided_recon\\plugin.py"
    },
    {
        "name": "guided_recon_1",
        "category": "recon",
        "path": "plugins\\recon\\guided_recon_1\\plugin.py"
    },
    {
        "name": "guided_recon_121",
        "category": "recon",
        "path": "plugins\\recon\\guided_recon_121\\plugin.py"
    },
    {
        "name": "guided_recon_122",
        "category": "recon",
        "path": "plugins\\recon\\guided_recon_122\\plugin.py"
    },
    {
        "name": "guided_view",
        "category": "recon",
        "path": "plugins\\recon\\guided_view\\plugin.py"
    },
    {
        "name": "hackertarget_1",
        "category": "recon",
        "path": "plugins\\recon\\hackertarget_1\\plugin.py"
    },
    {
        "name": "hackertarget_3",
        "category": "recon",
        "path": "plugins\\recon\\hackertarget_3\\plugin.py"
    },
    {
        "name": "hakrawler",
        "category": "recon",
        "path": "plugins\\recon\\hakrawler\\plugin.py"
    },
    {
        "name": "hakrawler_tool",
        "category": "recon",
        "path": "plugins\\recon\\hakrawler_tool\\plugin.py"
    },
    {
        "name": "handlers",
        "category": "recon",
        "path": "plugins\\recon\\handlers\\plugin.py"
    },
    {
        "name": "headers",
        "category": "recon",
        "path": "plugins\\recon\\headers\\plugin.py"
    },
    {
        "name": "header_checker",
        "category": "recon",
        "path": "plugins\\recon\\header_checker\\plugin.py"
    },
    {
        "name": "hexstrike_mcp",
        "category": "recon",
        "path": "plugins\\recon\\hexstrike_mcp\\plugin.py"
    },
    {
        "name": "hexstrike_server",
        "category": "recon",
        "path": "plugins\\recon\\hexstrike_server\\plugin.py"
    },
    {
        "name": "http",
        "category": "recon",
        "path": "plugins\\recon\\http\\plugin.py"
    },
    {
        "name": "http-framework-test",
        "category": "recon",
        "path": "plugins\\recon\\http-framework-test\\plugin.py"
    },
    {
        "name": "httpbinorg__20260515_233823",
        "category": "recon",
        "path": "plugins\\recon\\httpbinorg__20260515_233823\\plugin.py"
    },
    {
        "name": "httpx_tool",
        "category": "recon",
        "path": "plugins\\recon\\httpx_tool\\plugin.py"
    },
    {
        "name": "http_clients",
        "category": "recon",
        "path": "plugins\\recon\\http_clients\\plugin.py"
    },
    {
        "name": "http_test",
        "category": "recon",
        "path": "plugins\\recon\\http_test\\plugin.py"
    },
    {
        "name": "hudsonrock",
        "category": "recon",
        "path": "plugins\\recon\\hudsonrock\\plugin.py"
    },
    {
        "name": "hunterio",
        "category": "recon",
        "path": "plugins\\recon\\hunterio\\plugin.py"
    },
    {
        "name": "i18n",
        "category": "recon",
        "path": "plugins\\recon\\i18n\\plugin.py"
    },
    {
        "name": "idor_sequential",
        "category": "recon",
        "path": "plugins\\recon\\idor_sequential\\plugin.py"
    },
    {
        "name": "index_11",
        "category": "recon",
        "path": "plugins\\recon\\index_11\\plugin.py"
    },
    {
        "name": "index_8",
        "category": "recon",
        "path": "plugins\\recon\\index_8\\plugin.py"
    },
    {
        "name": "info-collect",
        "category": "recon",
        "path": "plugins\\recon\\info-collect\\plugin.py"
    },
    {
        "name": "infrastructure_view",
        "category": "recon",
        "path": "plugins\\recon\\infrastructure_view\\plugin.py"
    },
    {
        "name": "ini",
        "category": "recon",
        "path": "plugins\\recon\\ini\\plugin.py"
    },
    {
        "name": "initialize",
        "category": "recon",
        "path": "plugins\\recon\\initialize\\plugin.py"
    },
    {
        "name": "install",
        "category": "recon",
        "path": "plugins\\recon\\install\\plugin.py"
    },
    {
        "name": "installation",
        "category": "recon",
        "path": "plugins\\recon\\installation\\plugin.py"
    },
    {
        "name": "install_4",
        "category": "recon",
        "path": "plugins\\recon\\install_4\\plugin.py"
    },
    {
        "name": "install_wizard",
        "category": "recon",
        "path": "plugins\\recon\\install_wizard\\plugin.py"
    },
    {
        "name": "integration",
        "category": "recon",
        "path": "plugins\\recon\\integration\\plugin.py"
    },
    {
        "name": "intelligence_concepts",
        "category": "recon",
        "path": "plugins\\recon\\intelligence_concepts\\plugin.py"
    },
    {
        "name": "intelligence_pipeline",
        "category": "recon",
        "path": "plugins\\recon\\intelligence_pipeline\\plugin.py"
    },
    {
        "name": "intelx",
        "category": "recon",
        "path": "plugins\\recon\\intelx\\plugin.py"
    },
    {
        "name": "interactive",
        "category": "recon",
        "path": "plugins\\recon\\interactive\\plugin.py"
    },
    {
        "name": "introduction",
        "category": "recon",
        "path": "plugins\\recon\\introduction\\plugin.py"
    },
    {
        "name": "ipaddr",
        "category": "recon",
        "path": "plugins\\recon\\ipaddr\\plugin.py"
    },
    {
        "name": "ipaddr_endpoint",
        "category": "recon",
        "path": "plugins\\recon\\ipaddr_endpoint\\plugin.py"
    },
    {
        "name": "ipnet",
        "category": "recon",
        "path": "plugins\\recon\\ipnet\\plugin.py"
    },
    {
        "name": "ipverse",
        "category": "recon",
        "path": "plugins\\recon\\ipverse\\plugin.py"
    },
    {
        "name": "ip_netblock",
        "category": "recon",
        "path": "plugins\\recon\\ip_netblock\\plugin.py"
    },
    {
        "name": "issue-report",
        "category": "recon",
        "path": "plugins\\recon\\issue-report\\plugin.py"
    },
    {
        "name": "jarm",
        "category": "recon",
        "path": "plugins\\recon\\jarm\\plugin.py"
    },
    {
        "name": "jsluice_patterns",
        "category": "recon",
        "path": "plugins\\recon\\jsluice_patterns\\plugin.py"
    },
    {
        "name": "js_analyzer",
        "category": "recon",
        "path": "plugins\\recon\\js_analyzer\\plugin.py"
    },
    {
        "name": "juice-shop",
        "category": "recon",
        "path": "plugins\\recon\\juice-shop\\plugin.py"
    },
    {
        "name": "katana",
        "category": "recon",
        "path": "plugins\\recon\\katana\\plugin.py"
    },
    {
        "name": "katana_2",
        "category": "recon",
        "path": "plugins\\recon\\katana_2\\plugin.py"
    },
    {
        "name": "katana_tool",
        "category": "recon",
        "path": "plugins\\recon\\katana_tool\\plugin.py"
    },
    {
        "name": "kiterunner",
        "category": "recon",
        "path": "plugins\\recon\\kiterunner\\plugin.py"
    },
    {
        "name": "kiterunner_tool",
        "category": "recon",
        "path": "plugins\\recon\\kiterunner_tool\\plugin.py"
    },
    {
        "name": "knowledge-base",
        "category": "recon",
        "path": "plugins\\recon\\knowledge-base\\plugin.py"
    },
    {
        "name": "knowledge_base_1",
        "category": "recon",
        "path": "plugins\\recon\\knowledge_base_1\\plugin.py"
    },
    {
        "name": "known_fqdn",
        "category": "recon",
        "path": "plugins\\recon\\known_fqdn\\plugin.py"
    },
    {
        "name": "kubernetes_analyzer",
        "category": "recon",
        "path": "plugins\\recon\\kubernetes_analyzer\\plugin.py"
    },
    {
        "name": "leaked_credentials",
        "category": "recon",
        "path": "plugins\\recon\\leaked_credentials\\plugin.py"
    },
    {
        "name": "leakix",
        "category": "recon",
        "path": "plugins\\recon\\leakix\\plugin.py"
    },
    {
        "name": "leakix_2",
        "category": "recon",
        "path": "plugins\\recon\\leakix_2\\plugin.py"
    },
    {
        "name": "learning_mode",
        "category": "recon",
        "path": "plugins\\recon\\learning_mode\\plugin.py"
    },
    {
        "name": "ledger",
        "category": "recon",
        "path": "plugins\\recon\\ledger\\plugin.py"
    },
    {
        "name": "LegacyPentestRunner",
        "category": "recon",
        "path": "plugins\\recon\\LegacyPentestRunner\\plugin.py"
    },
    {
        "name": "lei_record",
        "category": "recon",
        "path": "plugins\\recon\\lei_record\\plugin.py"
    },
    {
        "name": "LICENSE_14",
        "category": "recon",
        "path": "plugins\\recon\\LICENSE_14\\plugin.py"
    },
    {
        "name": "LICENSE_3",
        "category": "recon",
        "path": "plugins\\recon\\LICENSE_3\\plugin.py"
    },
    {
        "name": "linkedin",
        "category": "recon",
        "path": "plugins\\recon\\linkedin\\plugin.py"
    },
    {
        "name": "listener",
        "category": "recon",
        "path": "plugins\\recon\\listener\\plugin.py"
    },
    {
        "name": "listener_http",
        "category": "recon",
        "path": "plugins\\recon\\listener_http\\plugin.py"
    },
    {
        "name": "live_capture",
        "category": "recon",
        "path": "plugins\\recon\\live_capture\\plugin.py"
    },
    {
        "name": "llm-analyzer",
        "category": "recon",
        "path": "plugins\\recon\\llm-analyzer\\plugin.py"
    },
    {
        "name": "llm-redteam",
        "category": "recon",
        "path": "plugins\\recon\\llm-redteam\\plugin.py"
    },
    {
        "name": "load",
        "category": "recon",
        "path": "plugins\\recon\\load\\plugin.py"
    },
    {
        "name": "local-source-generator",
        "category": "recon",
        "path": "plugins\\recon\\local-source-generator\\plugin.py"
    },
    {
        "name": "location",
        "category": "recon",
        "path": "plugins\\recon\\location\\plugin.py"
    },
    {
        "name": "locations",
        "category": "recon",
        "path": "plugins\\recon\\locations\\plugin.py"
    },
    {
        "name": "location_1",
        "category": "recon",
        "path": "plugins\\recon\\location_1\\plugin.py"
    },
    {
        "name": "log",
        "category": "recon",
        "path": "plugins\\recon\\log\\plugin.py"
    },
    {
        "name": "logo_1",
        "category": "recon",
        "path": "plugins\\recon\\logo_1\\plugin.py"
    },
    {
        "name": "logs",
        "category": "recon",
        "path": "plugins\\recon\\logs\\plugin.py"
    },
    {
        "name": "main_1",
        "category": "recon",
        "path": "plugins\\recon\\main_1\\plugin.py"
    },
    {
        "name": "main_10",
        "category": "recon",
        "path": "plugins\\recon\\main_10\\plugin.py"
    },
    {
        "name": "main_11",
        "category": "recon",
        "path": "plugins\\recon\\main_11\\plugin.py"
    },
    {
        "name": "main_17",
        "category": "recon",
        "path": "plugins\\recon\\main_17\\plugin.py"
    },
    {
        "name": "main_18",
        "category": "recon",
        "path": "plugins\\recon\\main_18\\plugin.py"
    },
    {
        "name": "main_2",
        "category": "recon",
        "path": "plugins\\recon\\main_2\\plugin.py"
    },
    {
        "name": "main_6",
        "category": "recon",
        "path": "plugins\\recon\\main_6\\plugin.py"
    },
    {
        "name": "main_9",
        "category": "recon",
        "path": "plugins\\recon\\main_9\\plugin.py"
    },
    {
        "name": "main_server_tls",
        "category": "recon",
        "path": "plugins\\recon\\main_server_tls\\plugin.py"
    },
    {
        "name": "Makefile_3",
        "category": "recon",
        "path": "plugins\\recon\\Makefile_3\\plugin.py"
    },
    {
        "name": "maltego",
        "category": "recon",
        "path": "plugins\\recon\\maltego\\plugin.py"
    },
    {
        "name": "malware-analyst",
        "category": "recon",
        "path": "plugins\\recon\\malware-analyst\\plugin.py"
    },
    {
        "name": "manager_1",
        "category": "recon",
        "path": "plugins\\recon\\manager_1\\plugin.py"
    },
    {
        "name": "mapcidr",
        "category": "recon",
        "path": "plugins\\recon\\mapcidr\\plugin.py"
    },
    {
        "name": "markers",
        "category": "recon",
        "path": "plugins\\recon\\markers\\plugin.py"
    },
    {
        "name": "marketplace",
        "category": "recon",
        "path": "plugins\\recon\\marketplace\\plugin.py"
    },
    {
        "name": "massdns",
        "category": "recon",
        "path": "plugins\\recon\\massdns\\plugin.py"
    },
    {
        "name": "massdns_tool",
        "category": "recon",
        "path": "plugins\\recon\\massdns_tool\\plugin.py"
    },
    {
        "name": "match",
        "category": "recon",
        "path": "plugins\\recon\\match\\plugin.py"
    },
    {
        "name": "mcp-management",
        "category": "recon",
        "path": "plugins\\recon\\mcp-management\\plugin.py"
    },
    {
        "name": "mcp-stdio2",
        "category": "recon",
        "path": "plugins\\recon\\mcp-stdio2\\plugin.py"
    },
    {
        "name": "menu",
        "category": "recon",
        "path": "plugins\\recon\\menu\\plugin.py"
    },
    {
        "name": "merklemap",
        "category": "recon",
        "path": "plugins\\recon\\merklemap\\plugin.py"
    },
    {
        "name": "metasploit-agent",
        "category": "recon",
        "path": "plugins\\recon\\metasploit-agent\\plugin.py"
    },
    {
        "name": "methodology_engine",
        "category": "recon",
        "path": "plugins\\recon\\methodology_engine\\plugin.py"
    },
    {
        "name": "ModelCommand",
        "category": "recon",
        "path": "plugins\\recon\\ModelCommand\\plugin.py"
    },
    {
        "name": "models_2",
        "category": "recon",
        "path": "plugins\\recon\\models_2\\plugin.py"
    },
    {
        "name": "modes",
        "category": "recon",
        "path": "plugins\\recon\\modes\\plugin.py"
    },
    {
        "name": "MODS",
        "category": "recon",
        "path": "plugins\\recon\\MODS\\plugin.py"
    },
    {
        "name": "MSSQLInjection",
        "category": "recon",
        "path": "plugins\\recon\\MSSQLInjection\\plugin.py"
    },
    {
        "name": "naabu_tool",
        "category": "recon",
        "path": "plugins\\recon\\naabu_tool\\plugin.py"
    },
    {
        "name": "namelist",
        "category": "recon",
        "path": "plugins\\recon\\namelist\\plugin.py"
    },
    {
        "name": "netblock",
        "category": "recon",
        "path": "plugins\\recon\\netblock\\plugin.py"
    },
    {
        "name": "netblock_1",
        "category": "recon",
        "path": "plugins\\recon\\netblock_1\\plugin.py"
    },
    {
        "name": "netlas",
        "category": "recon",
        "path": "plugins\\recon\\netlas\\plugin.py"
    },
    {
        "name": "network-recon",
        "category": "recon",
        "path": "plugins\\recon\\network-recon\\plugin.py"
    },
    {
        "name": "networks",
        "category": "recon",
        "path": "plugins\\recon\\networks\\plugin.py"
    },
    {
        "name": "nextjs_rsc_rce",
        "category": "recon",
        "path": "plugins\\recon\\nextjs_rsc_rce\\plugin.py"
    },
    {
        "name": "next_step_predictor",
        "category": "recon",
        "path": "plugins\\recon\\next_step_predictor\\plugin.py"
    },
    {
        "name": "nikto_2",
        "category": "recon",
        "path": "plugins\\recon\\nikto_2\\plugin.py"
    },
    {
        "name": "nmap-dns",
        "category": "recon",
        "path": "plugins\\recon\\nmap-dns\\plugin.py"
    },
    {
        "name": "nmap-multicast-dns",
        "category": "recon",
        "path": "plugins\\recon\\nmap-multicast-dns\\plugin.py"
    },
    {
        "name": "normalization",
        "category": "recon",
        "path": "plugins\\recon\\normalization\\plugin.py"
    },
    {
        "name": "nosql_fuzz",
        "category": "recon",
        "path": "plugins\\recon\\nosql_fuzz\\plugin.py"
    },
    {
        "name": "notify",
        "category": "recon",
        "path": "plugins\\recon\\notify\\plugin.py"
    },
    {
        "name": "nuclei_2",
        "category": "recon",
        "path": "plugins\\recon\\nuclei_2\\plugin.py"
    },
    {
        "name": "nuclei_tool",
        "category": "recon",
        "path": "plugins\\recon\\nuclei_tool\\plugin.py"
    },
    {
        "name": "oauth_pkce_downgrade",
        "category": "recon",
        "path": "plugins\\recon\\oauth_pkce_downgrade\\plugin.py"
    },
    {
        "name": "ollama",
        "category": "recon",
        "path": "plugins\\recon\\ollama\\plugin.py"
    },
    {
        "name": "onyphe",
        "category": "recon",
        "path": "plugins\\recon\\onyphe\\plugin.py"
    },
    {
        "name": "operations_center",
        "category": "recon",
        "path": "plugins\\recon\\operations_center\\plugin.py"
    },
    {
        "name": "opsec-anonymizer",
        "category": "recon",
        "path": "plugins\\recon\\opsec-anonymizer\\plugin.py"
    },
    {
        "name": "options_2",
        "category": "recon",
        "path": "plugins\\recon\\options_2\\plugin.py"
    },
    {
        "name": "OracleSQLInjection",
        "category": "recon",
        "path": "plugins\\recon\\OracleSQLInjection\\plugin.py"
    },
    {
        "name": "org",
        "category": "recon",
        "path": "plugins\\recon\\org\\plugin.py"
    },
    {
        "name": "orgs",
        "category": "recon",
        "path": "plugins\\recon\\orgs\\plugin.py"
    },
    {
        "name": "org_1",
        "category": "recon",
        "path": "plugins\\recon\\org_1\\plugin.py"
    },
    {
        "name": "org_lei",
        "category": "recon",
        "path": "plugins\\recon\\org_lei\\plugin.py"
    },
    {
        "name": "osint-collector",
        "category": "osint",
        "path": "plugins\\osint\\osint-collector\\plugin.py"
    },
    {
        "name": "outputter",
        "category": "recon",
        "path": "plugins\\recon\\outputter\\plugin.py"
    },
    {
        "name": "package-lock",
        "category": "recon",
        "path": "plugins\\recon\\package-lock\\plugin.py"
    },
    {
        "name": "parallel",
        "category": "recon",
        "path": "plugins\\recon\\parallel\\plugin.py"
    },
    {
        "name": "paramspider",
        "category": "recon",
        "path": "plugins\\recon\\paramspider\\plugin.py"
    },
    {
        "name": "parse",
        "category": "recon",
        "path": "plugins\\recon\\parse\\plugin.py"
    },
    {
        "name": "parsers",
        "category": "recon",
        "path": "plugins\\recon\\parsers\\plugin.py"
    },
    {
        "name": "parser_mixin",
        "category": "recon",
        "path": "plugins\\recon\\parser_mixin\\plugin.py"
    },
    {
        "name": "parse_test",
        "category": "recon",
        "path": "plugins\\recon\\parse_test\\plugin.py"
    },
    {
        "name": "passive",
        "category": "recon",
        "path": "plugins\\recon\\passive\\plugin.py"
    },
    {
        "name": "passivetotal",
        "category": "recon",
        "path": "plugins\\recon\\passivetotal\\plugin.py"
    },
    {
        "name": "payload-crafter",
        "category": "recon",
        "path": "plugins\\recon\\payload-crafter\\plugin.py"
    },
    {
        "name": "pcap_parser",
        "category": "recon",
        "path": "plugins\\recon\\pcap_parser\\plugin.py"
    },
    {
        "name": "pentest-mcp-server",
        "category": "recon",
        "path": "plugins\\recon\\pentest-mcp-server\\plugin.py"
    },
    {
        "name": "PentestGPT-720WebShareName",
        "category": "recon",
        "path": "plugins\\recon\\PentestGPT-720WebShareName\\plugin.py"
    },
    {
        "name": "permutations_list",
        "category": "recon",
        "path": "plugins\\recon\\permutations_list\\plugin.py"
    },
    {
        "name": "permutations_list_short",
        "category": "recon",
        "path": "plugins\\recon\\permutations_list_short\\plugin.py"
    },
    {
        "name": "phishing-operator",
        "category": "recon",
        "path": "plugins\\recon\\phishing-operator\\plugin.py"
    },
    {
        "name": "pipelines",
        "category": "recon",
        "path": "plugins\\recon\\pipelines\\plugin.py"
    },
    {
        "name": "pipeline_engine",
        "category": "recon",
        "path": "plugins\\recon\\pipeline_engine\\plugin.py"
    },
    {
        "name": "planner",
        "category": "recon",
        "path": "plugins\\recon\\planner\\plugin.py"
    },
    {
        "name": "plugin",
        "category": "recon",
        "path": "plugins\\recon\\plugin\\plugin.py"
    },
    {
        "name": "plugin_1",
        "category": "recon",
        "path": "plugins\\recon\\plugin_1\\plugin.py"
    },
    {
        "name": "plugin_10",
        "category": "recon",
        "path": "plugins\\recon\\plugin_10\\plugin.py"
    },
    {
        "name": "plugin_11",
        "category": "recon",
        "path": "plugins\\recon\\plugin_11\\plugin.py"
    },
    {
        "name": "plugin_2",
        "category": "recon",
        "path": "plugins\\recon\\plugin_2\\plugin.py"
    },
    {
        "name": "plugin_4",
        "category": "recon",
        "path": "plugins\\recon\\plugin_4\\plugin.py"
    },
    {
        "name": "plugin_5",
        "category": "recon",
        "path": "plugins\\recon\\plugin_5\\plugin.py"
    },
    {
        "name": "plugin_6",
        "category": "recon",
        "path": "plugins\\recon\\plugin_6\\plugin.py"
    },
    {
        "name": "plugin_7",
        "category": "recon",
        "path": "plugins\\recon\\plugin_7\\plugin.py"
    },
    {
        "name": "plugin_8",
        "category": "recon",
        "path": "plugins\\recon\\plugin_8\\plugin.py"
    },
    {
        "name": "portscan",
        "category": "recon",
        "path": "plugins\\recon\\portscan\\plugin.py"
    },
    {
        "name": "port_prioritizer",
        "category": "recon",
        "path": "plugins\\recon\\port_prioritizer\\plugin.py"
    },
    {
        "name": "PostgreSQLInjection",
        "category": "recon",
        "path": "plugins\\recon\\PostgreSQLInjection\\plugin.py"
    },
    {
        "name": "pre-recon",
        "category": "recon",
        "path": "plugins\\recon\\pre-recon\\plugin.py"
    },
    {
        "name": "preflight",
        "category": "recon",
        "path": "plugins\\recon\\preflight\\plugin.py"
    },
    {
        "name": "preflight-check",
        "category": "recon",
        "path": "plugins\\recon\\preflight-check\\plugin.py"
    },
    {
        "name": "print",
        "category": "recon",
        "path": "plugins\\recon\\print\\plugin.py"
    },
    {
        "name": "PRIVACY",
        "category": "recon",
        "path": "plugins\\recon\\PRIVACY\\plugin.py"
    },
    {
        "name": "process",
        "category": "recon",
        "path": "plugins\\recon\\process\\plugin.py"
    },
    {
        "name": "profundis",
        "category": "recon",
        "path": "plugins\\recon\\profundis\\plugin.py"
    },
    {
        "name": "prospeo",
        "category": "recon",
        "path": "plugins\\recon\\prospeo\\plugin.py"
    },
    {
        "name": "protocol_detector",
        "category": "recon",
        "path": "plugins\\recon\\protocol_detector\\plugin.py"
    },
    {
        "name": "proxy_controller",
        "category": "recon",
        "path": "plugins\\recon\\proxy_controller\\plugin.py"
    },
    {
        "name": "pseudo-source-builder",
        "category": "recon",
        "path": "plugins\\recon\\pseudo-source-builder\\plugin.py"
    },
    {
        "name": "pugrecon",
        "category": "recon",
        "path": "plugins\\recon\\pugrecon\\plugin.py"
    },
    {
        "name": "PULL_REQUEST_TEMPLATE_2",
        "category": "recon",
        "path": "plugins\\recon\\PULL_REQUEST_TEMPLATE_2\\plugin.py"
    },
    {
        "name": "puredns",
        "category": "recon",
        "path": "plugins\\recon\\puredns\\plugin.py"
    },
    {
        "name": "puredns_tool",
        "category": "recon",
        "path": "plugins\\recon\\puredns_tool\\plugin.py"
    },
    {
        "name": "pure_go",
        "category": "recon",
        "path": "plugins\\recon\\pure_go\\plugin.py"
    },
    {
        "name": "pyproject_2",
        "category": "recon",
        "path": "plugins\\recon\\pyproject_2\\plugin.py"
    },
    {
        "name": "pyshark_engine",
        "category": "recon",
        "path": "plugins\\recon\\pyshark_engine\\plugin.py"
    },
    {
        "name": "pythonorg_headers_20241216_000049",
        "category": "recon",
        "path": "plugins\\recon\\pythonorg_headers_20241216_000049\\plugin.py"
    },
    {
        "name": "pythonorg_subdomains_20241215_235829",
        "category": "recon",
        "path": "plugins\\recon\\pythonorg_subdomains_20241215_235829\\plugin.py"
    },
    {
        "name": "quake",
        "category": "recon",
        "path": "plugins\\recon\\quake\\plugin.py"
    },
    {
        "name": "quick_action_bar",
        "category": "recon",
        "path": "plugins\\recon\\quick_action_bar\\plugin.py"
    },
    {
        "name": "ranger",
        "category": "recon",
        "path": "plugins\\recon\\ranger\\plugin.py"
    },
    {
        "name": "rapiddns",
        "category": "recon",
        "path": "plugins\\recon\\rapiddns\\plugin.py"
    },
    {
        "name": "rapiddns_2",
        "category": "recon",
        "path": "plugins\\recon\\rapiddns_2\\plugin.py"
    },
    {
        "name": "ratelimit_test",
        "category": "recon",
        "path": "plugins\\recon\\ratelimit_test\\plugin.py"
    },
    {
        "name": "rdap",
        "category": "recon",
        "path": "plugins\\recon\\rdap\\plugin.py"
    },
    {
        "name": "README",
        "category": "recon",
        "path": "plugins\\recon\\README\\plugin.py"
    },
    {
        "name": "README_1",
        "category": "recon",
        "path": "plugins\\recon\\README_1\\plugin.py"
    },
    {
        "name": "README_17",
        "category": "recon",
        "path": "plugins\\recon\\README_17\\plugin.py"
    },
    {
        "name": "README_18",
        "category": "recon",
        "path": "plugins\\recon\\README_18\\plugin.py"
    },
    {
        "name": "README_2",
        "category": "recon",
        "path": "plugins\\recon\\README_2\\plugin.py"
    },
    {
        "name": "README_20",
        "category": "recon",
        "path": "plugins\\recon\\README_20\\plugin.py"
    },
    {
        "name": "README_27",
        "category": "recon",
        "path": "plugins\\recon\\README_27\\plugin.py"
    },
    {
        "name": "README_3",
        "category": "recon",
        "path": "plugins\\recon\\README_3\\plugin.py"
    },
    {
        "name": "README_39",
        "category": "recon",
        "path": "plugins\\recon\\README_39\\plugin.py"
    },
    {
        "name": "README_4",
        "category": "recon",
        "path": "plugins\\recon\\README_4\\plugin.py"
    },
    {
        "name": "README_41",
        "category": "recon",
        "path": "plugins\\recon\\README_41\\plugin.py"
    },
    {
        "name": "README_42",
        "category": "recon",
        "path": "plugins\\recon\\README_42\\plugin.py"
    },
    {
        "name": "README_43",
        "category": "recon",
        "path": "plugins\\recon\\README_43\\plugin.py"
    },
    {
        "name": "README_44",
        "category": "recon",
        "path": "plugins\\recon\\README_44\\plugin.py"
    },
    {
        "name": "README_45",
        "category": "recon",
        "path": "plugins\\recon\\README_45\\plugin.py"
    },
    {
        "name": "README_47",
        "category": "recon",
        "path": "plugins\\recon\\README_47\\plugin.py"
    },
    {
        "name": "README_48",
        "category": "recon",
        "path": "plugins\\recon\\README_48\\plugin.py"
    },
    {
        "name": "README_49",
        "category": "recon",
        "path": "plugins\\recon\\README_49\\plugin.py"
    },
    {
        "name": "README_5",
        "category": "recon",
        "path": "plugins\\recon\\README_5\\plugin.py"
    },
    {
        "name": "README_51",
        "category": "recon",
        "path": "plugins\\recon\\README_51\\plugin.py"
    },
    {
        "name": "README_52",
        "category": "recon",
        "path": "plugins\\recon\\README_52\\plugin.py"
    },
    {
        "name": "README_53",
        "category": "recon",
        "path": "plugins\\recon\\README_53\\plugin.py"
    },
    {
        "name": "README_57",
        "category": "recon",
        "path": "plugins\\recon\\README_57\\plugin.py"
    },
    {
        "name": "README_58",
        "category": "recon",
        "path": "plugins\\recon\\README_58\\plugin.py"
    },
    {
        "name": "README_8",
        "category": "recon",
        "path": "plugins\\recon\\README_8\\plugin.py"
    },
    {
        "name": "README_CN_1",
        "category": "recon",
        "path": "plugins\\recon\\README_CN_1\\plugin.py"
    },
    {
        "name": "recommend",
        "category": "recon",
        "path": "plugins\\recon\\recommend\\plugin.py"
    },
    {
        "name": "recommendation_engine",
        "category": "recon",
        "path": "plugins\\recon\\recommendation_engine\\plugin.py"
    },
    {
        "name": "recommendation_engine_1",
        "category": "recon",
        "path": "plugins\\recon\\recommendation_engine_1\\plugin.py"
    },
    {
        "name": "recon-advisor",
        "category": "recon",
        "path": "plugins\\recon\\recon-advisor\\plugin.py"
    },
    {
        "name": "reconcloud",
        "category": "cloud",
        "path": "plugins\\cloud\\reconcloud\\plugin.py"
    },
    {
        "name": "reconeer",
        "category": "recon",
        "path": "plugins\\recon\\reconeer\\plugin.py"
    },
    {
        "name": "reconftw",
        "category": "recon",
        "path": "plugins\\recon\\reconftw\\plugin.py"
    },
    {
        "name": "reconftw_1",
        "category": "recon",
        "path": "plugins\\recon\\reconftw_1\\plugin.py"
    },
    {
        "name": "reconftw_full",
        "category": "recon",
        "path": "plugins\\recon\\reconftw_full\\plugin.py"
    },
    {
        "name": "reconftw_stealth",
        "category": "recon",
        "path": "plugins\\recon\\reconftw_stealth\\plugin.py"
    },
    {
        "name": "recon_2",
        "category": "recon",
        "path": "plugins\\recon\\recon_2\\plugin.py"
    },
    {
        "name": "recon_agent",
        "category": "recon",
        "path": "plugins\\recon\\recon_agent\\plugin.py"
    },
    {
        "name": "recon_strategy",
        "category": "recon",
        "path": "plugins\\recon\\recon_strategy\\plugin.py"
    },
    {
        "name": "redhuntlabs",
        "category": "recon",
        "path": "plugins\\recon\\redhuntlabs\\plugin.py"
    },
    {
        "name": "registry_1",
        "category": "recon",
        "path": "plugins\\recon\\registry_1\\plugin.py"
    },
    {
        "name": "registry_121",
        "category": "recon",
        "path": "plugins\\recon\\registry_121\\plugin.py"
    },
    {
        "name": "registry_122",
        "category": "recon",
        "path": "plugins\\recon\\registry_122\\plugin.py"
    },
    {
        "name": "registry_123",
        "category": "recon",
        "path": "plugins\\recon\\registry_123\\plugin.py"
    },
    {
        "name": "registry_181",
        "category": "recon",
        "path": "plugins\\recon\\registry_181\\plugin.py"
    },
    {
        "name": "registry_182",
        "category": "recon",
        "path": "plugins\\recon\\registry_182\\plugin.py"
    },
    {
        "name": "registry_5",
        "category": "recon",
        "path": "plugins\\recon\\registry_5\\plugin.py"
    },
    {
        "name": "registry_test",
        "category": "recon",
        "path": "plugins\\recon\\registry_test\\plugin.py"
    },
    {
        "name": "reg_records",
        "category": "recon",
        "path": "plugins\\recon\\reg_records\\plugin.py"
    },
    {
        "name": "related",
        "category": "recon",
        "path": "plugins\\recon\\related\\plugin.py"
    },
    {
        "name": "relationship_graph",
        "category": "recon",
        "path": "plugins\\recon\\relationship_graph\\plugin.py"
    },
    {
        "name": "relationship_mapper",
        "category": "recon",
        "path": "plugins\\recon\\relationship_mapper\\plugin.py"
    },
    {
        "name": "report-executive_2",
        "category": "recon",
        "path": "plugins\\recon\\report-executive_2\\plugin.py"
    },
    {
        "name": "reporthtml",
        "category": "recon",
        "path": "plugins\\recon\\reporthtml\\plugin.py"
    },
    {
        "name": "report_121",
        "category": "recon",
        "path": "plugins\\recon\\report_121\\plugin.py"
    },
    {
        "name": "report_14",
        "category": "recon",
        "path": "plugins\\recon\\report_14\\plugin.py"
    },
    {
        "name": "report_16",
        "category": "recon",
        "path": "plugins\\recon\\report_16\\plugin.py"
    },
    {
        "name": "report_17",
        "category": "recon",
        "path": "plugins\\recon\\report_17\\plugin.py"
    },
    {
        "name": "report_injector_2",
        "category": "recon",
        "path": "plugins\\recon\\report_injector_2\\plugin.py"
    },
    {
        "name": "requirements",
        "category": "recon",
        "path": "plugins\\recon\\requirements\\plugin.py"
    },
    {
        "name": "requirements_11",
        "category": "recon",
        "path": "plugins\\recon\\requirements_11\\plugin.py"
    },
    {
        "name": "requirements_12",
        "category": "recon",
        "path": "plugins\\recon\\requirements_12\\plugin.py"
    },
    {
        "name": "requirements_16",
        "category": "recon",
        "path": "plugins\\recon\\requirements_16\\plugin.py"
    },
    {
        "name": "requirements_2",
        "category": "recon",
        "path": "plugins\\recon\\requirements_2\\plugin.py"
    },
    {
        "name": "requirements_3",
        "category": "recon",
        "path": "plugins\\recon\\requirements_3\\plugin.py"
    },
    {
        "name": "requirements_8",
        "category": "recon",
        "path": "plugins\\recon\\requirements_8\\plugin.py"
    },
    {
        "name": "resilience",
        "category": "recon",
        "path": "plugins\\recon\\resilience\\plugin.py"
    },
    {
        "name": "resolve",
        "category": "recon",
        "path": "plugins\\recon\\resolve\\plugin.py"
    },
    {
        "name": "resolvers",
        "category": "recon",
        "path": "plugins\\recon\\resolvers\\plugin.py"
    },
    {
        "name": "resolvers_1",
        "category": "recon",
        "path": "plugins\\recon\\resolvers_1\\plugin.py"
    },
    {
        "name": "resolver_manager",
        "category": "recon",
        "path": "plugins\\recon\\resolver_manager\\plugin.py"
    },
    {
        "name": "responder",
        "category": "recon",
        "path": "plugins\\recon\\responder\\plugin.py"
    },
    {
        "name": "RESPONSIBLE_DISCLOSURE",
        "category": "recon",
        "path": "plugins\\recon\\RESPONSIBLE_DISCLOSURE\\plugin.py"
    },
    {
        "name": "rest_api",
        "category": "recon",
        "path": "plugins\\recon\\rest_api\\plugin.py"
    },
    {
        "name": "reverse",
        "category": "recon",
        "path": "plugins\\recon\\reverse\\plugin.py"
    },
    {
        "name": "reverse-engineer",
        "category": "recon",
        "path": "plugins\\recon\\reverse-engineer\\plugin.py"
    },
    {
        "name": "riddler",
        "category": "recon",
        "path": "plugins\\recon\\riddler\\plugin.py"
    },
    {
        "name": "risk_mapper",
        "category": "recon",
        "path": "plugins\\recon\\risk_mapper\\plugin.py"
    },
    {
        "name": "risk_scorer",
        "category": "recon",
        "path": "plugins\\recon\\risk_scorer\\plugin.py"
    },
    {
        "name": "risk_scoring",
        "category": "recon",
        "path": "plugins\\recon\\risk_scoring\\plugin.py"
    },
    {
        "name": "robtext",
        "category": "recon",
        "path": "plugins\\recon\\robtext\\plugin.py"
    },
    {
        "name": "rsecloud",
        "category": "cloud",
        "path": "plugins\\cloud\\rsecloud\\plugin.py"
    },
    {
        "name": "runner_3",
        "category": "recon",
        "path": "plugins\\recon\\runner_3\\plugin.py"
    },
    {
        "name": "run_dvwa_engagement",
        "category": "recon",
        "path": "plugins\\recon\\run_dvwa_engagement\\plugin.py"
    },
    {
        "name": "run_dvwa_full",
        "category": "recon",
        "path": "plugins\\recon\\run_dvwa_full\\plugin.py"
    },
    {
        "name": "run_summary",
        "category": "recon",
        "path": "plugins\\recon\\run_summary\\plugin.py"
    },
    {
        "name": "s3scanner",
        "category": "cloud",
        "path": "plugins\\cloud\\s3scanner\\plugin.py"
    },
    {
        "name": "s3_scanner",
        "category": "cloud",
        "path": "plugins\\cloud\\s3_scanner\\plugin.py"
    },
    {
        "name": "save_results",
        "category": "recon",
        "path": "plugins\\recon\\save_results\\plugin.py"
    },
    {
        "name": "scanners",
        "category": "recon",
        "path": "plugins\\recon\\scanners\\plugin.py"
    },
    {
        "name": "scanner_5",
        "category": "recon",
        "path": "plugins\\recon\\scanner_5\\plugin.py"
    },
    {
        "name": "scheduler",
        "category": "recon",
        "path": "plugins\\recon\\scheduler\\plugin.py"
    },
    {
        "name": "schemas",
        "category": "recon",
        "path": "plugins\\recon\\schemas\\plugin.py"
    },
    {
        "name": "schemas_1",
        "category": "recon",
        "path": "plugins\\recon\\schemas_1\\plugin.py"
    },
    {
        "name": "scope_1",
        "category": "recon",
        "path": "plugins\\recon\\scope_1\\plugin.py"
    },
    {
        "name": "scope_test",
        "category": "recon",
        "path": "plugins\\recon\\scope_test\\plugin.py"
    },
    {
        "name": "SCORE",
        "category": "recon",
        "path": "plugins\\recon\\SCORE\\plugin.py"
    },
    {
        "name": "Screenshot1",
        "category": "recon",
        "path": "plugins\\recon\\Screenshot1\\plugin.py"
    },
    {
        "name": "search_2",
        "category": "recon",
        "path": "plugins\\recon\\search_2\\plugin.py"
    },
    {
        "name": "secretscfg",
        "category": "recon",
        "path": "plugins\\recon\\secretscfg\\plugin.py"
    },
    {
        "name": "security-header-analyzer",
        "category": "recon",
        "path": "plugins\\recon\\security-header-analyzer\\plugin.py"
    },
    {
        "name": "SecurityHeaderAnalyzer",
        "category": "recon",
        "path": "plugins\\recon\\SecurityHeaderAnalyzer\\plugin.py"
    },
    {
        "name": "securitytrails",
        "category": "recon",
        "path": "plugins\\recon\\securitytrails\\plugin.py"
    },
    {
        "name": "securitytrails_2",
        "category": "recon",
        "path": "plugins\\recon\\securitytrails_2\\plugin.py"
    },
    {
        "name": "sensitive_detector",
        "category": "recon",
        "path": "plugins\\recon\\sensitive_detector\\plugin.py"
    },
    {
        "name": "sensitive_domains",
        "category": "recon",
        "path": "plugins\\recon\\sensitive_domains\\plugin.py"
    },
    {
        "name": "server_1",
        "category": "recon",
        "path": "plugins\\recon\\server_1\\plugin.py"
    },
    {
        "name": "service_correlator",
        "category": "recon",
        "path": "plugins\\recon\\service_correlator\\plugin.py"
    },
    {
        "name": "service_learning",
        "category": "recon",
        "path": "plugins\\recon\\service_learning\\plugin.py"
    },
    {
        "name": "session",
        "category": "recon",
        "path": "plugins\\recon\\session\\plugin.py"
    },
    {
        "name": "sessions",
        "category": "recon",
        "path": "plugins\\recon\\sessions\\plugin.py"
    },
    {
        "name": "settings_1",
        "category": "recon",
        "path": "plugins\\recon\\settings_1\\plugin.py"
    },
    {
        "name": "setup_2",
        "category": "recon",
        "path": "plugins\\recon\\setup_2\\plugin.py"
    },
    {
        "name": "shadow-it",
        "category": "recon",
        "path": "plugins\\recon\\shadow-it\\plugin.py"
    },
    {
        "name": "shadow-ittest",
        "category": "recon",
        "path": "plugins\\recon\\shadow-ittest\\plugin.py"
    },
    {
        "name": "shannon-action",
        "category": "recon",
        "path": "plugins\\recon\\shannon-action\\plugin.py"
    },
    {
        "name": "shannon-report-crapi",
        "category": "recon",
        "path": "plugins\\recon\\shannon-report-crapi\\plugin.py"
    },
    {
        "name": "shannon-report-juice-shop",
        "category": "recon",
        "path": "plugins\\recon\\shannon-report-juice-shop\\plugin.py"
    },
    {
        "name": "shannon-scan",
        "category": "recon",
        "path": "plugins\\recon\\shannon-scan\\plugin.py"
    },
    {
        "name": "shannon-screen_1",
        "category": "recon",
        "path": "plugins\\recon\\shannon-screen_1\\plugin.py"
    },
    {
        "name": "shodan_recon_plugin",
        "category": "recon",
        "path": "plugins\\recon\\shodan_recon_plugin\\plugin.py"
    },
    {
        "name": "shuffledns",
        "category": "recon",
        "path": "plugins\\recon\\shuffledns\\plugin.py"
    },
    {
        "name": "shuffledns_tool",
        "category": "recon",
        "path": "plugins\\recon\\shuffledns_tool\\plugin.py"
    },
    {
        "name": "sitedossier",
        "category": "recon",
        "path": "plugins\\recon\\sitedossier\\plugin.py"
    },
    {
        "name": "sitedossier_2",
        "category": "recon",
        "path": "plugins\\recon\\sitedossier_2\\plugin.py"
    },
    {
        "name": "SKILL_20",
        "category": "recon",
        "path": "plugins\\recon\\SKILL_20\\plugin.py"
    },
    {
        "name": "SKILL_5",
        "category": "recon",
        "path": "plugins\\recon\\SKILL_5\\plugin.py"
    },
    {
        "name": "SKILL_6",
        "category": "recon",
        "path": "plugins\\recon\\SKILL_6\\plugin.py"
    },
    {
        "name": "SKILL_8",
        "category": "recon",
        "path": "plugins\\recon\\SKILL_8\\plugin.py"
    },
    {
        "name": "smart-scan",
        "category": "recon",
        "path": "plugins\\recon\\smart-scan\\plugin.py"
    },
    {
        "name": "smart-scan-expanded-toolset",
        "category": "recon",
        "path": "plugins\\recon\\smart-scan-expanded-toolset\\plugin.py"
    },
    {
        "name": "smart-scan-on-search",
        "category": "recon",
        "path": "plugins\\recon\\smart-scan-on-search\\plugin.py"
    },
    {
        "name": "sources",
        "category": "recon",
        "path": "plugins\\recon\\sources\\plugin.py"
    },
    {
        "name": "sources_test",
        "category": "recon",
        "path": "plugins\\recon\\sources_test\\plugin.py"
    },
    {
        "name": "sources_wo_auth_test",
        "category": "recon",
        "path": "plugins\\recon\\sources_wo_auth_test\\plugin.py"
    },
    {
        "name": "sources_w_auth_test",
        "category": "recon",
        "path": "plugins\\recon\\sources_w_auth_test\\plugin.py"
    },
    {
        "name": "spiderfoot",
        "category": "recon",
        "path": "plugins\\recon\\spiderfoot\\plugin.py"
    },
    {
        "name": "spotter",
        "category": "recon",
        "path": "plugins\\recon\\spotter\\plugin.py"
    },
    {
        "name": "sqli_fuzz",
        "category": "recon",
        "path": "plugins\\recon\\sqli_fuzz\\plugin.py"
    },
    {
        "name": "SQLmap",
        "category": "recon",
        "path": "plugins\\recon\\SQLmap\\plugin.py"
    },
    {
        "name": "sqlmap-agent",
        "category": "recon",
        "path": "plugins\\recon\\sqlmap-agent\\plugin.py"
    },
    {
        "name": "srv",
        "category": "recon",
        "path": "plugins\\recon\\srv\\plugin.py"
    },
    {
        "name": "ssl_checker",
        "category": "recon",
        "path": "plugins\\recon\\ssl_checker\\plugin.py"
    },
    {
        "name": "ssrf_cloud_metadata",
        "category": "cloud",
        "path": "plugins\\cloud\\ssrf_cloud_metadata\\plugin.py"
    },
    {
        "name": "ssti_fuzz",
        "category": "recon",
        "path": "plugins\\recon\\ssti_fuzz\\plugin.py"
    },
    {
        "name": "stage121_catalog",
        "category": "recon",
        "path": "plugins\\recon\\stage121_catalog\\plugin.py"
    },
    {
        "name": "stage121_web",
        "category": "recon",
        "path": "plugins\\recon\\stage121_web\\plugin.py"
    },
    {
        "name": "stage122_catalog",
        "category": "recon",
        "path": "plugins\\recon\\stage122_catalog\\plugin.py"
    },
    {
        "name": "stage123_catalog",
        "category": "recon",
        "path": "plugins\\recon\\stage123_catalog\\plugin.py"
    },
    {
        "name": "start",
        "category": "recon",
        "path": "plugins\\recon\\start\\plugin.py"
    },
    {
        "name": "stats",
        "category": "recon",
        "path": "plugins\\recon\\stats\\plugin.py"
    },
    {
        "name": "stderr",
        "category": "recon",
        "path": "plugins\\recon\\stderr\\plugin.py"
    },
    {
        "name": "stderr_1",
        "category": "recon",
        "path": "plugins\\recon\\stderr_1\\plugin.py"
    },
    {
        "name": "stealth_crawler",
        "category": "recon",
        "path": "plugins\\recon\\stealth_crawler\\plugin.py"
    },
    {
        "name": "stig-analyst",
        "category": "recon",
        "path": "plugins\\recon\\stig-analyst\\plugin.py"
    },
    {
        "name": "subdomain",
        "category": "recon",
        "path": "plugins\\recon\\subdomain\\plugin.py"
    },
    {
        "name": "subdomain-enumeration",
        "category": "recon",
        "path": "plugins\\recon\\subdomain-enumeration\\plugin.py"
    },
    {
        "name": "subdomain-hunter-agent",
        "category": "recon",
        "path": "plugins\\recon\\subdomain-hunter-agent\\plugin.py"
    },
    {
        "name": "subdomainstxt",
        "category": "recon",
        "path": "plugins\\recon\\subdomainstxt\\plugin.py"
    },
    {
        "name": "subdomains_1",
        "category": "recon",
        "path": "plugins\\recon\\subdomains_1\\plugin.py"
    },
    {
        "name": "subdomains_2",
        "category": "recon",
        "path": "plugins\\recon\\subdomains_2\\plugin.py"
    },
    {
        "name": "subdomains_v0",
        "category": "recon",
        "path": "plugins\\recon\\subdomains_v0\\plugin.py"
    },
    {
        "name": "subdomains_v1",
        "category": "recon",
        "path": "plugins\\recon\\subdomains_v1\\plugin.py"
    },
    {
        "name": "subdomains_v2",
        "category": "recon",
        "path": "plugins\\recon\\subdomains_v2\\plugin.py"
    },
    {
        "name": "subfinder-logo",
        "category": "recon",
        "path": "plugins\\recon\\subfinder-logo\\plugin.py"
    },
    {
        "name": "subfinder-run",
        "category": "recon",
        "path": "plugins\\recon\\subfinder-run\\plugin.py"
    },
    {
        "name": "subfinder_2",
        "category": "recon",
        "path": "plugins\\recon\\subfinder_2\\plugin.py"
    },
    {
        "name": "sublist3r_tool",
        "category": "recon",
        "path": "plugins\\recon\\sublist3r_tool\\plugin.py"
    },
    {
        "name": "submd",
        "category": "recon",
        "path": "plugins\\recon\\submd\\plugin.py"
    },
    {
        "name": "SUBPROCESSORS",
        "category": "recon",
        "path": "plugins\\recon\\SUBPROCESSORS\\plugin.py"
    },
    {
        "name": "subs",
        "category": "recon",
        "path": "plugins\\recon\\subs\\plugin.py"
    },
    {
        "name": "suggestion_engine",
        "category": "recon",
        "path": "plugins\\recon\\suggestion_engine\\plugin.py"
    },
    {
        "name": "support",
        "category": "recon",
        "path": "plugins\\recon\\support\\plugin.py"
    },
    {
        "name": "support_test",
        "category": "recon",
        "path": "plugins\\recon\\support_test\\plugin.py"
    },
    {
        "name": "swagger",
        "category": "recon",
        "path": "plugins\\recon\\swagger\\plugin.py"
    },
    {
        "name": "swarm-orchestrator",
        "category": "recon",
        "path": "plugins\\recon\\swarm-orchestrator\\plugin.py"
    },
    {
        "name": "tag_engine",
        "category": "recon",
        "path": "plugins\\recon\\tag_engine\\plugin.py"
    },
    {
        "name": "takeover_detector",
        "category": "recon",
        "path": "plugins\\recon\\takeover_detector\\plugin.py"
    },
    {
        "name": "target-model",
        "category": "recon",
        "path": "plugins\\recon\\target-model\\plugin.py"
    },
    {
        "name": "target_classifier",
        "category": "recon",
        "path": "plugins\\recon\\target_classifier\\plugin.py"
    },
    {
        "name": "task-management",
        "category": "recon",
        "path": "plugins\\recon\\task-management\\plugin.py"
    },
    {
        "name": "tech-fingerprinter-agent",
        "category": "recon",
        "path": "plugins\\recon\\tech-fingerprinter-agent\\plugin.py"
    },
    {
        "name": "templates",
        "category": "recon",
        "path": "plugins\\recon\\templates\\plugin.py"
    },
    {
        "name": "template_manager",
        "category": "recon",
        "path": "plugins\\recon\\template_manager\\plugin.py"
    },
    {
        "name": "TERMS",
        "category": "recon",
        "path": "plugins\\recon\\TERMS\\plugin.py"
    },
    {
        "name": "test-lsg-v2",
        "category": "recon",
        "path": "plugins\\recon\\test-lsg-v2\\plugin.py"
    },
    {
        "name": "test-suite",
        "category": "recon",
        "path": "plugins\\recon\\test-suite\\plugin.py"
    },
    {
        "name": "test1",
        "category": "recon",
        "path": "plugins\\recon\\test1\\plugin.py"
    },
    {
        "name": "test2",
        "category": "recon",
        "path": "plugins\\recon\\test2\\plugin.py"
    },
    {
        "name": "test_api_server",
        "category": "recon",
        "path": "plugins\\recon\\test_api_server\\plugin.py"
    },
    {
        "name": "test_arjun_integration",
        "category": "recon",
        "path": "plugins\\recon\\test_arjun_integration\\plugin.py"
    },
    {
        "name": "test_authenticated_scan_coverage",
        "category": "recon",
        "path": "plugins\\recon\\test_authenticated_scan_coverage\\plugin.py"
    },
    {
        "name": "test_auth_profiles_smoke",
        "category": "recon",
        "path": "plugins\\recon\\test_auth_profiles_smoke\\plugin.py"
    },
    {
        "name": "test_auth_scan_e2e_smoke",
        "category": "recon",
        "path": "plugins\\recon\\test_auth_scan_e2e_smoke\\plugin.py"
    },
    {
        "name": "test_auth_session",
        "category": "recon",
        "path": "plugins\\recon\\test_auth_session\\plugin.py"
    },
    {
        "name": "test_auth_session_bearer_flow",
        "category": "recon",
        "path": "plugins\\recon\\test_auth_session_bearer_flow\\plugin.py"
    },
    {
        "name": "test_browser_agent_e2e_smoke",
        "category": "recon",
        "path": "plugins\\recon\\test_browser_agent_e2e_smoke\\plugin.py"
    },
    {
        "name": "test_browser_crawler",
        "category": "recon",
        "path": "plugins\\recon\\test_browser_crawler\\plugin.py"
    },
    {
        "name": "test_checkpoint",
        "category": "recon",
        "path": "plugins\\recon\\test_checkpoint\\plugin.py"
    },
    {
        "name": "test_ci_mode",
        "category": "recon",
        "path": "plugins\\recon\\test_ci_mode\\plugin.py"
    },
    {
        "name": "test_cli",
        "category": "recon",
        "path": "plugins\\recon\\test_cli\\plugin.py"
    },
    {
        "name": "test_cli_auth_coverage",
        "category": "recon",
        "path": "plugins\\recon\\test_cli_auth_coverage\\plugin.py"
    },
    {
        "name": "test_common",
        "category": "recon",
        "path": "plugins\\recon\\test_common\\plugin.py"
    },
    {
        "name": "test_csrf_auth_e2e_smoke",
        "category": "recon",
        "path": "plugins\\recon\\test_csrf_auth_e2e_smoke\\plugin.py"
    },
    {
        "name": "test_dashboard",
        "category": "recon",
        "path": "plugins\\recon\\test_dashboard\\plugin.py"
    },
    {
        "name": "test_dns_resolver_auto",
        "category": "recon",
        "path": "plugins\\recon\\test_dns_resolver_auto\\plugin.py"
    },
    {
        "name": "test_e2e_probes",
        "category": "recon",
        "path": "plugins\\recon\\test_e2e_probes\\plugin.py"
    },
    {
        "name": "test_engagement_lifecycle_e2e",
        "category": "recon",
        "path": "plugins\\recon\\test_engagement_lifecycle_e2e\\plugin.py"
    },
    {
        "name": "test_evidence_contract",
        "category": "recon",
        "path": "plugins\\recon\\test_evidence_contract\\plugin.py"
    },
    {
        "name": "test_exports",
        "category": "recon",
        "path": "plugins\\recon\\test_exports\\plugin.py"
    },
    {
        "name": "test_export_cli",
        "category": "recon",
        "path": "plugins\\recon\\test_export_cli\\plugin.py"
    },
    {
        "name": "test_full_flow",
        "category": "recon",
        "path": "plugins\\recon\\test_full_flow\\plugin.py"
    },
    {
        "name": "test_handler_meta",
        "category": "recon",
        "path": "plugins\\recon\\test_handler_meta\\plugin.py"
    },
    {
        "name": "test_integration_dvwa",
        "category": "recon",
        "path": "plugins\\recon\\test_integration_dvwa\\plugin.py"
    },
    {
        "name": "test_juiceshop_e2e_smoke",
        "category": "recon",
        "path": "plugins\\recon\\test_juiceshop_e2e_smoke\\plugin.py"
    },
    {
        "name": "test_llm_redteam",
        "category": "recon",
        "path": "plugins\\recon\\test_llm_redteam\\plugin.py"
    },
    {
        "name": "test_mcp_auth_profile",
        "category": "recon",
        "path": "plugins\\recon\\test_mcp_auth_profile\\plugin.py"
    },
    {
        "name": "test_mcp_server_coverage",
        "category": "recon",
        "path": "plugins\\recon\\test_mcp_server_coverage\\plugin.py"
    },
    {
        "name": "test_monitor",
        "category": "recon",
        "path": "plugins\\recon\\test_monitor\\plugin.py"
    },
    {
        "name": "test_monitor_mode",
        "category": "recon",
        "path": "plugins\\recon\\test_monitor_mode\\plugin.py"
    },
    {
        "name": "test_new_tool_integrations",
        "category": "recon",
        "path": "plugins\\recon\\test_new_tool_integrations\\plugin.py"
    },
    {
        "name": "test_phase6",
        "category": "recon",
        "path": "plugins\\recon\\test_phase6\\plugin.py"
    },
    {
        "name": "test_probe_asset_secrets",
        "category": "recon",
        "path": "plugins\\recon\\test_probe_asset_secrets\\plugin.py"
    },
    {
        "name": "test_probe_crawler",
        "category": "recon",
        "path": "plugins\\recon\\test_probe_crawler\\plugin.py"
    },
    {
        "name": "test_probe_exif_metadata",
        "category": "recon",
        "path": "plugins\\recon\\test_probe_exif_metadata\\plugin.py"
    },
    {
        "name": "test_probe_leaked_credentials",
        "category": "recon",
        "path": "plugins\\recon\\test_probe_leaked_credentials\\plugin.py"
    },
    {
        "name": "test_probe_nosql_fuzz",
        "category": "recon",
        "path": "plugins\\recon\\test_probe_nosql_fuzz\\plugin.py"
    },
    {
        "name": "test_probe_oauth_pkce_downgrade",
        "category": "recon",
        "path": "plugins\\recon\\test_probe_oauth_pkce_downgrade\\plugin.py"
    },
    {
        "name": "test_probe_sqli_fuzz",
        "category": "recon",
        "path": "plugins\\recon\\test_probe_sqli_fuzz\\plugin.py"
    },
    {
        "name": "test_probe_ssrf_cloud_metadata",
        "category": "cloud",
        "path": "plugins\\cloud\\test_probe_ssrf_cloud_metadata\\plugin.py"
    },
    {
        "name": "test_probe_ssti_fuzz",
        "category": "recon",
        "path": "plugins\\recon\\test_probe_ssti_fuzz\\plugin.py"
    },
    {
        "name": "test_probe_xss_fuzz",
        "category": "recon",
        "path": "plugins\\recon\\test_probe_xss_fuzz\\plugin.py"
    },
    {
        "name": "test_registry_coverage",
        "category": "recon",
        "path": "plugins\\recon\\test_registry_coverage\\plugin.py"
    },
    {
        "name": "test_registry_extended",
        "category": "recon",
        "path": "plugins\\recon\\test_registry_extended\\plugin.py"
    },
    {
        "name": "test_reporting",
        "category": "recon",
        "path": "plugins\\recon\\test_reporting\\plugin.py"
    },
    {
        "name": "test_report_only",
        "category": "recon",
        "path": "plugins\\recon\\test_report_only\\plugin.py"
    },
    {
        "name": "test_resolvers_external",
        "category": "recon",
        "path": "plugins\\recon\\test_resolvers_external\\plugin.py"
    },
    {
        "name": "test_resolvers_hardening",
        "category": "recon",
        "path": "plugins\\recon\\test_resolvers_hardening\\plugin.py"
    },
    {
        "name": "test_sanitize",
        "category": "recon",
        "path": "plugins\\recon\\test_sanitize\\plugin.py"
    },
    {
        "name": "test_scanners",
        "category": "recon",
        "path": "plugins\\recon\\test_scanners\\plugin.py"
    },
    {
        "name": "test_shell_syntax",
        "category": "recon",
        "path": "plugins\\recon\\test_shell_syntax\\plugin.py"
    },
    {
        "name": "test_smoke",
        "category": "recon",
        "path": "plugins\\recon\\test_smoke\\plugin.py"
    },
    {
        "name": "test_stage121_integration",
        "category": "recon",
        "path": "plugins\\recon\\test_stage121_integration\\plugin.py"
    },
    {
        "name": "test_stage122_integration",
        "category": "recon",
        "path": "plugins\\recon\\test_stage122_integration\\plugin.py"
    },
    {
        "name": "test_stage123_integration",
        "category": "recon",
        "path": "plugins\\recon\\test_stage123_integration\\plugin.py"
    },
    {
        "name": "test_stage13_orchestration",
        "category": "recon",
        "path": "plugins\\recon\\test_stage13_orchestration\\plugin.py"
    },
    {
        "name": "test_stage14_tui",
        "category": "recon",
        "path": "plugins\\recon\\test_stage14_tui\\plugin.py"
    },
    {
        "name": "test_stage15_plugins",
        "category": "recon",
        "path": "plugins\\recon\\test_stage15_plugins\\plugin.py"
    },
    {
        "name": "test_stage181_burp",
        "category": "recon",
        "path": "plugins\\recon\\test_stage181_burp\\plugin.py"
    },
    {
        "name": "test_stage182_traffic",
        "category": "recon",
        "path": "plugins\\recon\\test_stage182_traffic\\plugin.py"
    },
    {
        "name": "test_stage19_plugins",
        "category": "recon",
        "path": "plugins\\recon\\test_stage19_plugins\\plugin.py"
    },
    {
        "name": "test_stage20_services",
        "category": "recon",
        "path": "plugins\\recon\\test_stage20_services\\plugin.py"
    },
    {
        "name": "test_stealth_crawler",
        "category": "recon",
        "path": "plugins\\recon\\test_stealth_crawler\\plugin.py"
    },
    {
        "name": "test_subdomains_asn",
        "category": "recon",
        "path": "plugins\\recon\\test_subdomains_asn\\plugin.py"
    },
    {
        "name": "test_subdomains_filtering",
        "category": "recon",
        "path": "plugins\\recon\\test_subdomains_filtering\\plugin.py"
    },
    {
        "name": "test_sub_tls_no_match",
        "category": "recon",
        "path": "plugins\\recon\\test_sub_tls_no_match\\plugin.py"
    },
    {
        "name": "test_terminal_output_modes",
        "category": "recon",
        "path": "plugins\\recon\\test_terminal_output_modes\\plugin.py"
    },
    {
        "name": "test_tool_installer_extended",
        "category": "recon",
        "path": "plugins\\recon\\test_tool_installer_extended\\plugin.py"
    },
    {
        "name": "test_ui_snapshots",
        "category": "recon",
        "path": "plugins\\recon\\test_ui_snapshots\\plugin.py"
    },
    {
        "name": "test_utils",
        "category": "recon",
        "path": "plugins\\recon\\test_utils\\plugin.py"
    },
    {
        "name": "test_validation",
        "category": "recon",
        "path": "plugins\\recon\\test_validation\\plugin.py"
    },
    {
        "name": "test_vps_count_cli",
        "category": "recon",
        "path": "plugins\\recon\\test_vps_count_cli\\plugin.py"
    },
    {
        "name": "test_webprobe_full_formats",
        "category": "recon",
        "path": "plugins\\recon\\test_webprobe_full_formats\\plugin.py"
    },
    {
        "name": "test_web_agent_crawl_inject",
        "category": "recon",
        "path": "plugins\\recon\\test_web_agent_crawl_inject\\plugin.py"
    },
    {
        "name": "THANKS",
        "category": "recon",
        "path": "plugins\\recon\\THANKS\\plugin.py"
    },
    {
        "name": "thc",
        "category": "recon",
        "path": "plugins\\recon\\thc\\plugin.py"
    },
    {
        "name": "theharvester",
        "category": "recon",
        "path": "plugins\\recon\\theharvester\\plugin.py"
    },
    {
        "name": "threat-modeler",
        "category": "recon",
        "path": "plugins\\recon\\threat-modeler\\plugin.py"
    },
    {
        "name": "threatbook",
        "category": "recon",
        "path": "plugins\\recon\\threatbook\\plugin.py"
    },
    {
        "name": "threatcrowd",
        "category": "recon",
        "path": "plugins\\recon\\threatcrowd\\plugin.py"
    },
    {
        "name": "threatcrowd_2",
        "category": "recon",
        "path": "plugins\\recon\\threatcrowd_2\\plugin.py"
    },
    {
        "name": "threatminer",
        "category": "recon",
        "path": "plugins\\recon\\threatminer\\plugin.py"
    },
    {
        "name": "TIER2-EXECUTION",
        "category": "recon",
        "path": "plugins\\recon\\TIER2-EXECUTION\\plugin.py"
    },
    {
        "name": "TIMELINE",
        "category": "recon",
        "path": "plugins\\recon\\TIMELINE\\plugin.py"
    },
    {
        "name": "tlsx",
        "category": "recon",
        "path": "plugins\\recon\\tlsx\\plugin.py"
    },
    {
        "name": "tls_cert",
        "category": "recon",
        "path": "plugins\\recon\\tls_cert\\plugin.py"
    },
    {
        "name": "tls_cert_1",
        "category": "recon",
        "path": "plugins\\recon\\tls_cert_1\\plugin.py"
    },
    {
        "name": "tool-checker",
        "category": "recon",
        "path": "plugins\\recon\\tool-checker\\plugin.py"
    },
    {
        "name": "tool-runner",
        "category": "recon",
        "path": "plugins\\recon\\tool-runner\\plugin.py"
    },
    {
        "name": "tools",
        "category": "recon",
        "path": "plugins\\recon\\tools\\plugin.py"
    },
    {
        "name": "tool_browser",
        "category": "recon",
        "path": "plugins\\recon\\tool_browser\\plugin.py"
    },
    {
        "name": "tool_chains",
        "category": "recon",
        "path": "plugins\\recon\\tool_chains\\plugin.py"
    },
    {
        "name": "tool_installer",
        "category": "recon",
        "path": "plugins\\recon\\tool_installer\\plugin.py"
    },
    {
        "name": "tool_lessons",
        "category": "recon",
        "path": "plugins\\recon\\tool_lessons\\plugin.py"
    },
    {
        "name": "tool_registry",
        "category": "recon",
        "path": "plugins\\recon\\tool_registry\\plugin.py"
    },
    {
        "name": "tool_result",
        "category": "recon",
        "path": "plugins\\recon\\tool_result\\plugin.py"
    },
    {
        "name": "tool_schemas",
        "category": "recon",
        "path": "plugins\\recon\\tool_schemas\\plugin.py"
    },
    {
        "name": "tool_versions",
        "category": "recon",
        "path": "plugins\\recon\\tool_versions\\plugin.py"
    },
    {
        "name": "traffic_commands",
        "category": "recon",
        "path": "plugins\\recon\\traffic_commands\\plugin.py"
    },
    {
        "name": "traffic_view",
        "category": "recon",
        "path": "plugins\\recon\\traffic_view\\plugin.py"
    },
    {
        "name": "training-data-2025-12-24T03-29-17-267Z",
        "category": "recon",
        "path": "plugins\\recon\\training-data-2025-12-24T03-29-17-267Z\\plugin.py"
    },
    {
        "name": "transform",
        "category": "recon",
        "path": "plugins\\recon\\transform\\plugin.py"
    },
    {
        "name": "transform_test",
        "category": "recon",
        "path": "plugins\\recon\\transform_test\\plugin.py"
    },
    {
        "name": "transparentbanner",
        "category": "recon",
        "path": "plugins\\recon\\transparentbanner\\plugin.py"
    },
    {
        "name": "triage",
        "category": "recon",
        "path": "plugins\\recon\\triage\\plugin.py"
    },
    {
        "name": "tshark",
        "category": "recon",
        "path": "plugins\\recon\\tshark\\plugin.py"
    },
    {
        "name": "tshark_engine",
        "category": "recon",
        "path": "plugins\\recon\\tshark_engine\\plugin.py"
    },
    {
        "name": "txt",
        "category": "recon",
        "path": "plugins\\recon\\txt\\plugin.py"
    },
    {
        "name": "txt_1",
        "category": "recon",
        "path": "plugins\\recon\\txt_1\\plugin.py"
    },
    {
        "name": "type",
        "category": "recon",
        "path": "plugins\\recon\\type\\plugin.py"
    },
    {
        "name": "types_1",
        "category": "recon",
        "path": "plugins\\recon\\types_1\\plugin.py"
    },
    {
        "name": "types_9",
        "category": "recon",
        "path": "plugins\\recon\\types_9\\plugin.py"
    },
    {
        "name": "unauthed-findings",
        "category": "recon",
        "path": "plugins\\recon\\unauthed-findings\\plugin.py"
    },
    {
        "name": "unauthed-findings_1",
        "category": "recon",
        "path": "plugins\\recon\\unauthed-findings_1\\plugin.py"
    },
    {
        "name": "url",
        "category": "recon",
        "path": "plugins\\recon\\url\\plugin.py"
    },
    {
        "name": "urlscan_2",
        "category": "recon",
        "path": "plugins\\recon\\urlscan_2\\plugin.py"
    },
    {
        "name": "uv_1",
        "category": "recon",
        "path": "plugins\\recon\\uv_1\\plugin.py"
    },
    {
        "name": "validate_2",
        "category": "recon",
        "path": "plugins\\recon\\validate_2\\plugin.py"
    },
    {
        "name": "vault",
        "category": "recon",
        "path": "plugins\\recon\\vault\\plugin.py"
    },
    {
        "name": "virtual-host-enumeration",
        "category": "recon",
        "path": "plugins\\recon\\virtual-host-enumeration\\plugin.py"
    },
    {
        "name": "virustotal",
        "category": "recon",
        "path": "plugins\\recon\\virustotal\\plugin.py"
    },
    {
        "name": "virustotal_1",
        "category": "recon",
        "path": "plugins\\recon\\virustotal_1\\plugin.py"
    },
    {
        "name": "virustotal_3",
        "category": "recon",
        "path": "plugins\\recon\\virustotal_3\\plugin.py"
    },
    {
        "name": "viz",
        "category": "recon",
        "path": "plugins\\recon\\viz\\plugin.py"
    },
    {
        "name": "vuln-hypothesizer",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\vuln-hypothesizer\\plugin.py"
    },
    {
        "name": "vuln-scanner",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\vuln-scanner\\plugin.py"
    },
    {
        "name": "vuln-ssrf",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\vuln-ssrf\\plugin.py"
    },
    {
        "name": "vuln-ssrf_2",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\vuln-ssrf_2\\plugin.py"
    },
    {
        "name": "vulnerability_concepts",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\vulnerability_concepts\\plugin.py"
    },
    {
        "name": "vuln_analysis",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\vuln_analysis\\plugin.py"
    },
    {
        "name": "waybackarchive",
        "category": "recon",
        "path": "plugins\\recon\\waybackarchive\\plugin.py"
    },
    {
        "name": "waybackurls_2",
        "category": "recon",
        "path": "plugins\\recon\\waybackurls_2\\plugin.py"
    },
    {
        "name": "wayback_1",
        "category": "recon",
        "path": "plugins\\recon\\wayback_1\\plugin.py"
    },
    {
        "name": "waymore",
        "category": "recon",
        "path": "plugins\\recon\\waymore\\plugin.py"
    },
    {
        "name": "web",
        "category": "recon",
        "path": "plugins\\recon\\web\\plugin.py"
    },
    {
        "name": "web-app-quick",
        "category": "recon",
        "path": "plugins\\recon\\web-app-quick\\plugin.py"
    },
    {
        "name": "web-hunter",
        "category": "recon",
        "path": "plugins\\recon\\web-hunter\\plugin.py"
    },
    {
        "name": "webshell-management",
        "category": "recon",
        "path": "plugins\\recon\\webshell-management\\plugin.py"
    },
    {
        "name": "web_agent",
        "category": "recon",
        "path": "plugins\\recon\\web_agent\\plugin.py"
    },
    {
        "name": "web_cache_deception",
        "category": "recon",
        "path": "plugins\\recon\\web_cache_deception\\plugin.py"
    },
    {
        "name": "web_pipeline",
        "category": "recon",
        "path": "plugins\\recon\\web_pipeline\\plugin.py"
    },
    {
        "name": "whoisxmlapi",
        "category": "recon",
        "path": "plugins\\recon\\whoisxmlapi\\plugin.py"
    },
    {
        "name": "whois_lookup",
        "category": "recon",
        "path": "plugins\\recon\\whois_lookup\\plugin.py"
    },
    {
        "name": "wildcard_detector",
        "category": "recon",
        "path": "plugins\\recon\\wildcard_detector\\plugin.py"
    },
    {
        "name": "windvane",
        "category": "recon",
        "path": "plugins\\recon\\windvane\\plugin.py"
    },
    {
        "name": "wireless-pentester",
        "category": "recon",
        "path": "plugins\\recon\\wireless-pentester\\plugin.py"
    },
    {
        "name": "workflow_builder",
        "category": "recon",
        "path": "plugins\\recon\\workflow_builder\\plugin.py"
    },
    {
        "name": "workflow_definitions",
        "category": "recon",
        "path": "plugins\\recon\\workflow_definitions\\plugin.py"
    },
    {
        "name": "workflow_planner",
        "category": "recon",
        "path": "plugins\\recon\\workflow_planner\\plugin.py"
    },
    {
        "name": "workflow_templates",
        "category": "recon",
        "path": "plugins\\recon\\workflow_templates\\plugin.py"
    },
    {
        "name": "world-model",
        "category": "recon",
        "path": "plugins\\recon\\world-model\\plugin.py"
    },
    {
        "name": "WorldModel",
        "category": "recon",
        "path": "plugins\\recon\\WorldModel\\plugin.py"
    },
    {
        "name": "WorldModeltest",
        "category": "recon",
        "path": "plugins\\recon\\WorldModeltest\\plugin.py"
    },
    {
        "name": "xbow-performance-comparison",
        "category": "recon",
        "path": "plugins\\recon\\xbow-performance-comparison\\plugin.py"
    },
    {
        "name": "xss-validator-agent",
        "category": "recon",
        "path": "plugins\\recon\\xss-validator-agent\\plugin.py"
    },
    {
        "name": "xss_fuzz",
        "category": "recon",
        "path": "plugins\\recon\\xss_fuzz\\plugin.py"
    },
    {
        "name": "zetalytics",
        "category": "recon",
        "path": "plugins\\recon\\zetalytics\\plugin.py"
    },
    {
        "name": "zoomeyeapi",
        "category": "recon",
        "path": "plugins\\recon\\zoomeyeapi\\plugin.py"
    },
    {
        "name": "zoomeye_search",
        "category": "recon",
        "path": "plugins\\recon\\zoomeye_search\\plugin.py"
    },
    {
        "name": "_11",
        "category": "recon",
        "path": "plugins\\recon\\_11\\plugin.py"
    },
    {
        "name": "_12",
        "category": "recon",
        "path": "plugins\\recon\\_12\\plugin.py"
    },
    {
        "name": "_15",
        "category": "recon",
        "path": "plugins\\recon\\_15\\plugin.py"
    },
    {
        "name": "_scope-guard",
        "category": "recon",
        "path": "plugins\\recon\\_scope-guard\\plugin.py"
    },
    {
        "name": "__init___105",
        "category": "recon",
        "path": "plugins\\recon\\__init___105\\plugin.py"
    },
    {
        "name": "__init___106",
        "category": "recon",
        "path": "plugins\\recon\\__init___106\\plugin.py"
    },
    {
        "name": "__init___107",
        "category": "recon",
        "path": "plugins\\recon\\__init___107\\plugin.py"
    },
    {
        "name": "__init___117",
        "category": "recon",
        "path": "plugins\\recon\\__init___117\\plugin.py"
    },
    {
        "name": "__init___121",
        "category": "recon",
        "path": "plugins\\recon\\__init___121\\plugin.py"
    },
    {
        "name": "__init___122",
        "category": "recon",
        "path": "plugins\\recon\\__init___122\\plugin.py"
    },
    {
        "name": "__init___129",
        "category": "recon",
        "path": "plugins\\recon\\__init___129\\plugin.py"
    },
    {
        "name": "__init___148",
        "category": "recon",
        "path": "plugins\\recon\\__init___148\\plugin.py"
    },
    {
        "name": "__init___149",
        "category": "recon",
        "path": "plugins\\recon\\__init___149\\plugin.py"
    },
    {
        "name": "__init___156",
        "category": "recon",
        "path": "plugins\\recon\\__init___156\\plugin.py"
    },
    {
        "name": "__init___30",
        "category": "recon",
        "path": "plugins\\recon\\__init___30\\plugin.py"
    },
    {
        "name": "__init___33",
        "category": "recon",
        "path": "plugins\\recon\\__init___33\\plugin.py"
    },
    {
        "name": "__init___36",
        "category": "recon",
        "path": "plugins\\recon\\__init___36\\plugin.py"
    },
    {
        "name": "__init___37",
        "category": "recon",
        "path": "plugins\\recon\\__init___37\\plugin.py"
    },
    {
        "name": "__main___1",
        "category": "recon",
        "path": "plugins\\recon\\__main___1\\plugin.py"
    },
    {
        "name": "analyze_repos",
        "category": "recon",
        "path": "plugins\\recon\\analyze_repos\\plugin.py"
    },
    {
        "name": "aquatone",
        "category": "recon",
        "path": "plugins\\recon\\aquatone\\plugin.py"
    },
    {
        "name": "artifact-manifest",
        "category": "recon",
        "path": "plugins\\recon\\artifact-manifest\\plugin.py"
    },
    {
        "name": "authed-stderr",
        "category": "recon",
        "path": "plugins\\recon\\authed-stderr\\plugin.py"
    },
    {
        "name": "banner_3",
        "category": "recon",
        "path": "plugins\\recon\\banner_3\\plugin.py"
    },
    {
        "name": "book",
        "category": "recon",
        "path": "plugins\\recon\\book\\plugin.py"
    },
    {
        "name": "bug_2",
        "category": "recon",
        "path": "plugins\\recon\\bug_2\\plugin.py"
    },
    {
        "name": "bug_report_2",
        "category": "recon",
        "path": "plugins\\recon\\bug_report_2\\plugin.py"
    },
    {
        "name": "capability_map",
        "category": "recon",
        "path": "plugins\\recon\\capability_map\\plugin.py"
    },
    {
        "name": "check_artifacts_all",
        "category": "recon",
        "path": "plugins\\recon\\check_artifacts_all\\plugin.py"
    },
    {
        "name": "chunk_eino",
        "category": "recon",
        "path": "plugins\\recon\\chunk_eino\\plugin.py"
    },
    {
        "name": "compare_baseline",
        "category": "recon",
        "path": "plugins\\recon\\compare_baseline\\plugin.py"
    },
    {
        "name": "config_test",
        "category": "recon",
        "path": "plugins\\recon\\config_test\\plugin.py"
    },
    {
        "name": "curl",
        "category": "recon",
        "path": "plugins\\recon\\curl\\plugin.py"
    },
    {
        "name": "diff",
        "category": "recon",
        "path": "plugins\\recon\\diff\\plugin.py"
    },
    {
        "name": "ding",
        "category": "recon",
        "path": "plugins\\recon\\ding\\plugin.py"
    },
    {
        "name": "dirsearch",
        "category": "recon",
        "path": "plugins\\recon\\dirsearch\\plugin.py"
    },
    {
        "name": "execution",
        "category": "recon",
        "path": "plugins\\recon\\execution\\plugin.py"
    },
    {
        "name": "fping_tool",
        "category": "recon",
        "path": "plugins\\recon\\fping_tool\\plugin.py"
    },
    {
        "name": "generator",
        "category": "recon",
        "path": "plugins\\recon\\generator\\plugin.py"
    },
    {
        "name": "generatorcpython-313",
        "category": "recon",
        "path": "plugins\\recon\\generatorcpython-313\\plugin.py"
    },
    {
        "name": "gitbook",
        "category": "recon",
        "path": "plugins\\recon\\gitbook\\plugin.py"
    },
    {
        "name": "ground-truth-validator",
        "category": "recon",
        "path": "plugins\\recon\\ground-truth-validator\\plugin.py"
    },
    {
        "name": "index_6",
        "category": "recon",
        "path": "plugins\\recon\\index_6\\plugin.py"
    },
    {
        "name": "index_pipeline_test",
        "category": "recon",
        "path": "plugins\\recon\\index_pipeline_test\\plugin.py"
    },
    {
        "name": "inputFiles",
        "category": "recon",
        "path": "plugins\\recon\\inputFiles\\plugin.py"
    },
    {
        "name": "lfi_wordlist",
        "category": "recon",
        "path": "plugins\\recon\\lfi_wordlist\\plugin.py"
    },
    {
        "name": "listener_websocket",
        "category": "recon",
        "path": "plugins\\recon\\listener_websocket\\plugin.py"
    },
    {
        "name": "Makefile_2",
        "category": "recon",
        "path": "plugins\\recon\\Makefile_2\\plugin.py"
    },
    {
        "name": "netdiscover_tool",
        "category": "recon",
        "path": "plugins\\recon\\netdiscover_tool\\plugin.py"
    },
    {
        "name": "plugin_manager",
        "category": "recon",
        "path": "plugins\\recon\\plugin_manager\\plugin.py"
    },
    {
        "name": "PULL_REQUEST_TEMPLATE",
        "category": "recon",
        "path": "plugins\\recon\\PULL_REQUEST_TEMPLATE\\plugin.py"
    },
    {
        "name": "radare2",
        "category": "recon",
        "path": "plugins\\recon\\radare2\\plugin.py"
    },
    {
        "name": "README_24",
        "category": "recon",
        "path": "plugins\\recon\\README_24\\plugin.py"
    },
    {
        "name": "renderer",
        "category": "recon",
        "path": "plugins\\recon\\renderer\\plugin.py"
    },
    {
        "name": "report-executive_1",
        "category": "recon",
        "path": "plugins\\recon\\report-executive_1\\plugin.py"
    },
    {
        "name": "reporter",
        "category": "recon",
        "path": "plugins\\recon\\reporter\\plugin.py"
    },
    {
        "name": "reporting-cherrytree",
        "category": "recon",
        "path": "plugins\\recon\\reporting-cherrytree\\plugin.py"
    },
    {
        "name": "reporting-markdown",
        "category": "recon",
        "path": "plugins\\recon\\reporting-markdown\\plugin.py"
    },
    {
        "name": "report_15",
        "category": "recon",
        "path": "plugins\\recon\\report_15\\plugin.py"
    },
    {
        "name": "report_generator",
        "category": "recon",
        "path": "plugins\\recon\\report_generator\\plugin.py"
    },
    {
        "name": "resource_availability",
        "category": "recon",
        "path": "plugins\\recon\\resource_availability\\plugin.py"
    },
    {
        "name": "rollback-beta",
        "category": "recon",
        "path": "plugins\\recon\\rollback-beta\\plugin.py"
    },
    {
        "name": "run_benchmarks",
        "category": "recon",
        "path": "plugins\\recon\\run_benchmarks\\plugin.py"
    },
    {
        "name": "run_tests",
        "category": "recon",
        "path": "plugins\\recon\\run_tests\\plugin.py"
    },
    {
        "name": "scan_optimizer",
        "category": "recon",
        "path": "plugins\\recon\\scan_optimizer\\plugin.py"
    },
    {
        "name": "session_manager",
        "category": "recon",
        "path": "plugins\\recon\\session_manager\\plugin.py"
    },
    {
        "name": "SKILL_22",
        "category": "recon",
        "path": "plugins\\recon\\SKILL_22\\plugin.py"
    },
    {
        "name": "ssh_manager",
        "category": "recon",
        "path": "plugins\\recon\\ssh_manager\\plugin.py"
    },
    {
        "name": "sslscan",
        "category": "recon",
        "path": "plugins\\recon\\sslscan\\plugin.py"
    },
    {
        "name": "targets",
        "category": "recon",
        "path": "plugins\\recon\\targets\\plugin.py"
    },
    {
        "name": "testssl",
        "category": "recon",
        "path": "plugins\\recon\\testssl\\plugin.py"
    },
    {
        "name": "test_hitl_coverage",
        "category": "recon",
        "path": "plugins\\recon\\test_hitl_coverage\\plugin.py"
    },
    {
        "name": "test_list_targets",
        "category": "recon",
        "path": "plugins\\recon\\test_list_targets\\plugin.py"
    },
    {
        "name": "test_parallel",
        "category": "recon",
        "path": "plugins\\recon\\test_parallel\\plugin.py"
    },
    {
        "name": "test_primitives_evidence_capture",
        "category": "recon",
        "path": "plugins\\recon\\test_primitives_evidence_capture\\plugin.py"
    },
    {
        "name": "test_probe_captcha_replay",
        "category": "recon",
        "path": "plugins\\recon\\test_probe_captcha_replay\\plugin.py"
    },
    {
        "name": "test_probe_response_headers",
        "category": "recon",
        "path": "plugins\\recon\\test_probe_response_headers\\plugin.py"
    },
    {
        "name": "test_probe_ssti_polyglot",
        "category": "recon",
        "path": "plugins\\recon\\test_probe_ssti_polyglot\\plugin.py"
    },
    {
        "name": "test_stage2",
        "category": "recon",
        "path": "plugins\\recon\\test_stage2\\plugin.py"
    },
    {
        "name": "throttle",
        "category": "recon",
        "path": "plugins\\recon\\throttle\\plugin.py"
    },
    {
        "name": "tls_fingerprint",
        "category": "recon",
        "path": "plugins\\recon\\tls_fingerprint\\plugin.py"
    },
    {
        "name": "tool-responses",
        "category": "recon",
        "path": "plugins\\recon\\tool-responses\\plugin.py"
    },
    {
        "name": "tool_health",
        "category": "recon",
        "path": "plugins\\recon\\tool_health\\plugin.py"
    },
    {
        "name": "train-archnet",
        "category": "recon",
        "path": "plugins\\recon\\train-archnet\\plugin.py"
    },
    {
        "name": "training-data-2025-12-24T03-31-48-760Z",
        "category": "recon",
        "path": "plugins\\recon\\training-data-2025-12-24T03-31-48-760Z\\plugin.py"
    },
    {
        "name": "training-data-2025-12-24T04-13-25-236Z",
        "category": "recon",
        "path": "plugins\\recon\\training-data-2025-12-24T04-13-25-236Z\\plugin.py"
    },
    {
        "name": "training-data-2025-12-24T04-32-35-147Z",
        "category": "recon",
        "path": "plugins\\recon\\training-data-2025-12-24T04-32-35-147Z\\plugin.py"
    },
    {
        "name": "training-data-2025-12-24T04-43-48-405Z",
        "category": "recon",
        "path": "plugins\\recon\\training-data-2025-12-24T04-43-48-405Z\\plugin.py"
    },
    {
        "name": "types_6",
        "category": "recon",
        "path": "plugins\\recon\\types_6\\plugin.py"
    },
    {
        "name": "vuln-authz_1",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\vuln-authz_1\\plugin.py"
    },
    {
        "name": "vuln-auth_1",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\vuln-auth_1\\plugin.py"
    },
    {
        "name": "vuln-injection_1",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\vuln-injection_1\\plugin.py"
    },
    {
        "name": "webhook-reporter",
        "category": "recon",
        "path": "plugins\\recon\\webhook-reporter\\plugin.py"
    },
    {
        "name": "websocket",
        "category": "recon",
        "path": "plugins\\recon\\websocket\\plugin.py"
    },
    {
        "name": "workflow_player",
        "category": "recon",
        "path": "plugins\\recon\\workflow_player\\plugin.py"
    },
    {
        "name": "workflow_recorder",
        "category": "recon",
        "path": "plugins\\recon\\workflow_recorder\\plugin.py"
    },
    {
        "name": "workspaces_1",
        "category": "recon",
        "path": "plugins\\recon\\workspaces_1\\plugin.py"
    },
    {
        "name": "__init___54",
        "category": "recon",
        "path": "plugins\\recon\\__init___54\\plugin.py"
    },
    {
        "name": "agent_loop",
        "category": "recon",
        "path": "plugins\\recon\\agent_loop\\plugin.py"
    },
    {
        "name": "API",
        "category": "recon",
        "path": "plugins\\recon\\API\\plugin.py"
    },
    {
        "name": "api-security",
        "category": "recon",
        "path": "plugins\\recon\\api-security\\plugin.py"
    },
    {
        "name": "api_security_agent",
        "category": "recon",
        "path": "plugins\\recon\\api_security_agent\\plugin.py"
    },
    {
        "name": "api_surface_mapper",
        "category": "recon",
        "path": "plugins\\recon\\api_surface_mapper\\plugin.py"
    },
    {
        "name": "apply_triage_labels",
        "category": "recon",
        "path": "plugins\\recon\\apply_triage_labels\\plugin.py"
    },
    {
        "name": "arjun_tool",
        "category": "recon",
        "path": "plugins\\recon\\arjun_tool\\plugin.py"
    },
    {
        "name": "base_5",
        "category": "recon",
        "path": "plugins\\recon\\base_5\\plugin.py"
    },
    {
        "name": "benchmark_juice_shop",
        "category": "recon",
        "path": "plugins\\recon\\benchmark_juice_shop\\plugin.py"
    },
    {
        "name": "business_logic_fuzz",
        "category": "recon",
        "path": "plugins\\recon\\business_logic_fuzz\\plugin.py"
    },
    {
        "name": "chat_uploads",
        "category": "recon",
        "path": "plugins\\recon\\chat_uploads\\plugin.py"
    },
    {
        "name": "ci-cd",
        "category": "recon",
        "path": "plugins\\recon\\ci-cd\\plugin.py"
    },
    {
        "name": "cicd-redteam",
        "category": "recon",
        "path": "plugins\\recon\\cicd-redteam\\plugin.py"
    },
    {
        "name": "compliance",
        "category": "recon",
        "path": "plugins\\recon\\compliance\\plugin.py"
    },
    {
        "name": "const",
        "category": "recon",
        "path": "plugins\\recon\\const\\plugin.py"
    },
    {
        "name": "constants_1",
        "category": "recon",
        "path": "plugins\\recon\\constants_1\\plugin.py"
    },
    {
        "name": "crlfuzz",
        "category": "recon",
        "path": "plugins\\recon\\crlfuzz\\plugin.py"
    },
    {
        "name": "dalfox",
        "category": "recon",
        "path": "plugins\\recon\\dalfox\\plugin.py"
    },
    {
        "name": "dirbuster_2",
        "category": "recon",
        "path": "plugins\\recon\\dirbuster_2\\plugin.py"
    },
    {
        "name": "dirsearch_2",
        "category": "recon",
        "path": "plugins\\recon\\dirsearch_2\\plugin.py"
    },
    {
        "name": "dirsearch_tool",
        "category": "recon",
        "path": "plugins\\recon\\dirsearch_tool\\plugin.py"
    },
    {
        "name": "Dockerfile_6",
        "category": "recon",
        "path": "plugins\\recon\\Dockerfile_6\\plugin.py"
    },
    {
        "name": "efd01c52_findings",
        "category": "recon",
        "path": "plugins\\recon\\efd01c52_findings\\plugin.py"
    },
    {
        "name": "efd01c52_llm_coordinated_run",
        "category": "recon",
        "path": "plugins\\recon\\efd01c52_llm_coordinated_run\\plugin.py"
    },
    {
        "name": "eino_tool_name_injection",
        "category": "recon",
        "path": "plugins\\recon\\eino_tool_name_injection\\plugin.py"
    },
    {
        "name": "enhanced-report",
        "category": "recon",
        "path": "plugins\\recon\\enhanced-report\\plugin.py"
    },
    {
        "name": "example-report-excerpt",
        "category": "recon",
        "path": "plugins\\recon\\example-report-excerpt\\plugin.py"
    },
    {
        "name": "example_sqlmap",
        "category": "recon",
        "path": "plugins\\recon\\example_sqlmap\\plugin.py"
    },
    {
        "name": "example_sqlmap_1",
        "category": "recon",
        "path": "plugins\\recon\\example_sqlmap_1\\plugin.py"
    },
    {
        "name": "exploit",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\exploit\\plugin.py"
    },
    {
        "name": "exploit-injection_2",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\exploit-injection_2\\plugin.py"
    },
    {
        "name": "feroxbuster",
        "category": "recon",
        "path": "plugins\\recon\\feroxbuster\\plugin.py"
    },
    {
        "name": "ffuf",
        "category": "recon",
        "path": "plugins\\recon\\ffuf\\plugin.py"
    },
    {
        "name": "ffuf_tool",
        "category": "recon",
        "path": "plugins\\recon\\ffuf_tool\\plugin.py"
    },
    {
        "name": "findings_1",
        "category": "recon",
        "path": "plugins\\recon\\findings_1\\plugin.py"
    },
    {
        "name": "ghost-traffic",
        "category": "recon",
        "path": "plugins\\recon\\ghost-traffic\\plugin.py"
    },
    {
        "name": "ghost-traffictest",
        "category": "recon",
        "path": "plugins\\recon\\ghost-traffictest\\plugin.py"
    },
    {
        "name": "HTB_challenge_Template",
        "category": "recon",
        "path": "plugins\\recon\\HTB_challenge_Template\\plugin.py"
    },
    {
        "name": "index_10",
        "category": "recon",
        "path": "plugins\\recon\\index_10\\plugin.py"
    },
    {
        "name": "INSTALL",
        "category": "recon",
        "path": "plugins\\recon\\INSTALL\\plugin.py"
    },
    {
        "name": "install_1",
        "category": "recon",
        "path": "plugins\\recon\\install_1\\plugin.py"
    },
    {
        "name": "install_planner",
        "category": "recon",
        "path": "plugins\\recon\\install_planner\\plugin.py"
    },
    {
        "name": "library",
        "category": "recon",
        "path": "plugins\\recon\\library\\plugin.py"
    },
    {
        "name": "llm-app-redteam",
        "category": "recon",
        "path": "plugins\\recon\\llm-app-redteam\\plugin.py"
    },
    {
        "name": "mapping",
        "category": "recon",
        "path": "plugins\\recon\\mapping\\plugin.py"
    },
    {
        "name": "mobile_agent",
        "category": "recon",
        "path": "plugins\\recon\\mobile_agent\\plugin.py"
    },
    {
        "name": "mock_pipelinetest",
        "category": "recon",
        "path": "plugins\\recon\\mock_pipelinetest\\plugin.py"
    },
    {
        "name": "nmap-ajp",
        "category": "recon",
        "path": "plugins\\recon\\nmap-ajp\\plugin.py"
    },
    {
        "name": "nmap-cassandra",
        "category": "recon",
        "path": "plugins\\recon\\nmap-cassandra\\plugin.py"
    },
    {
        "name": "nmap-cups",
        "category": "recon",
        "path": "plugins\\recon\\nmap-cups\\plugin.py"
    },
    {
        "name": "nmap-ftp",
        "category": "recon",
        "path": "plugins\\recon\\nmap-ftp\\plugin.py"
    },
    {
        "name": "nmap-http",
        "category": "recon",
        "path": "plugins\\recon\\nmap-http\\plugin.py"
    },
    {
        "name": "nmap-imap",
        "category": "recon",
        "path": "plugins\\recon\\nmap-imap\\plugin.py"
    },
    {
        "name": "nmap-ldap",
        "category": "recon",
        "path": "plugins\\recon\\nmap-ldap\\plugin.py"
    },
    {
        "name": "nmap-mongodb",
        "category": "recon",
        "path": "plugins\\recon\\nmap-mongodb\\plugin.py"
    },
    {
        "name": "nmap-mountd",
        "category": "recon",
        "path": "plugins\\recon\\nmap-mountd\\plugin.py"
    },
    {
        "name": "nmap-mssql",
        "category": "recon",
        "path": "plugins\\recon\\nmap-mssql\\plugin.py"
    },
    {
        "name": "nmap-mysql",
        "category": "recon",
        "path": "plugins\\recon\\nmap-mysql\\plugin.py"
    },
    {
        "name": "nmap-nfs",
        "category": "recon",
        "path": "plugins\\recon\\nmap-nfs\\plugin.py"
    },
    {
        "name": "nmap-ntp",
        "category": "recon",
        "path": "plugins\\recon\\nmap-ntp\\plugin.py"
    },
    {
        "name": "nmap-oracle",
        "category": "recon",
        "path": "plugins\\recon\\nmap-oracle\\plugin.py"
    },
    {
        "name": "nmap-pop3",
        "category": "recon",
        "path": "plugins\\recon\\nmap-pop3\\plugin.py"
    },
    {
        "name": "nmap-rdp",
        "category": "recon",
        "path": "plugins\\recon\\nmap-rdp\\plugin.py"
    },
    {
        "name": "nmap-rsync",
        "category": "recon",
        "path": "plugins\\recon\\nmap-rsync\\plugin.py"
    },
    {
        "name": "nmap-smb",
        "category": "recon",
        "path": "plugins\\recon\\nmap-smb\\plugin.py"
    },
    {
        "name": "nmap-smtp",
        "category": "recon",
        "path": "plugins\\recon\\nmap-smtp\\plugin.py"
    },
    {
        "name": "nmap-snmp",
        "category": "recon",
        "path": "plugins\\recon\\nmap-snmp\\plugin.py"
    },
    {
        "name": "nmap-vnc",
        "category": "recon",
        "path": "plugins\\recon\\nmap-vnc\\plugin.py"
    },
    {
        "name": "nuclei-agent",
        "category": "recon",
        "path": "plugins\\recon\\nuclei-agent\\plugin.py"
    },
    {
        "name": "nuclei-template-sha",
        "category": "recon",
        "path": "plugins\\recon\\nuclei-template-sha\\plugin.py"
    },
    {
        "name": "parameter_discovery",
        "category": "recon",
        "path": "plugins\\recon\\parameter_discovery\\plugin.py"
    },
    {
        "name": "pentestGPT_HTB_phonebook_failed",
        "category": "recon",
        "path": "plugins\\recon\\pentestGPT_HTB_phonebook_failed\\plugin.py"
    },
    {
        "name": "pentestGPT_log_HTB_Precious",
        "category": "recon",
        "path": "plugins\\recon\\pentestGPT_log_HTB_Precious\\plugin.py"
    },
    {
        "name": "pentesting",
        "category": "recon",
        "path": "plugins\\recon\\pentesting\\plugin.py"
    },
    {
        "name": "playbook",
        "category": "recon",
        "path": "plugins\\recon\\playbook\\plugin.py"
    },
    {
        "name": "plugin_12",
        "category": "recon",
        "path": "plugins\\recon\\plugin_12\\plugin.py"
    },
    {
        "name": "probes",
        "category": "recon",
        "path": "plugins\\recon\\probes\\plugin.py"
    },
    {
        "name": "prompt_class_v1",
        "category": "recon",
        "path": "plugins\\recon\\prompt_class_v1\\plugin.py"
    },
    {
        "name": "prompt_class_v2",
        "category": "recon",
        "path": "plugins\\recon\\prompt_class_v2\\plugin.py"
    },
    {
        "name": "ptt_reasoning",
        "category": "recon",
        "path": "plugins\\recon\\ptt_reasoning\\plugin.py"
    },
    {
        "name": "pyproject_4",
        "category": "recon",
        "path": "plugins\\recon\\pyproject_4\\plugin.py"
    },
    {
        "name": "README_16",
        "category": "recon",
        "path": "plugins\\recon\\README_16\\plugin.py"
    },
    {
        "name": "README_23",
        "category": "recon",
        "path": "plugins\\recon\\README_23\\plugin.py"
    },
    {
        "name": "README_26",
        "category": "recon",
        "path": "plugins\\recon\\README_26\\plugin.py"
    },
    {
        "name": "README_36",
        "category": "recon",
        "path": "plugins\\recon\\README_36\\plugin.py"
    },
    {
        "name": "README_7",
        "category": "recon",
        "path": "plugins\\recon\\README_7\\plugin.py"
    },
    {
        "name": "README_EN",
        "category": "recon",
        "path": "plugins\\recon\\README_EN\\plugin.py"
    },
    {
        "name": "realdemo",
        "category": "recon",
        "path": "plugins\\recon\\realdemo\\plugin.py"
    },
    {
        "name": "realdemo-paced",
        "category": "recon",
        "path": "plugins\\recon\\realdemo-paced\\plugin.py"
    },
    {
        "name": "reconftw_quick",
        "category": "recon",
        "path": "plugins\\recon\\reconftw_quick\\plugin.py"
    },
    {
        "name": "replay_engine",
        "category": "recon",
        "path": "plugins\\recon\\replay_engine\\plugin.py"
    },
    {
        "name": "requirements_9",
        "category": "recon",
        "path": "plugins\\recon\\requirements_9\\plugin.py"
    },
    {
        "name": "response_headers",
        "category": "recon",
        "path": "plugins\\recon\\response_headers\\plugin.py"
    },
    {
        "name": "ROADMAP",
        "category": "recon",
        "path": "plugins\\recon\\ROADMAP\\plugin.py"
    },
    {
        "name": "runner_1",
        "category": "recon",
        "path": "plugins\\recon\\runner_1\\plugin.py"
    },
    {
        "name": "run_summary_1",
        "category": "recon",
        "path": "plugins\\recon\\run_summary_1\\plugin.py"
    },
    {
        "name": "SCORE_1",
        "category": "recon",
        "path": "plugins\\recon\\SCORE_1\\plugin.py"
    },
    {
        "name": "SCORE_2",
        "category": "recon",
        "path": "plugins\\recon\\SCORE_2\\plugin.py"
    },
    {
        "name": "SECURITY",
        "category": "recon",
        "path": "plugins\\recon\\SECURITY\\plugin.py"
    },
    {
        "name": "SECURITY_2",
        "category": "recon",
        "path": "plugins\\recon\\SECURITY_2\\plugin.py"
    },
    {
        "name": "security_tools",
        "category": "recon",
        "path": "plugins\\recon\\security_tools\\plugin.py"
    },
    {
        "name": "server_2",
        "category": "recon",
        "path": "plugins\\recon\\server_2\\plugin.py"
    },
    {
        "name": "server_3",
        "category": "recon",
        "path": "plugins\\recon\\server_3\\plugin.py"
    },
    {
        "name": "severity_engine",
        "category": "recon",
        "path": "plugins\\recon\\severity_engine\\plugin.py"
    },
    {
        "name": "SHANNON-PRO",
        "category": "recon",
        "path": "plugins\\recon\\SHANNON-PRO\\plugin.py"
    },
    {
        "name": "SKILL_19",
        "category": "recon",
        "path": "plugins\\recon\\SKILL_19\\plugin.py"
    },
    {
        "name": "SKILL_2",
        "category": "recon",
        "path": "plugins\\recon\\SKILL_2\\plugin.py"
    },
    {
        "name": "SKILL_23",
        "category": "recon",
        "path": "plugins\\recon\\SKILL_23\\plugin.py"
    },
    {
        "name": "solution",
        "category": "recon",
        "path": "plugins\\recon\\solution\\plugin.py"
    },
    {
        "name": "solved-challenges",
        "category": "recon",
        "path": "plugins\\recon\\solved-challenges\\plugin.py"
    },
    {
        "name": "spa_probes",
        "category": "recon",
        "path": "plugins\\recon\\spa_probes\\plugin.py"
    },
    {
        "name": "SPEC",
        "category": "recon",
        "path": "plugins\\recon\\SPEC\\plugin.py"
    },
    {
        "name": "sqli_login_bypass",
        "category": "recon",
        "path": "plugins\\recon\\sqli_login_bypass\\plugin.py"
    },
    {
        "name": "sqlmap",
        "category": "recon",
        "path": "plugins\\recon\\sqlmap\\plugin.py"
    },
    {
        "name": "ssti_stored",
        "category": "recon",
        "path": "plugins\\recon\\ssti_stored\\plugin.py"
    },
    {
        "name": "STAGE2",
        "category": "recon",
        "path": "plugins\\recon\\STAGE2\\plugin.py"
    },
    {
        "name": "stdout",
        "category": "recon",
        "path": "plugins\\recon\\stdout\\plugin.py"
    },
    {
        "name": "stdout_1",
        "category": "recon",
        "path": "plugins\\recon\\stdout_1\\plugin.py"
    },
    {
        "name": "summary",
        "category": "recon",
        "path": "plugins\\recon\\summary\\plugin.py"
    },
    {
        "name": "test_agents_parallel",
        "category": "recon",
        "path": "plugins\\recon\\test_agents_parallel\\plugin.py"
    },
    {
        "name": "test_api_security_e2e_smoke",
        "category": "recon",
        "path": "plugins\\recon\\test_api_security_e2e_smoke\\plugin.py"
    },
    {
        "name": "test_cache",
        "category": "recon",
        "path": "plugins\\recon\\test_cache\\plugin.py"
    },
    {
        "name": "test_core",
        "category": "recon",
        "path": "plugins\\recon\\test_core\\plugin.py"
    },
    {
        "name": "test_dedup",
        "category": "recon",
        "path": "plugins\\recon\\test_dedup\\plugin.py"
    },
    {
        "name": "test_evidence",
        "category": "recon",
        "path": "plugins\\recon\\test_evidence\\plugin.py"
    },
    {
        "name": "test_full_workflow",
        "category": "recon",
        "path": "plugins\\recon\\test_full_workflow\\plugin.py"
    },
    {
        "name": "test_install_preferences",
        "category": "recon",
        "path": "plugins\\recon\\test_install_preferences\\plugin.py"
    },
    {
        "name": "test_mcp_honeypot_e2e",
        "category": "recon",
        "path": "plugins\\recon\\test_mcp_honeypot_e2e\\plugin.py"
    },
    {
        "name": "test_mcp_security_tools",
        "category": "recon",
        "path": "plugins\\recon\\test_mcp_security_tools\\plugin.py"
    },
    {
        "name": "test_misc_coverage",
        "category": "recon",
        "path": "plugins\\recon\\test_misc_coverage\\plugin.py"
    },
    {
        "name": "test_mobile_agent_e2e_smoke",
        "category": "recon",
        "path": "plugins\\recon\\test_mobile_agent_e2e_smoke\\plugin.py"
    },
    {
        "name": "test_observation_normalization",
        "category": "recon",
        "path": "plugins\\recon\\test_observation_normalization\\plugin.py"
    },
    {
        "name": "test_os_execution",
        "category": "recon",
        "path": "plugins\\recon\\test_os_execution\\plugin.py"
    },
    {
        "name": "test_payload_library",
        "category": "recon",
        "path": "plugins\\recon\\test_payload_library\\plugin.py"
    },
    {
        "name": "test_perf_profile",
        "category": "recon",
        "path": "plugins\\recon\\test_perf_profile\\plugin.py"
    },
    {
        "name": "test_probe_business_logic_fuzz",
        "category": "recon",
        "path": "plugins\\recon\\test_probe_business_logic_fuzz\\plugin.py"
    },
    {
        "name": "test_severity_calibration",
        "category": "recon",
        "path": "plugins\\recon\\test_severity_calibration\\plugin.py"
    },
    {
        "name": "test_tool_bridge",
        "category": "recon",
        "path": "plugins\\recon\\test_tool_bridge\\plugin.py"
    },
    {
        "name": "test_tool_bridge_e2e",
        "category": "recon",
        "path": "plugins\\recon\\test_tool_bridge_e2e\\plugin.py"
    },
    {
        "name": "test_tool_installer",
        "category": "recon",
        "path": "plugins\\recon\\test_tool_installer\\plugin.py"
    },
    {
        "name": "test_tool_installer_coverage",
        "category": "recon",
        "path": "plugins\\recon\\test_tool_installer_coverage\\plugin.py"
    },
    {
        "name": "test_tool_result_persistence",
        "category": "recon",
        "path": "plugins\\recon\\test_tool_result_persistence\\plugin.py"
    },
    {
        "name": "tool_bridge",
        "category": "recon",
        "path": "plugins\\recon\\tool_bridge\\plugin.py"
    },
    {
        "name": "triage-results",
        "category": "recon",
        "path": "plugins\\recon\\triage-results\\plugin.py"
    },
    {
        "name": "triage-rubric",
        "category": "recon",
        "path": "plugins\\recon\\triage-rubric\\plugin.py"
    },
    {
        "name": "triage-summary",
        "category": "recon",
        "path": "plugins\\recon\\triage-summary\\plugin.py"
    },
    {
        "name": "triage_sample",
        "category": "recon",
        "path": "plugins\\recon\\triage_sample\\plugin.py"
    },
    {
        "name": "types_2",
        "category": "recon",
        "path": "plugins\\recon\\types_2\\plugin.py"
    },
    {
        "name": "validator",
        "category": "recon",
        "path": "plugins\\recon\\validator\\plugin.py"
    },
    {
        "name": "vars",
        "category": "recon",
        "path": "plugins\\recon\\vars\\plugin.py"
    },
    {
        "name": "version",
        "category": "recon",
        "path": "plugins\\recon\\version\\plugin.py"
    },
    {
        "name": "vulns",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\vulns\\plugin.py"
    },
    {
        "name": "vuln_correlator",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\vuln_correlator\\plugin.py"
    },
    {
        "name": "vuln_pipeline",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\vuln_pipeline\\plugin.py"
    },
    {
        "name": "vuln_scanner_agent",
        "category": "vulnerabilities",
        "path": "plugins\\vulnerabilities\\vuln_scanner_agent\\plugin.py"
    },
    {
        "name": "web_enum",
        "category": "recon",
        "path": "plugins\\recon\\web_enum\\plugin.py"
    },
    {
        "name": "xss",
        "category": "recon",
        "path": "plugins\\recon\\xss\\plugin.py"
    },
    {
        "name": "__init___135",
        "category": "recon",
        "path": "plugins\\recon\\__init___135\\plugin.py"
    },
    {
        "name": "__init___218",
        "category": "recon",
        "path": "plugins\\recon\\__init___218\\plugin.py"
    },
    {
        "name": "__init___35",
        "category": "recon",
        "path": "plugins\\recon\\__init___35\\plugin.py"
    }
]
    @classmethod
    def get_plugin(cls, name):
        for p in cls.plugins: 
            if p['name'] == name: return p
        return None
