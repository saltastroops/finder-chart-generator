from astropy.coordinates import Angle
from fastapi import Request

from fcg.viewmodels import parse
from fcg.viewmodels.form_base_viewmodel import FormBaseViewModel


class EquinoxConversionViewModel(FormBaseViewModel):
    def __init__(self, request: Request):
        super().__init__(request)
        self.right_ascension: Angle = Angle("0deg")
        self.declination: Angle = Angle("0deg")
        self.old_equinox: float = 2000
        self.new_equinox: float = 2000
        self.errors: dict[str, str] = dict()

    async def load(self) -> None:
        form = await self.request.form()

        # right ascension
        self.right_ascension = parse.parse_right_ascension(form, self.errors)

        # declination
        self.declination = parse.parse_declination(form, self.errors)

        # old equinox
        self.old_equinox = parse.parse_equinox(form, self.errors, "old_equinox")

        # new equinox
        self.new_equinox = parse.parse_equinox(form, self.errors, "new_equinox")
