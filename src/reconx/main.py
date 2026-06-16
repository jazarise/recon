import sys
import argparse
from reconx.logger import setup_logging
from reconx.version import __version__
from reconx.api.server import start_server

BANNER = f"""
===================================================
                RECONX v{__version__} FINAL
         Enterprise SaaS / API Backend Service
===================================================
"""

def main():
    print(BANNER)
    setup_logging()
    
    parser = argparse.ArgumentParser(description="ReconX API Service")
    parser.add_argument("action", choices=["api"], help="Launch the API Server")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind")
    
    args = parser.parse_args()
        
    if args.action == "api":
        start_server(args.port)

if __name__ == "__main__":
    main()
