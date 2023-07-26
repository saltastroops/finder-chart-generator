from typing import cast

from astropy.coordinates import Angle
from fastapi import Request
from starlette.datastructures import UploadFile

from fcg.infrastructure.types import OutputFormat
from fcg.viewmodels import parse
from fcg.viewmodels.form_base_viewmodel import FormBaseViewModel


class LongslitViewModel(FormBaseViewModel):
    def __init__(self, request: Request):
        super().__init__(request)
        self.right_ascension: Angle = Angle("0deg")
        self.declination: Angle = Angle("0deg")
        self.reference_star_right_ascension: Angle | None = None
        self.reference_star_declination: Angle | None = None
        self.position_angle: Angle | None = None
        self.calculate_position_angle = False
        self.slit_width: Angle = Angle("0deg")
        self.background_image: str | UploadFile = ""
        self.output_format: OutputFormat = "pdf"
        self.errors: dict[str, str] = dict()

    async def load(self) -> None:
        form = await self.request.form()

        super().load_common_data(form)

        # right ascension
        self.right_ascension = parse.parse_right_ascension(form, self.errors)

        # declination
        self.declination = parse.parse_declination(form, self.errors)

        # reference star right ascension
        if cast(str, form.get("reference_star_right_ascension", "")).strip():
            self.reference_star_right_ascension = (
                parse.parse_reference_star_right_ascension(form, self.errors)
            )

        # reference star declination
        if cast(str, form.get("reference_star_declination", "")).strip():
            self.reference_star_declination = parse.parse_reference_star_declination(
                form, self.errors
            )

        # position angle
        if cast(str, form.get("position_angle", "")).strip():
            self.position_angle = parse.parse_position_angle(form, self.errors)

        # calculate the position angle?
        self.calculate_position_angle = "calculate_position_angle" in form

        # slit width
        self.slit_width = parse.parse_slit_width(form, self.errors)

        # background image
        self.background_image = parse.parse_background_image(form, self.errors)

        # output format
        self.output_format = parse.parse_output_format(form, self.errors)

        # error checking
        if (
            self.reference_star_right_ascension is not None
            and self.reference_star_declination is None
        ):
            self.errors[
                "reference_star_declination"
            ] = "A reference star right ascension requires a declination as well."
        if (
            self.reference_star_declination is not None
            and self.reference_star_right_ascension is None
        ):
            self.errors[
                "reference_star_right_ascension"
            ] = "A reference star declination requires a right ascension as well."

        if self.calculate_position_angle:
            if self.position_angle is not None:
                self.errors[
                    "position_angle"
                ] = "The position angle must not be supplied if it is calculated."
            if self.reference_star_right_ascension is None:
                self.errors[
                    "reference_star_right_ascension"
                ] = "The reference star right ascension is required for calculating the position angle."
            if self.reference_star_declination is None:
                self.errors[
                    "reference_star_declination"
                ] = "The reference star declination is required for calculating the position angle."

        if not self.calculate_position_angle and self.position_angle is None:
            self.errors["position_angle"] = "The position angle is missing."
