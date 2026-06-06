from colorama import Fore, init
init(autoreset=True)

def show_banner():
    print(Fore.CYAN + """
==================== DirX ====================
      Fastest Directory Bruteforce Tool
            Author: Krish X TDC
==============================================
""")

def print_header():
    print(f"{'PATH':<20} {'CODE':<5} {'SIZE':<10} RESULT")

def format_output(path, code, size, full_url=None):
    if code == 200:
        color = Fore.GREEN
    elif code == 403:
        color = Fore.YELLOW
    elif code in [301,302]:
        color = Fore.MAGENTA
    else:
        color = Fore.CYAN

    if code in [200,301,302] and full_url:
        return color + f"{path:<20} {code:<5} {size:<10} -> {full_url}"
    else:
        return color + f"{path:<20} {code:<5} {size}"
