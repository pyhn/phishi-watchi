from flask import (
    Blueprint, render_template, request,
    redirect, url_for, flash
)
from .gmail_client import GmailClient
from .scanner     import UrlScanner
from .config      import SCOPES, CLIENT_SECRETS_PATH, TOKEN_PATH

bp = Blueprint('main', __name__)


scanner = UrlScanner()

# hold your GmailClient instance in memory
gmail_client = None

@bp.route("/", methods=["GET", "POST"])
def index():
    global gmail_client

    # if not yet logged in, send them to /oauth_login
    if gmail_client is None:
        return redirect(url_for("main.oauth_login"))

    if request.method == "POST":
        # you now have a logged-in client:
        email_content = request.form["email"]
        # TODO: extract URLs from email_content and scan
        result = "SAFE"
        return render_template("result.html", result=result)

    # initial GET: show the form
    return render_template("index.html")


@bp.route("/oauth_login")
def oauth_login():
    global gmail_client

    try:
        # this will run the browser-based flow the first time:
        gmail_client = GmailClient(
            SCOPES,
            client_secrets_path=CLIENT_SECRETS_PATH,
            token_path=TOKEN_PATH
        )
        flash("Successfully authenticated with Gmail!", "success")
    except Exception as e:
        flash(f"OAuth flow failed: {e}", "danger")

    # whether success or failure, go back to index
    return redirect(url_for("main.index"))