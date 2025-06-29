import re

class UrlScanner:
    def __init__(self):
        self.URL_REGEX = re.compile(r"https?://[^\s\"']+")

    def extract_urls_from_text(self, text):
        return self.URL_REGEX.findall(text)

    def extract_urls_from_message(self, message):
        # walk payload parts, decode base64 bodies, collect URLs
        urls = []
        def _walk(parts):
            for p in parts:
                data = p.get("body", {}).get("data")
                if data:
                    import base64
                    txt = base64.urlsafe_b64decode(data).decode(errors="ignore")
                    urls.extend(self.extract_urls_from_text(txt))
                if p.get("parts"):
                    _walk(p["parts"])
        payload = message.get("payload", {})
        parts = payload.get("parts", [payload])
        _walk(parts)
        return list(set(urls))  # dedupe
