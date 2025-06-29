import os
from dotenv import load_dotenv
load_dotenv()

SCOPES = os.getenv("SCOPES")
client_secret_path = os.getenv("client_secret_path")
token_path = os.getenv("token_path")