import os
from urllib.parse import urlsplit

from dotenv import load_dotenv

load_dotenv()


def database_url():
    """DATABASE_URL from the environment, with SSL required for hosted databases.

    Neon only accepts encrypted connections. Its connection string already
    ends in ?sslmode=require, but this adds it if it was left off. The local
    Docker database doesn't use SSL, so localhost is left alone.
    """
    url = os.environ["DATABASE_URL"]
    host = urlsplit(url).hostname or ""
    if host not in ("localhost", "127.0.0.1") and "sslmode=" not in url:
        url += ("&" if "?" in url else "?") + "sslmode=require"
    return url


DATABASE_URL = database_url()
