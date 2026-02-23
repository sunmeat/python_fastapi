# py -m pip install "fastapi[standard]" uvicorn sqlalchemy pydantic greenlet pydantic-settings

from fastapi import FastAPI, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from database import get_db, engine, Base
from crud import get_messages, create_message
from schemas import MessageCreate

import webbrowser
import threading

from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Гостьова книга")

Base.metadata.create_all(bind=engine) # створює всі таблиці в базі даних, які описані в моделях

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates") # об'єкт для роботи з шаблонами, вказана папка, де вони знаходяться

@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    messages = get_messages(db, limit=100)
    return templates.TemplateResponse(
        "guestbook.html",
        {
            "request": request,
            "messages": messages,
            "title": "Гостьова книга"
        }
    )

@app.post("/", response_class=RedirectResponse)
async def add_message(
    name: str = Form(...),
    text: str = Form(...),
    db: Session = Depends(get_db)
):
    name = name.strip()
    text = text.strip()

    if not name or not text:
        # можна повернути помилку на сторінці, але для простоти редірект
        return RedirectResponse(url="/", status_code=303)

    create_message(db, name=name, text=text)
    return RedirectResponse(url="/", status_code=303)

# опціональний API ендпоінт
@app.get("/api/messages")
def api_messages(db: Session = Depends(get_db)):
    return get_messages(db, limit=100)

if __name__ == "__main__":
    def open_browser():
        webbrowser.open_new("http://localhost:8000")

    # відкриття браузера з невеликою затримкою (щоб сервер встиг стартанути)
    threading.Timer(1.5, open_browser).start()

    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)