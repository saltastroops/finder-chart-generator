from fastapi import Request

from fcg.viewmodels.base_viewmodel import BaseViewModel


class IndexViewModel(BaseViewModel):
    def __init__(self, request: Request):
        super().__init__(request)
