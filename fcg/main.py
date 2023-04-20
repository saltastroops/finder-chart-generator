from fastapi import FastAPI, Request, Response

from infrastructure.jinja2 import templates

app = FastAPI()


@app.get("/")
def index(request: Request) -> Response:
    return templates.TemplateResponse("index.html", {"request": request})
