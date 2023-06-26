from astropy.coordinates import Angle
from fastapi import Request
from starlette.datastructures import UploadFile

from fcg.viewmodels import parse
from fcg.viewmodels.form_base_viewmodel import FormBaseViewModel
from fcg.infrastructure.types import OutputFormat


class NirViewModel(FormBaseViewModel):
    def __init__(self, request: Request):
        super().__init__(request)
        self.right_ascension: Angle = Angle("0deg")
        self.declination: Angle = Angle("0deg")
        self.science_bundle_right_ascension: Angle = Angle("0deg")
        self.science_bundle_declination: Angle = Angle("0deg")
        self.nir_bundle_separation: Angle = Angle("0deg")
        self.position_angle: Angle = Angle("0deg")
        self.background_image: str | UploadFile = ""
        self.output_format: OutputFormat = "pdf"
        self.errors: dict[str, str] = dict()

    async def load(self) -> None:
        form = await self.request.form()

        super().load_common_data(form)

        # right ascension
        self.right_ascension = parse.parse_right_ascension(form, self.errors) or Angle(
            "0deg"
        )

        # declination
        self.declination = parse.parse_declination(form, self.errors) or Angle("0deg")

        # science bundle right ascension
        self.science_bundle_right_ascension = (
            parse.parse_science_bundle_right_ascension(form, self.errors)
        ) or Angle("0deg")

        # science bundle declination
        self.science_bundle_declination = parse.parse_science_bundle_declination(
            form, self.errors
        ) or Angle("0deg")

        # bundle separation
        self.nir_bundle_separation = parse.parse_nir_bundle_separation(
            form, self.errors
        ) or Angle("0deg")

        # position angle
        self.position_angle = parse.parse_position_angle(form, self.errors) or Angle(
            "0deg"
        )

        # background image
        self.background_image = parse.parse_background_image(form, self.errors) or ""

        # output format
        self.output_format = parse.parse_output_format(form, self.errors) or "pdf"
