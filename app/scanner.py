import re, base64

class UrlScanner:
    URL_REGEX = re.compile(r"https?://[^\s\"'<>]+")

    def extract_urls_from_text(self, text):
        raw = self.URL_REGEX.findall(text)
        return [self._clean(u) for u in raw]

    def _clean(self, url):
        return re.sub(r"[<>…]+$", "", url)

    def extract_urls_from_message(self, message):
        urls = []
        def _walk(parts):
            for p in parts:
                data = p.get("body", {}).get("data")
                if data:
                    txt = base64.urlsafe_b64decode(data).decode(errors="ignore")
                    urls.extend(self.extract_urls_from_text(txt))
                if p.get("parts"):
                    _walk(p["parts"])
        payload = message.get("payload", {})
        _walk(payload.get("parts", [payload]))
        return list(dict.fromkeys(urls))  # dedupe, preserving order
