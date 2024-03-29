from fastapi import APIRouter, Request, Response

from fcg.infrastructure.jinja2 import templates
from fcg.viewmodels.index_viewmodel import IndexViewModel

router = APIRouter()


@router.get("/")
def index(request: Request) -> Response:
    vm = IndexViewModel(request)

    return templates.TemplateResponse("index.html", vm.to_dict())
