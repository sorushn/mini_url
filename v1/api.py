from typing import Union
import logging
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import RedirectResponse
from icecream import ic

from mini_url.v1 import functions

app = FastAPI()


@app.get("/favicon.ico")
def favicon():
    return RedirectResponse(url="/static/favicon.ico")


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/shorten/")
def shorten_url(long_url: str):
    return {"long_url": long_url, "short_url": functions.shorten_url(long_url)}


@app.get("/red/{url_hash}")
def read_item(url_hash: str):
    long_url = functions.unshorten_url(url_hash)
    ic(long_url)
    if long_url:
        return RedirectResponse(url=long_url, status_code=302)
    else:
        return {"message": "URL not found"}
