from fastapi import FastAPI, Request, Response
from fastapi.staticfiles import StaticFiles

from infrastructure.jinja2 import templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def index(request: Request) -> Response:
    return templates.TemplateResponse("index.html", {"request": request})
