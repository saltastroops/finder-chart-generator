from datetime import datetime, timezone

from starlette.requests import Request

from fcg.viewmodels import parse
from fcg.viewmodels.base_viewmodel import BaseViewModel
from fcg.viewmodels.parse import (
    parse_horizons_identifier,
    parse_output_interval,
    parse_start_time,
)


class EphemeridesViewModel(BaseViewModel):
    def __init__(self, request: Request):
        super().__init__(request)
        self.end = datetime.fromtimestamp(0, timezone.utc)
        self.output_interval = 0
        self.identifier = ""
        self.start = datetime.fromtimestamp(0, timezone.utc)

    async def load(self) -> None:
        form = await self.request.form()

        # end time
        self.end = parse.parse_end_time(form, self.errors)

        # identifier
        self.identifier = parse_horizons_identifier(form, self.errors)

        # output interval
        self.output_interval = parse_output_interval(form, self.errors)

        # start time
        self.start = parse_start_time(form, self.errors)

        # the start time must be earlier than the end time
        if "start" not in self.errors and "end" not in self.errors:
            if self.start >= self.end:
                self.errors[
                    "__general"
                ] = "The start time must be earlier than the end time."
