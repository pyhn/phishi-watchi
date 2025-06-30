import requests
import time
from .config import URLSCAN_KEY

class UrlScanIOClient:
    def __init__(self):
        self.base_url = "https://urlscan.io/api/v1"
        self.headers = {"Content-Type":"application/json"}
        self.headers["api-key"] = URLSCAN_KEY
    
    # single url scan
    def scan_url(self, url, visibility="private", country=None, tags=None):
        payload = {
            "url": url,
            "visibility": visibility
        }
        if country:
            payload["country"] = country
        if tags:
            payload["tags"] = tags

        # note the trailing slash on scan/
        resp = requests.post(
            f"{self.base_url}/scan/",
            headers=self.headers,
            json=payload
        )
        resp.raise_for_status()
        data = resp.json()
        # return only the uuid, since scan_urls expects that
        return data["uuid"]
    
    def get_result(self, uuid):
        max_retries = 10
        retry_delay = 3

        url = f"{self.base_url}/result/{uuid}/"
        for attempt in range(1, max_retries+1):
            resp = requests.get(url, headers=self.headers)
            if resp.status_code == 200:
                return resp.json()
            elif resp.status_code == 404:
                print(f"Result not ready yet (attempt {attempt}), retrying in {retry_delay}s…")
                time.sleep(retry_delay)
                continue
            else:
                # some other error (e.g. 401, 429)—bubble it up
                resp.raise_for_status()

        raise Exception(f"Result for {uuid} still not found after {max_retries} retries")
    
    def scan_urls(self, urls):
        wait_time = 5
        results = []

        for url in urls:

            print(f"Scanning {url}…")

            uuid = self.scan_url(url)
            print(f" → Scan queued (UUID={uuid}), waiting {wait_time}s…")
            time.sleep(wait_time)


            print(" → Fetching result…")
            result = self.get_result(uuid)
            results.append(result)
        return results