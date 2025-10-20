from fastapi import FastAPI, Request

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/src/static", StaticFiles(directory="src/static"), name="static")

templates = Jinja2Templates(directory="src/templates")


async def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="halloween/index.html",
        context={}
    )