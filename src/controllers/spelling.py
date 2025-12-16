import random
import sqlite3
from types import SimpleNamespace

from fastapi import Request
from fastapi.responses import RedirectResponse

from src.templates import templates

async def index(request: Request):
    with sqlite3.connect("esl.db") as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM spelling_list;")
        spelling_lists = [SimpleNamespace(**row) for row in cursor.fetchall()]

    return templates.TemplateResponse(
        request=request,
        name="spelling/index.html",
        context={"spelling_lists": spelling_lists}
    )

async def lists_new(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="spelling/lists/new.html",
        context={}
    )

async def lists_create(request: Request):
    form_data = await request.form()
    
    list_name = form_data.get("list_name")
    if not list_name:
        return RedirectResponse(url="/spelling/lists/new", status_code=303)
    
    words = form_data.getlist("words")
    for word in words:
        if not word:
            return RedirectResponse(url="/spelling/lists/new", status_code=303)

    try:
        with sqlite3.connect("esl.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("INSERT INTO spelling_list (name) VALUES (?);", (list_name, ))
            spelling_list_id = cursor.lastrowid

            words_to_insert = []
            for word in words:
                words_to_insert.append((word, spelling_list_id))
            
            cursor.executemany("INSERT INTO spelling_list_word (word, list_id) VALUES (?, ?);", words_to_insert)
            conn.commit()
    except Exception as e:
        print(f"something went wrong storing spelling list: {e}")
        return RedirectResponse(url="/spelling/lists/new", status_code=303)
    
    return RedirectResponse(url="/spelling", status_code=303)

async def missing_letters(request: Request, list_id: int):
    with sqlite3.connect("esl.db") as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM spelling_list WHERE list_id = ?;", (list_id, ))
        list = cursor.fetchone()
        
        cursor.execute("SELECT * FROM spelling_list_word WHERE list_id = ?;", (list_id, ))
        words = [SimpleNamespace(**row) for row in cursor.fetchall()]

    word_order = request.query_params.get("order") if request.query_params.get("order") else None
    
    if word_order == "shuffle":
        random.shuffle(words)

    num_of_missing_letters = int(request.query_params.get("letters")) if request.query_params.get("letters") else None

    if num_of_missing_letters:
        for word in words:
            whole_word = word.word
            letter_index = random.randrange(len(whole_word))
            letter = whole_word[letter_index]
            word.word = whole_word.replace(letter,"_", 1)

        return templates.TemplateResponse(
            request=request,
            name="spelling/missing-letters.html",
            context={"list": list, "words": words}
        )


    return templates.TemplateResponse(
        request=request,
        name="spelling/missing-letters.html",
        context={"list": list, "words": words}
    )