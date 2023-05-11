from fastapi import Request, UploadFile

from fcg.viewmodels import parse
from fcg.viewmodels.base_viewmodel import BaseViewModel, OutputFormat


class MosViewModel(BaseViewModel):
    def __init__(self, request: Request):
        super().__init__(request)
        self.proposal_code = ""
        self.principal_investigator = ""
        self.target = ""
        self.mos_mask_file: UploadFile | None = None
        self.background_image: str | UploadFile | None = None
        self.output_format: OutputFormat | None = None
        self.errors: dict[str, str] = dict()

    async def load(self) -> None:
        form = await self.request.form()

        # proposal code
        self.proposal_code = parse.parse_proposal_code(form, self.errors)

        # Principal Investigator
        self.principal_investigator = parse.parse_principal_investigator(
            form, self.errors
        )

        # target
        self.target = parse.parse_target(form, self.errors)

        # MOS mask file
        self.mos_mask_file = parse.parse_mos_mask_file(form, self.errors)

        # background image
        self.background_image = parse.parse_background_image(form, self.errors)

        # output format
        self.output_format = parse.parse_output_format(form, self.errors)
