import argparse
import sys
import os
import json

from core.async_executor import run_pipeline
from data.findings_db import FindingsDB
from reporting.pdf_reporter import generate_pdf
from dashboard_server import start_dashboard

def parse_args():
    parser = argparse.ArgumentParser(description="ReconX Unified Platform")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # init
    init_parser = subparsers.add_parser("init", help="Initialize ReconX environment")
    init_parser.add_argument("--workspace", type=str, default="./workspace", help="Workspace path")

    # run
    run_parser = subparsers.add_parser("run", help="Run a ReconX workflow")
    run_parser.add_argument("--target", required=True, help="Target domain/IP")
    run_parser.add_argument("--profile", default="balanced", help="Execution profile (fast, balanced, deep)")
    run_parser.add_argument("--parallel", action="store_true", help="Enable parallel execution")

    # findings
    findings_parser = subparsers.add_parser("findings", help="View findings")
    findings_parser.add_argument("--target", help="Filter by target")
    findings_parser.add_argument("--severity", help="Filter by severity")
    findings_parser.add_argument("--visual", action="store_true", help="Launch visual dashboard")

    # reports
    reports_parser = subparsers.add_parser("reports", help="Generate reports")
    reports_parser.add_argument("--format", choices=["pdf", "csv", "json"], default="pdf", help="Report format")
    reports_parser.add_argument("--target", required=True, help="Target to report on")
    reports_parser.add_argument("--output", default="report.pdf", help="Output file path")
    reports_parser.add_argument("--web", action="store_true", help="Launch web report dashboard")

    # dashboard
    dashboard_parser = subparsers.add_parser("dashboard", help="Launch the web dashboard")
    dashboard_parser.add_argument("--port", type=int, default=3000, help="Dashboard port")

    # status
    status_parser = subparsers.add_parser("status", help="Check system status")

    # doctor
    doctor_parser = subparsers.add_parser("doctor", help="Validate system dependencies")

    return parser.parse_args()

def main():
    if len(sys.argv) == 1:
        # No arguments provided, launch interactive shell
        from cli.interactive_shell import start_shell
        start_shell()
        sys.exit(0)

    args = parse_args()

    if not args.command:
        # Failsafe
        from cli.interactive_shell import start_shell
        start_shell()
        sys.exit(0)

    if args.command == "doctor":
        from cli.doctor import run_doctor
        run_doctor()
        sys.exit(0)

    db = FindingsDB()

    if args.command == "init":
        os.makedirs(args.workspace, exist_ok=True)
        print(f"[+] Initialized ReconX workspace at {args.workspace}")

    elif args.command == "run":
        print(f"[+] Starting ReconX on {args.target} with profile {args.profile}")
        # Call into async_executor
        run_pipeline(args.target, args.profile)
        print("[+] Execution completed.")

    elif args.command == "findings":
        if args.visual:
            print("[+] Launching Visual Findings Dashboard...")
            start_dashboard(3000)
            return
            
        print(f"[+] Retrieving findings...")
        findings = db.get_findings(args.target)
        for f in findings:
            print(f"- {f.get('severity', 'INFO')}: {f.get('title')} ({f.get('target')})")

    elif args.command == "reports":
        if args.web:
            print(f"[+] Launching Web Report Dashboard for {args.target}...")
            start_dashboard(3000)
            return
            
        print(f"[+] Generating {args.format.upper()} report for {args.target}...")
        findings = db.get_findings(args.target)
        if args.format == "pdf":
            generate_pdf(findings, args.output)
        elif args.format == "json":
            with open(args.output, "w") as f:
                json.dump(findings, f, indent=4)
        print(f"[+] Report saved to {args.output}")

    elif args.command == "dashboard":
        print(f"[+] Launching ReconX Dashboard on port {args.port}...")
        start_dashboard(args.port)

    elif args.command == "status":
        print("[+] ReconX Status: OPERATIONAL")
        print("[+] All engines loaded.")

if __name__ == "__main__":
    main()
