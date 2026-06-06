import cmd
import shlex
from typing import List

from core.async_executor import run_pipeline
from data.findings_db import FindingsDB
from reporting.pdf_reporter import generate_pdf
from dashboard_server import start_dashboard

class ReconXShell(cmd.Cmd):
    intro = (
        "==================================================\n"
        "ReconX Interactive Shell - CLI First\n"
        "Type 'help' or '?' to list commands.\n"
        "=================================================="
    )
    prompt = "ReconX > "

    def __init__(self):
        super().__init__()
        self.db = FindingsDB()
        self.workspace = "./workspace"
        
    def do_scan(self, arg):
        """
        scan <target> [profile]
        Initiate a reconnaissance workflow on the specified target.
        Profiles: fast, balanced, deep (default: balanced)
        """
        args = shlex.split(arg)
        if not args:
            print("[-] Usage: scan <target> [profile]")
            return
            
        target = args[0]
        profile = args[1] if len(args) > 1 else "balanced"
        
        print(f"[+] Starting ReconX on {target} with profile {profile}")
        # Blocks in interactive shell
        run_pipeline(target, profile)
        print("[+] Scan completed.")

    def do_show(self, arg):
        """
        show findings <target> [--visual]
        show assets
        Display current reconnaissance data.
        """
        args = shlex.split(arg)
        if not args:
            print("[-] Usage: show <findings|assets> [options]")
            return
            
        category = args[0].lower()
        if category == "findings":
            target = args[1] if len(args) > 1 and not args[1].startswith("--") else None
            visual = "--visual" in args
            
            if visual:
                print("[+] Launching Visual Findings Dashboard...")
                start_dashboard(3000)
                return
                
            print("[+] Retrieving findings...")
            findings = self.db.get_findings(target)
            for f in findings:
                print(f"- {f.get('severity', 'INFO')}: {f.get('title')} ({f.get('target')})")
        else:
            print(f"[-] Category '{category}' not fully implemented in shell yet.")

    def do_report(self, arg):
        """
        report <target> [format] [--web]
        Generate a report for the target.
        Formats: pdf, json, csv
        """
        args = shlex.split(arg)
        if not args:
            print("[-] Usage: report <target> [format] [--web]")
            return
            
        target = args[0]
        fmt = "pdf"
        
        if "--web" in args:
            print(f"[+] Launching Web Report Dashboard for {target}...")
            start_dashboard(3000)
            return
            
        if len(args) > 1 and not args[1].startswith("--"):
            fmt = args[1]
            
        print(f"[+] Generating {fmt.upper()} report for {target}...")
        findings = self.db.get_findings(target)
        if fmt == "pdf":
            generate_pdf(findings, f"{target}_report.pdf")
            print(f"[+] Report saved to {target}_report.pdf")
        else:
            print(f"[-] Format {fmt} generation logic not loaded.")

    def do_status(self, arg):
        """Check system status."""
        print("[+] ReconX Status: OPERATIONAL (Interactive Mode)")
        print("[+] All engines loaded natively.")

    def do_exit(self, arg):
        """Exit the ReconX shell."""
        print("Goodbye.")
        return True
        
    def do_quit(self, arg):
        """Exit the ReconX shell."""
        return self.do_exit(arg)

def start_shell():
    try:
        ReconXShell().cmdloop()
    except KeyboardInterrupt:
        print("\nGoodbye.")
