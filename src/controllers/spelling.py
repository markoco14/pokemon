import random

from fastapi import Request

from src.templates import templates

async def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="spelling/index.html",
        context={}
    )

async def missing_letters(request: Request):

    words = ["window", "clock", "door", "house", "roof", "chimney"]

    word_order = request.query_params.get("order") if request.query_params.get("order") else None
    
    if word_order == "shuffle":
        random.shuffle(words)

    num_of_missing_letters = int(request.query_params.get("letters")) if request.query_params.get("letters") else None

    if num_of_missing_letters:
        words_with_missing_letters = []

        for word in words:
            letter_index = random.randrange(len(word))
            letter = word[letter_index]
            words_with_missing_letters.append(word.replace(letter,"_", 1))

        return templates.TemplateResponse(
            request=request,
            name="spelling/missing-letters.html",
            context={"words": words_with_missing_letters}
        )


    return templates.TemplateResponse(
        request=request,
        name="spelling/missing-letters.html",
        context={"words": words}
    )