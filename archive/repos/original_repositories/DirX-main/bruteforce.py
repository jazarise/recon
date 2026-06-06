import aiohttp
import asyncio
import time
from config import TIMEOUT
from utils import print_header, format_output
import sys

completed = 0
total = 0
start_time = 0


def progress_bar():
    percent = completed / total if total else 0
    bar_len = 20
    filled = int(bar_len * percent)

    bar = "█" * filled + "░" * (bar_len - filled)

    elapsed = time.time() - start_time
    rate = completed / elapsed if elapsed > 0 else 0
    remaining = (total - completed) / rate if rate > 0 else 0

    eta = time.strftime("%M:%S", time.gmtime(remaining))

    sys.stdout.write(
        f"\r[{bar}] {percent*100:.1f}% ({completed}/{total}) | ETA: {eta}"
    )
    sys.stdout.flush()


async def fetch(session, url, path, sem, status_filter, exclude_filter, proxy):
    global completed

    full_url = f"{url}{path}"

    async with sem:
        try:
            async with session.get(
                full_url,
                timeout=TIMEOUT,
                allow_redirects=False,
                proxy=proxy
            ) as res:

                code = res.status
                size = len(await res.read())

                show = True

                if status_filter and code not in status_filter:
                    show = False

                if exclude_filter and code in exclude_filter:
                    show = False

                if show and code != 404:
                    sys.stdout.write("\r" + " "*100 + "\r")

                    if code in [200,301,302]:
                        print(format_output(path, code, f"{size}B", full_url))
                    else:
                        print(format_output(path, code, f"{size}B"))

                    progress_bar()

        except:
            pass

        completed += 1
        progress_bar()


async def run(url, paths, threads, status_filter, exclude_filter, proxy):
    connector = aiohttp.TCPConnector(limit=threads)
    timeout = aiohttp.ClientTimeout(total=TIMEOUT)
    sem = asyncio.Semaphore(threads)

    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        tasks = [
            fetch(session, url, p, sem, status_filter, exclude_filter, proxy)
            for p in paths
        ]
        await asyncio.gather(*tasks)


def start_scan(url, wordlist, threads, status_filter, exclude_filter, proxy):
    global total, completed, start_time

    with open(wordlist) as f:
        paths = ["/" + l.strip() for l in f if l.strip()]

    total = len(paths)
    completed = 0
    start_time = time.time()

    print_header()
    progress_bar()

    asyncio.run(run(url, paths, threads, status_filter, exclude_filter, proxy))

    sys.stdout.write("\r" + " " * 100 + "\r")
    sys.stdout.flush()

    print("="*60)
    print(f"Progress: {completed} / {total} (100.00%)")
    print("="*60)
    print("Finished")
    print("="*60)
