from typing import cast

from fastapi import Request
from starlette.datastructures import UploadFile

from fcg.infrastructure.types import OutputFormat
from fcg.viewmodels import parse
from fcg.viewmodels.form_base_viewmodel import FormBaseViewModel


class MosViewModel(FormBaseViewModel):
    def __init__(self, request: Request):
        super().__init__(request)
        self.mos_mask_file: UploadFile | None = None
        self.background_image: str | UploadFile = ""
        self.output_format: OutputFormat = "pdf"
        self.errors: dict[str, str] = dict()

    async def load(self) -> None:
        form = await self.request.form()

        super().load_common_data(form)

        # MOS mask file
        self.mos_mask_file = cast(
            UploadFile, parse.parse_mos_mask_file(form, self.errors)
        )

        # background image
        self.background_image = parse.parse_background_image(form, self.errors)

        # output format
        self.output_format = parse.parse_output_format(form, self.errors)
