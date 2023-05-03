import platform

import matplotlib as mpl
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from fcg.views import index, finder_charts


# The default macOS backend for Matplotlib leads to crashes, hence we specifically
# choose the pdf one
if "darwin" in platform.system().lower():
    mpl.use("pdf")


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(index.router)
app.include_router(finder_charts.router)
