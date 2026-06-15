import urllib.request
import time

def test_dashboard_startup():
    # Verify the dev server is running and returning HTML
    retries = 5
    success = False
    for i in range(retries):
        try:
            resp = urllib.request.urlopen("http://localhost:5173/")
            html = resp.read().decode('utf-8')
            assert "<div id=\"root\"></div>" in html
            assert "src=\"/src/main.jsx\"" in html
            success = True
            break
        except Exception as e:
            time.sleep(2)
    assert success, "Vite dev server did not respond or return valid React HTML"
    print("UI Test: Dashboard startup verified.")
    
if __name__ == "__main__":
    test_dashboard_startup()
