import os
from dotenv import load_dotenv
load_dotenv()

SCOPES = [ os.getenv("SCOPES", "").strip() ]
CLIENT_SECRETS_PATH = os.getenv("CLIENT_SECRETS_PATH")
TOKEN_PATH = os.getenv("TOKEN_PATH")
URLSCAN_KEY = os.getenv("URLSCAN_KEY")