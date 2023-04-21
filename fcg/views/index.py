from fastapi import Request, Response, APIRouter

from fcg.viewmodels.index_viewmodel import IndexViewModel
from infrastructure.jinja2 import templates

router = APIRouter()


@router.get("/")
def index(request: Request) -> Response:
    vm = IndexViewModel(request)

    return templates.TemplateResponse("index.html", vm.to_dict())
