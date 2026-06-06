import argparse
from bruteforce import start_scan
from utils import show_banner
from colorama import Fore, init

init(autoreset=True)

def parse_list(value):
    return [int(x) for x in value.split(",")] if value else []

def main():
    show_banner()

    parser = argparse.ArgumentParser(
        prog="DirX",
        description="DirX - Fastest Directory Bruteforce Tool",
        formatter_class=argparse.RawTextHelpFormatter,
        add_help=False
    )

    parser.add_argument("-h", "--help", action="help", help="Show help menu")

    # Required
    req = parser.add_argument_group("Required")
    req.add_argument("-u", "--url", required=True, help="Target URL")
    req.add_argument("-w", "--wordlist", required=True, help="Wordlist file")

    # Optional
    opt = parser.add_argument_group("Optional")
    opt.add_argument("-t", "--threads", type=int, default=10, help="Threads (default: 10)")
    opt.add_argument("--status", help="Show only these codes (e.g. 200,403)")
    opt.add_argument("--exclude", help="Exclude codes (e.g. 404,500)")
    opt.add_argument("--proxy", help="Proxy (e.g. http://127.0.0.1:8080)")

    parser.epilog = """
Examples:
  python3 main.py -u https://example.com -w wordlist.txt
  python3 main.py -u https://target.com -w list.txt -t 20
  python3 main.py -u https://target.com -w list.txt --status 200,403
  python3 main.py -u https://target.com -w list.txt --proxy http://127.0.0.1:8080

Author:
  Krish X TDC
"""

    args = parser.parse_args()

    url = args.url.rstrip("/")
    wordlist = args.wordlist
    threads = args.threads
    status_filter = parse_list(args.status)
    exclude_filter = parse_list(args.exclude)
    proxy = args.proxy

    try:
        with open(wordlist) as f:
            total = sum(1 for l in f if l.strip())
    except:
        print(Fore.RED + "❌ Wordlist not found")
        return

    print(Fore.BLUE + f"\n[+] URL        : {url}")
    print(Fore.BLUE + f"[+] Wordlist   : {wordlist}")
    print(Fore.BLUE + f"[+] Threads    : {threads}")
    print(Fore.BLUE + f"[+] Total      : {total}")
    if proxy:
        print(Fore.BLUE + f"[+] Proxy      : {proxy}")

    print("="*60)

    start_scan(url, wordlist, threads, status_filter, exclude_filter, proxy)

if __name__ == "__main__":
    main()
