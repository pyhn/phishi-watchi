from flask import (
    Blueprint, render_template, request,
    redirect, url_for, flash
)
from .gmail_client import GmailClient
from .scanner     import UrlScanner
from .config      import SCOPES, CLIENT_SECRETS_PATH, TOKEN_PATH
from .urlscan_client import UrlScanIOClient

bp = Blueprint('main', __name__)

gmail = GmailClient(SCOPES, CLIENT_SECRETS_PATH, TOKEN_PATH)
scanner = UrlScanner()
urlscan_client = UrlScanIOClient()


@bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # 1) fetch last 5 message IDs
        msg_ids = gmail.fetch_last_n_messages(5)

        # 2) extract all URLs from those messages
        all_urls = []
        for mid in msg_ids:
            msg  = gmail.get_message(mid)
            urls = scanner.extract_urls_from_message(msg)
            all_urls.extend(urls)

        # dedupe
        all_urls = list(dict.fromkeys(all_urls))

        # 3) send each URL to urlscan.io
        scan_results = urlscan_client.scan_urls(all_urls)

        # pass the raw scan JSONs (or selected fields) to the template
        return render_template("results.html",
                               urls=all_urls,
                               scans=scan_results)

    # GET → show index.html
    return render_template("index.html")


