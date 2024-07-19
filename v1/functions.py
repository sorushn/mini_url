import hashlib
import redis
import urllib
from fastapi.responses import RedirectResponse
from icecream import ic

r = redis.StrictRedis('localhost', 6379, charset="utf-8", db=0,
                      decode_responses=True)


def ensure_schema(url: str) -> str:
    parsed_url = urllib.parse.urlparse(url)
    if not parsed_url.scheme:
        # Assume https as the default schema
        return f"https://{url}".encode("utf-8")
    return url


def shorten_url(long_url):
    long_url = ensure_schema(long_url)
    if r.exists(long_url):
        return urllib.parse.urljoin('http://localhost:8000/red/', r.get(long_url))
    url_hash = hashlib.md5(long_url).hexdigest()
    new_url = urllib.parse.urljoin('http://localhost:8000/red/',
                                   url_hash)
    r.set(long_url, url_hash)
    r.set(url_hash, long_url)
    return new_url


def unshorten_url(url_hash):
    # if r.exists(url_hash):
    #     return r.get(url_hash)
    return r.get(url_hash)
