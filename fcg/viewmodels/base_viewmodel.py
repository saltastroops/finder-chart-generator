from typing import Any, Literal

from fastapi import Request


OutputFormat = Literal["pdf", "png"]


class BaseViewModel:
    def __init__(self, request: Request):
        self.request = request
        self.errors: dict[str, str] = dict()

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__
