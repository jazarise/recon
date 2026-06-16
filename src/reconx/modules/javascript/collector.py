from modules.javascript.crawler import js_crawler

class JSCollector:
    def collect(self, target: str) -> dict:
        """
        Takes a target domain/URL and uses the crawler to collect all associated JS.
        """
        url = target if target.startswith("http") else f"https://{target}"
        return js_crawler.crawl(url)

js_collector = JSCollector()
