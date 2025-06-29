import requests
import time

class UrlScanIOClient:
    def __init__(self):
        self.base_url = "https://urlscan.io/api/v1"
        self.headers = {"Content-Type":"application/json"}
    
    # single url scan
    def scan_url(self, url,):
        response = requests.post(
        f"{self.base_url}/scan/",
        headers=self.headers,
        json={"url": url, "public":"off"})

        response.raise_for_status()
        return response.json()
    
    def get_result(self, uuid):
        response = requests.get(f"{self.base_url}/result/{uuid}/",
            headers=self.headers
        )

        response.raise_for_status()
        return response.json()
    
    def scan_urls(self, urls):
        wait_time = 10
        results = []

        for url in urls:

            print(f"Scanning {url}…")

            uuid = self.scan_url(url, "off")
            print(f" → Scan queued (UUID={uuid}), waiting {wait_time}s…")
            time.sleep(wait_time)

            
            print(" → Fetching result…")
            result = self.get_result(uuid)
            results.append(result)
        return results