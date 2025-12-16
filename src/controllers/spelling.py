from fastapi import Request

from src.templates import templates

async def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="spelling/index.html",
        context={}
    )

async def missing_letters(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="spelling/missing-letters.html",
        context={}
    )