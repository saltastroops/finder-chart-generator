from astropy.coordinates import Angle
from fastapi import Request
from starlette.datastructures import UploadFile

from fcg.viewmodels import parse
from fcg.viewmodels.base_viewmodel import BaseViewModel, OutputFormat


class ImagingViewModel(BaseViewModel):
    def __init__(self, request: Request):
        super().__init__(request)
        self.proposal_code = ""
        self.principal_investigator = ""
        self.target = ""
        self.right_ascension: Angle = Angle("0deg")
        self.declination: Angle = Angle("0deg")
        self.position_angle: Angle = Angle("0deg")
        self.background_image: str | UploadFile = ""
        self.output_format: OutputFormat = "pdf"
        self.errors: dict[str, str] = dict()

    async def load(self) -> None:
        form = await self.request.form()

        # proposal code
        self.proposal_code = parse.parse_proposal_code(form, self.errors) or ""

        # Principal Investigator
        self.principal_investigator = (
            parse.parse_principal_investigator(form, self.errors) or ""
        )

        # target
        self.target = parse.parse_target(form, self.errors) or ""

        # right ascension
        self.right_ascension = parse.parse_right_ascension(form, self.errors) or Angle(
            "0deg"
        )

        # declination
        self.declination = parse.parse_declination(form, self.errors) or Angle("0deg")

        # position angle
        self.position_angle = parse.parse_position_angle(form, self.errors) or Angle(
            "0deg"
        )

        # background image
        self.background_image = parse.parse_background_image(
            form, self.errors
        ) or Angle("0deg")

        # output format
        self.output_format = parse.parse_output_format(form, self.errors) or "pdf"
