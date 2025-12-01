from typing import Annotated, TypedDict
from fastapi import FastAPI, Form, Request, Response

from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.templates import templates

# class IndexPage(TypedDict):


async def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="christmas/index.html",
        context={}
    )

async def teach(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="christmas/teach.html",
        context={}
    )