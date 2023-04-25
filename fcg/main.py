from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from fcg.views import index, forms

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(index.router)
app.include_router(forms.router)
