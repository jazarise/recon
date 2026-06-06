import re
from core.utils.http_client import HttpClient

class JSCrawler:
    def __init__(self):
        self.http = HttpClient()

    def crawl(self, url: str) -> dict:
        """
        Crawls a URL to extract inline scripts and linked JS files.
        Returns a dict mapping URLs to their JS content.
        """
        results = {}
        print(f"[*] Crawling {url} for JavaScript bundles...")
        
        # 1. Fetch main HTML
        response = self.http.get(url)
        if not response:
            return results
            
        html_content = response.text
        
        # 2. Extract inline scripts (basic mock regex)
        inline_scripts = re.findall(r'<script[^>]*>(.*?)</script>', html_content, re.DOTALL | re.IGNORECASE)
        if inline_scripts:
            results[url] = "\n".join(inline_scripts)
            
        # 3. Extract linked scripts
        script_srcs = re.findall(r'<script[^>]+src=["\']([^"\']+\.js)["\']', html_content, re.IGNORECASE)
        
        for src in script_srcs:
            # Normalize URL (mocking url_normalizer)
            full_url = src if src.startswith("http") else f"{url.rstrip('/')}/{src.lstrip('/')}"
            
            print(f"[*] Fetching JS bundle: {full_url}")
            js_resp = self.http.get(full_url)
            if js_resp:
                results[full_url] = js_resp.text
                
        return results

js_crawler = JSCrawler()
