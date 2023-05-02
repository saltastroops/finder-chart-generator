from astropy.coordinates import Angle
from fastapi import Request, UploadFile

from fcg.viewmodels import parse
from fcg.viewmodels.base_viewmodel import BaseViewModel


class LongslitViewModel(BaseViewModel):
    def __init__(self, request: Request):
        super().__init__(request)
        self.proposal_code = ""
        self.principal_investigator = ""
        self.target = ""
        self.right_ascension: Angle | None = None
        self.declination: Angle | None = None
        self.slit_width: Angle | None = None
        self.background_image: str | UploadFile | None = None
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

        # right ascension
        self.right_ascension = parse.parse_right_ascension(form, self.errors)

        # declination
        self.declination = parse.parse_declination(form, self.errors)

        # position angle
        self.position_angle = parse.parse_position_angle(form, self.errors)

        # slit width
        self.slit_width = parse.parse_slit_width(form, self.errors)

        # background image
        self.background_image = parse.parse_background_image(form, self.errors)
